"""
Copyright 2025 Perforce Software, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    10|Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import annotations

import asyncio
import logging
import re
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from config.blazemeter import TESTS_ENDPOINT
from config.file_access import LOCAL_FILE_ACCESS_UNAVAILABLE_MESSAGE, FileAccessPort
from config.security import detect_sensitive_upload_path_reason
from config.storage import SessionScope, SessionScopeResolverPort
from config.tickets import TicketClientError, TicketPort
from config.token import BzmToken
from models.result import BaseResult
from tools.utils.common import api_request, format_sanitized_traceback

logger = logging.getLogger(__name__)

ReadTest = Callable[[int], Awaitable[BaseResult]]

_FILENAME_RE = re.compile(r"^[A-Za-z0-9_-]+\.[A-Za-z0-9]+$")
_SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
_ALLOWED_ENCODINGS = frozenset({"identity", "gzip"})
_FORBIDDEN_UPLOAD_KEYS = frozenset(
    {"file", "file_paths", "content", "bytes", "base64", "main_script"}
)
MAX_DECLARED_SIZE = 100 * 1024 * 1024

_MIME_TYPES = {
    ".jmx": "application/xml",
    ".yaml": "text/yaml",
    ".yml": "text/yaml",
    ".csv": "text/csv",
    ".zip": "application/zip",
    ".jar": "application/java-archive",
    ".properties": "text/plain",
    ".xml": "application/xml",
}
_SCRIPT_TYPES = {
    ".jmx": "jmeter",
    ".yaml": "taurus",
    ".yml": "taurus",
    ".py": "python",
    ".js": "javascript",
}


@dataclass(frozen=True)
class MintUploadRequest:
    test_id: int
    filename: str
    declared_size: int
    encoding: str
    sha256: str

    @classmethod
    def from_args(cls, args: dict[str, Any]) -> MintUploadRequest | BaseResult:
        forbidden = sorted(_FORBIDDEN_UPLOAD_KEYS.intersection(args))
        if forbidden:
            return BaseResult(
                error=(
                    "HTTP upload_assets does not accept file bytes, paths, or main_script. "
                    f"Remove: {', '.join(forbidden)}."
                )
            )

        test_id = args.get("test_id")
        filename = args.get("filename")
        declared_size = args.get("declared_size")
        encoding = args.get("encoding")
        sha256 = args.get("sha256")

        if not isinstance(test_id, int) or isinstance(test_id, bool) or test_id < 1:
            return BaseResult(
                error="Missing or invalid required argument 'test_id'. Expected integer."
            )
        if (
            not isinstance(filename, str)
            or not (3 <= len(filename) <= 255)
            or not _FILENAME_RE.fullmatch(filename)
        ):
            return BaseResult(
                error=(
                    "Invalid filename. Use ASCII letters, digits, underscore, hyphen, "
                    "and a required extension (length 3-255)."
                )
            )
        if (
            not isinstance(declared_size, int)
            or isinstance(declared_size, bool)
            or declared_size <= 0
        ):
            return BaseResult(
                error="Invalid declared_size. Expected an integer greater than 0."
            )
        if declared_size > MAX_DECLARED_SIZE:
            return BaseResult(error="Invalid declared_size. Hard ceiling is 100 MiB.")
        if encoding not in _ALLOWED_ENCODINGS:
            return BaseResult(error="Invalid encoding. Expected 'identity' or 'gzip'.")
        if not isinstance(sha256, str) or not _SHA256_RE.fullmatch(sha256):
            return BaseResult(error="Invalid sha256. Expected 64 hexadecimal characters.")

        return cls(
            test_id=test_id,
            filename=filename,
            declared_size=declared_size,
            encoding=encoding,
            sha256=sha256.lower(),
        )


class StdioAssetUploader:
    def __init__(
        self,
        file_access: FileAccessPort | None,
        scope_resolver: SessionScopeResolverPort | None,
    ) -> None:
        self._file_access = file_access
        self._scope_resolver = scope_resolver

    async def upload(
        self,
        token: BzmToken | None,
        ctx: Any,
        test_id: int | None,
        file_paths: list[str] | None,
        main_script: str | None,
        read_test: ReadTest,
    ) -> BaseResult:
        if not isinstance(test_id, int) or test_id < 1:
            return BaseResult(
                error="Missing or invalid required argument 'test_id'. Expected integer."
            )
        if not isinstance(file_paths, list) or not file_paths:
            return BaseResult(
                error="Missing or invalid required argument 'file_paths'. Expected non-empty list."
            )
        if self._file_access is None or self._scope_resolver is None:
            return BaseResult(error=LOCAL_FILE_ACCESS_UNAVAILABLE_MESSAGE)

        test_data = await read_test(test_id)
        if test_data.error:
            return BaseResult(error=test_data.error)

        scope = self._scope_resolver.resolve(ctx, token)
        mapped_file_paths = self._file_access.map_paths(file_paths, scope=scope)
        mapped_main_script = None
        if main_script:
            mapped_main_script_list = self._file_access.map_paths(
                [main_script], scope=scope
            )
            mapped_main_script = (
                mapped_main_script_list[0] if mapped_main_script_list else None
            )

        valid_files, invalid_files, blocked_files = self.classify_files(
            mapped_file_paths, scope
        )
        if not valid_files:
            return BaseResult(
                error="No valid files found to upload",
                result=[
                    {
                        "invalid_files": invalid_files,
                        "blocked_files": blocked_files,
                    }
                ],
            )

        upload_results = await asyncio.gather(
            *[
                self._upload_single_file(token, test_id, file_path, scope)
                for file_path in valid_files
            ],
            return_exceptions=True,
        )
        successful_uploads, failed_uploads = _collect_results(
            list(upload_results), valid_files
        )

        config_update_result = None
        if mapped_main_script and mapped_main_script in valid_files:
            config_update_result = await self._update_test_configuration(
                token, test_id, mapped_main_script
            )

        return BaseResult(
            result=[
                {
                    "test_id": test_id,
                    "successful_uploads": successful_uploads,
                    "failed_uploads": failed_uploads,
                    "invalid_files": invalid_files,
                    "blocked_files": blocked_files,
                    "config_update": config_update_result,
                }
            ]
        )

    def classify_files(
        self, file_paths: list[str], scope: SessionScope | None = None
    ) -> tuple[list[str], list[str], list[dict[str, str]]]:
        # Uploads are allowed from any user working location. Sensitive-origin
        # filtering is enforced by detect_sensitive_upload_path_reason().
        valid_files: list[str] = []
        invalid_files: list[str] = []
        blocked_files: list[dict[str, str]] = []
        file_access = self._file_access
        if file_access is None:
            return valid_files, file_paths[:], blocked_files
        for file_path in file_paths:
            sensitive_reason = detect_sensitive_upload_path_reason(file_path)
            if sensitive_reason:
                blocked_files.append({"file": file_path, "reason": sensitive_reason})
                continue
            if file_access.exists(file_path, scope=scope) and file_access.is_file(
                file_path, scope=scope
            ):
                valid_files.append(file_path)
            else:
                invalid_files.append(file_path)
        return valid_files, invalid_files, blocked_files

    async def _upload_single_file(
        self,
        token: BzmToken | None,
        test_id: int,
        file_path: str,
        scope: SessionScope,
    ) -> BaseResult:
        file_access = self._file_access
        assert file_access is not None
        try:
            file_name = Path(file_path).name
            file_content = file_access.read_bytes(file_path, scope=scope)
            files = {"file": (file_name, file_content, _mime_type(file_path))}
            return await api_request(
                token, "POST", f"{TESTS_ENDPOINT}/{test_id}/files", files=files
            )
        except Exception as exc:
            logger.error(
                "Failed to upload %s: %s", file_path, format_sanitized_traceback(exc)
            )
            raise Exception(f"Failed to upload {file_path}: {exc!s}") from exc

    async def _update_test_configuration(
        self, token: BzmToken | None, test_id: int, main_script_path: str
    ) -> BaseResult:
        try:
            file_name = Path(main_script_path).name
            return await api_request(
                token,
                "PATCH",
                f"{TESTS_ENDPOINT}/{test_id}",
                json={
                    "configuration": {
                        "filename": file_name,
                        "scriptType": _script_type(file_name),
                    }
                },
            )
        except Exception as exc:
            raise Exception(f"Failed to update test configuration: {exc!s}") from exc


class HttpAssetMinter:
    def __init__(
        self,
        tickets: TicketPort | None,
        scope_resolver: SessionScopeResolverPort | None,
    ) -> None:
        self._tickets = tickets
        self._scope_resolver = scope_resolver

    async def mint(
        self,
        token: BzmToken | None,
        ctx: Any,
        args: dict[str, Any],
        read_test: ReadTest,
    ) -> BaseResult:
        parsed = MintUploadRequest.from_args(args)
        if isinstance(parsed, BaseResult):
            return parsed
        if self._tickets is None or self._scope_resolver is None:
            return BaseResult(error="Upload tickets are not configured for this runtime.")
        if token is None:
            return BaseResult(error="Missing BlazeMeter credentials for this request.")

        test_data = await read_test(parsed.test_id)
        if test_data.error:
            return BaseResult(error=test_data.error)

        scope = self._scope_resolver.resolve(ctx, token)
        try:
            await self._tickets.put_credential(
                scope.user_id, scope.mcp_session_id, token.as_basic_auth()
            )
            minted = await self._tickets.mint(
                scope.user_id,
                scope.mcp_session_id,
                parsed.test_id,
                parsed.filename,
                parsed.declared_size,
                parsed.encoding,
                parsed.sha256,
            )
        except TicketClientError as exc:
            return BaseResult(error=str(exc))

        logger.info("minted upload ticket %s for test %s", minted.id, parsed.test_id)
        return BaseResult(
            result=[
                {
                    "method": "POST",
                    "url": self._tickets.public_upload_url(minted.id),
                    "authorization": f"Bearer {minted.token}",
                    "headers": {
                        "Authorization": f"Bearer {minted.token}",
                        "X-Upload-Filename": parsed.filename,
                        "X-Content-SHA256": parsed.sha256,
                        "Content-Encoding": parsed.encoding,
                    },
                    "size_ceiling": minted.size_ceiling,
                    "redeem_deadline": minted.redeem_deadline,
                    "upload_deadline": minted.upload_deadline,
                    "one_file_per_url": True,
                    "success_status": 201,
                    "test_id": parsed.test_id,
                    "filename": parsed.filename,
                }
            ]
        )


def _collect_results(
    upload_results: list[Any],
    valid_files: list[str],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    successful_uploads: list[dict[str, Any]] = []
    failed_uploads: list[dict[str, Any]] = []
    for i, result in enumerate(upload_results):
        if isinstance(result, Exception):
            failed_uploads.append({"file": valid_files[i], "error": str(result)})
        else:
            successful_uploads.append({"file": valid_files[i], "result": result})
    return successful_uploads, failed_uploads


def _mime_type(file_path: str) -> str:
    return _MIME_TYPES.get(Path(file_path).suffix.lower(), "application/octet-stream")


def _script_type(file_name: str) -> str:
    return _SCRIPT_TYPES.get(Path(file_name).suffix.lower(), "unknown")
