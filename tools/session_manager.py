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
from config.runtime import AppRuntime
from config.session import SESSION_TOOL_NAME, SessionPort
from config.session_context import SessionContextMissing, current_credential, current_identity
from models.result import BaseResult
from tools.actions.session import ACTIONS, HEADER, HINTS
from tools.mcp_entrypoint import register_managed_tool


class SessionManager:
    """Opens chat sessions for the verified caller of the current tool call."""

    def __init__(self, sessions: SessionPort):
        self.sessions = sessions

    async def get(self) -> BaseResult:
        identity = current_identity()
        credential = current_credential()
        if identity is None or not credential:
            raise SessionContextMissing("The caller identity was not verified for this call.")
        session = await self.sessions.open(identity.user_id, credential)
        return BaseResult(
            result=[{
                "session_id": session.session_id,
                "state": session.state.value,
                "created_at": session.created_at.isoformat(),
            }],
            session_id=session.session_id,
            info=[
                "Keep this session_id in context and pass it as 'session_id' in every BlazeMeter "
                "tool call of this conversation. Do not call this tool again unless a tool returns "
                "SESSION_REQUIRED, SESSION_INVALID or SESSION_EXPIRED.",
            ],
        )


def register(mcp, runtime: AppRuntime):
    session_manager = SessionManager(runtime.sessions)

    async def _dispatch(action, args, token, ctx):
        match action:
            case "get":
                return await session_manager.get()
            case _:
                return BaseResult(error=f"Action {action} not found in session tool")

    register_managed_tool(
        mcp,
        runtime,
        name=SESSION_TOOL_NAME,
        actions=ACTIONS,
        header=HEADER,
        hints=HINTS,
        dispatch=_dispatch,
        # A new session id must never be materialized into a dataframe.
        disable_materialization=True,
        requires_session=False,
    )
