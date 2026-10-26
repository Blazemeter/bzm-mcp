"""
Copyright 2025 Perforce Software, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import annotations

import logging
from collections.abc import Sequence
from contextlib import nullcontext
from dataclasses import dataclass, field
from typing import Annotated, Any, Awaitable, Callable, Dict, Optional, Set, Union

import httpx
from mcp.server.fastmcp import Context, FastMCP
from pydantic import Field

from config.blazemeter import SUPPORT_MESSAGE
from config.identity import Identity, IdentityError
from config.runtime import AppRuntime
from config.session import (
    SESSION_TOOL_NAME,
    ChatSession,
    SessionError,
    SessionErrorCode,
    is_valid_session_id,
)
from config.session_context import (
    bind_session_context,
    current_credential,
    current_identity,
    current_session,
)
from config.token import BzmToken
from models.result import BaseResult
from tools.actions import ActionSpec, action_by_name, filter_actions, render_description
from tools.runtime_tools import run_tool_with_runtime
from tools.utils import (
    format_sanitized_traceback,
    normalize_action_args,
    tool_result,
    validate_required_args,
)

logger = logging.getLogger(__name__)

ToolDispatch = Callable[
    [str, Dict[str, Any], Optional[BzmToken], Context],
    Awaitable[BaseResult],
]

SESSION_ID_ARG = "session_id"
SESSION_HINT = (
    f"- **CRITICAL (session)**: Every call requires `{SESSION_ID_ARG}` (top-level or inside args). "
    f"Get it once per conversation with `{SESSION_TOOL_NAME}` action 'get' and reuse it in every call; "
    "never reuse a session_id from another conversation. If a call returns error_code "
    "SESSION_REQUIRED, SESSION_INVALID or SESSION_EXPIRED, get a new session_id, use it from then on, "
    "and re-run the calls whose tasks or dataframes you still need."
)
SESSION_ID_DESCRIPTION = (
    f"Chat session id returned by `{SESSION_TOOL_NAME}` action 'get', called once at the start of "
    "this conversation. Pass the same value in every call of this conversation; never one from "
    "another conversation."
)
PUBLIC_SESSION_ID_DESCRIPTION = (
    f"Optional: this conversation's session id from `{SESSION_TOOL_NAME}`, when it already has one."
)
# Module-level so the (string) annotations of the generated tool functions resolve.
SessionIdParam = Annotated[Optional[str], Field(description=SESSION_ID_DESCRIPTION)]
PublicSessionIdParam = Annotated[Optional[str], Field(description=PUBLIC_SESSION_ID_DESCRIPTION)]
PUBLIC_SESSION_HINT = (
    f"- Session: works without an API key or `{SESSION_ID_ARG}`. When the conversation already has a "
    f"`{SESSION_ID_ARG}` from `{SESSION_TOOL_NAME}`, pass it too so long-running results stay in that session."
)


@dataclass
class _CallContext:
    """What the gate let through for one call; unset parts mean "not validated"."""

    identity: Optional[Identity] = None
    session: Optional[ChatSession] = None
    credential: Optional[str] = None
    warnings: list[str] = field(default_factory=list)

    def binding(self):
        if self.identity is None:
            return nullcontext()
        return bind_session_context(self.identity, self.session, self.credential)


def _session_error(code: SessionErrorCode) -> BaseResult:
    return BaseResult(error=SessionError(code).message, error_code=code.value)


def _credential(token: Optional[BzmToken]) -> Optional[str]:
    # Opaque end-user credential the session is bound to (today the BlazeMeter
    # Authorization value; another auth method only changes this line).
    return token.as_basic_auth() if token is not None else None


async def _validate_session(
        runtime: AppRuntime,
        requested: Any,
        identity: Identity,
        credential: Optional[str],
) -> Union[BaseResult, ChatSession]:
    if requested is None or (isinstance(requested, str) and not requested.strip()):
        return _session_error(SessionErrorCode.REQUIRED)
    if not is_valid_session_id(requested) or not credential:
        return _session_error(SessionErrorCode.INVALID)
    try:
        return await runtime.sessions.touch(requested, identity.user_id, credential)
    except SessionError as exc:
        return _session_error(exc.code)
    except Exception:
        logger.exception("Session validation failed")
        return _session_error(SessionErrorCode.UNAVAILABLE)


async def _enter_call(
        runtime: AppRuntime,
        args: Dict[str, Any],
        token: Optional[BzmToken],
        requires_session: bool,
        public: bool,
        explicit_session_id: Optional[str] = None,
) -> Union[BaseResult, _CallContext]:
    """
    Validate who is calling and in which session, or return the error to send back.

    Nothing reaches the request context unless it passed: the identity only after
    BlazeMeter accepted the token, the session only when it is ACTIVE, owned by
    that identity and used with the credential it was created with. Nested calls
    (help/skills batch re-entry) inherit the caller's validated context: a gated
    tool answers SESSION_INVALID to a nested session_id other than the inherited
    one; a public tool ignores it and keeps the inherited session.
    Public tools (static help/skills content) never block: without a valid token
    or session they run with no identity and no session, plus a warning.
    """
    # The declared top-level parameter wins; a session_id nested in `arguments`
    # (older clients) is still accepted. Never forwarded to the managers.
    nested_session_id = args.pop(SESSION_ID_ARG, None)
    requested = explicit_session_id if explicit_session_id is not None else nested_session_id

    inherited_identity = current_identity()
    if inherited_identity is not None:
        inherited_session = current_session()
        if requires_session and not public:
            if inherited_session is None:
                return _session_error(SessionErrorCode.REQUIRED)
            if requested is not None and requested != inherited_session.session_id:
                return _session_error(SessionErrorCode.INVALID)
        return _CallContext(inherited_identity, inherited_session, current_credential())

    credential = _credential(token)
    if public and requested is None:
        return _CallContext()

    try:
        identity = await runtime.identity.verify(token)
    except IdentityError as exc:
        if public:
            return _CallContext(warnings=[f"Running without a session: {exc.detail}"])
        return BaseResult(error=exc.detail, error_code=exc.code)

    if not requires_session and not public:
        return _CallContext(identity, None, credential)

    session = await _validate_session(runtime, requested, identity, credential)
    if isinstance(session, BaseResult):
        if public:
            return _CallContext(warnings=[f"Running without a session: {session.error}"])
        return session
    return _CallContext(identity, session, credential)


def register_managed_tool(
        mcp: Any,
        runtime: AppRuntime,
        *,
        name: str,
        dispatch: ToolDispatch,
        description: Optional[str] = None,
        actions: Optional[Sequence[ActionSpec]] = None,
        header: str = "",
        hints: Sequence[str] = (),
        excluded_actions: Optional[Set[str]] = None,
        disable_materialization: bool = False,
        support_message: Optional[str] = SUPPORT_MESSAGE,
        requires_session: bool = True,
        public: bool = False,
) -> Callable[..., Awaitable[BaseResult]]:
    """
    Shared MCP tool entrypoint: arguments= normalize → identity/session gate →
    configure_context → run_tool_with_runtime → @tool_result wrap.

    Pass either a literal ``description`` (legacy managers) or ``actions``
    (filtered by ``runtime.transport``). Catalog ``required_args`` are enforced
    here. ``dispatch`` owns action routing.
    Every tool requires a verified token and a valid ``session_id`` unless
    ``requires_session`` is False (the session tool itself) or ``public`` is True
    (static content: no API key needed, session optional). The session rule is
    appended to the description so agents learn it from the schema.
    Materialization stays inside ``run_tool_with_runtime`` so tracing includes persist.
    Returns the registered tool coroutine (needed for help/skills batch re-entry).
    """
    catalog_names: set[str] = set()
    visible_names: set[str] = set()
    visible: tuple[ActionSpec, ...] = ()
    if actions is not None:
        visible = filter_actions(runtime.transport, actions)
        description = render_description(header, visible, hints)
        catalog_names = {spec.name for spec in actions}
        visible_names = {spec.name for spec in visible}
    if not description:
        raise ValueError("register_managed_tool requires description= or actions=")
    if public:
        description = f"{description.rstrip()}\n{PUBLIC_SESSION_HINT}\n"
    elif requires_session:
        description = f"{description.rstrip()}\n{SESSION_HINT}\n"

    async def _handle(
            arguments: Optional[Dict[str, Any]],
            ctx: Optional[Context],
            session_id: Optional[str],
    ) -> BaseResult:
        action, args = normalize_action_args(arguments)
        if not action:
            return BaseResult(error="Missing required argument 'action' within tool arguments.")
        if action in catalog_names and action not in visible_names:
            return BaseResult(
                error=f"Action {action} is not available on {runtime.transport}."
            )
        spec = action_by_name(visible, action)
        if spec is not None and spec.required_args:
            if validation_error := validate_required_args(
                action, args, list(spec.required_args)
            ):
                return validation_error
        runtime.configure_context(ctx)
        token = runtime.auth.get_token(ctx)

        entered = await _enter_call(runtime, args, token, requires_session, public, session_id)
        if isinstance(entered, BaseResult):
            # TODO(telemetry): gate rejections (AUTH_*, SESSION_*) return before
            # run_tool_with_runtime, so they produce no span/metric. Record them
            # (span or counter by error_code) when auth/session observability matters.
            return entered

        async def _run() -> BaseResult:
            return await dispatch(action, args, token, ctx)

        with entered.binding():
            try:
                result = await run_tool_with_runtime(
                    runtime,
                    name,
                    action,
                    ctx,
                    _run,
                    tool_args=args,
                    dataframe_excluded_actions=excluded_actions,
                    disable_dataframe_materialization=disable_materialization,
                )
            except httpx.HTTPStatusError:
                return BaseResult(error=f"Error: {format_sanitized_traceback()}")
            except Exception:
                detail = format_sanitized_traceback()
                if support_message:
                    return BaseResult(error=f"Error: {detail}\n{support_message}")
                return BaseResult(error=f"Error: {detail}")
        if isinstance(result, BaseResult):
            if entered.warnings:
                result.append_warnings(entered.warnings)
            if not result.error and entered.session is not None:
                result.session_id = entered.session.session_id
        return result

    # The tool signature is the published input schema: expose session_id as a
    # parameter of its own so agents see it (required for session tools, optional
    # for public ones, absent on the session tool itself).
    if public:
        async def _tool(
                arguments: Dict[str, Any] = None,
                ctx: Context = None,
                session_id: PublicSessionIdParam = None,
        ) -> BaseResult:
            return await _handle(arguments, ctx, session_id)
    elif requires_session:
        async def _tool(
                arguments: Dict[str, Any] = None,
                ctx: Context = None,
                session_id: SessionIdParam = None,
        ) -> BaseResult:
            return await _handle(arguments, ctx, session_id)
    else:
        async def _tool(
                arguments: Dict[str, Any] = None,
                ctx: Context = None,
        ) -> BaseResult:
            return await _handle(arguments, ctx, None)

    registered = mcp.tool(name=name, description=description)(
        tool_result(excluded_actions=excluded_actions, disable_materialization=True)(_tool)
    )
    if requires_session and not public:
        _declare_session_id_required(mcp, name)
    return registered


def _declare_session_id_required(mcp: Any, name: str) -> None:
    """
    Publish ``session_id`` as a required string in the tool's input schema.

    The Python parameter keeps a default on purpose: a call without it reaches the
    gate, which answers SESSION_REQUIRED with the recovery guidance instead of a
    bare schema validation error.
    """
    if not isinstance(mcp, FastMCP):  # test doubles
        return
    # FastMCP has no public hook to edit a generated schema; if this private
    # path moves in an upgrade, fail at startup rather than publish a schema
    # where session_id looks optional.
    tool = mcp._tool_manager.get_tool(name)
    if tool is None or not isinstance(getattr(tool, "parameters", None), dict):
        raise RuntimeError(f"Cannot declare session_id as required on tool {name!r}.")
    tool.parameters.setdefault("properties", {})[SESSION_ID_ARG] = {
        "type": "string",
        "title": "Session Id",
        "description": SESSION_ID_DESCRIPTION,
    }
    required = tool.parameters.setdefault("required", [])
    if SESSION_ID_ARG not in required:
        required.append(SESSION_ID_ARG)
