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
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Literal

import httpx

logger = logging.getLogger(__name__)

DEV_MCP_CALLER_TOKEN = "dev-mcp-caller"
DEFAULT_UPLOAD_PUBLIC_BASE_URL = "http://127.0.0.1:8090"
DEFAULT_TICKET_TIMEOUT_SECONDS = 2.0


class TicketClientError(Exception):
    """Mapped storage-api failure for mint / credential writes."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


@dataclass(frozen=True)
class MintedTicket:
    id: str
    token: str
    redeem_deadline: str
    upload_deadline: str
    size_ceiling: int


class TicketPort(ABC):
    """storage-api mint / credential writer. HTTP runtime only."""

    public_base_url: str

    @abstractmethod
    async def put_credential(
        self, user_id: str, mcp_session_id: str, api_token: str
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def mint(
        self,
        user_id: str,
        mcp_session_id: str,
        test_id: int,
        filename: str,
        declared_size: int,
        encoding: str,
        sha256: str,
    ) -> MintedTicket:
        raise NotImplementedError

    def public_upload_url(self, ticket_id: str) -> str:
        return f"{self.public_base_url.rstrip('/')}/services/uploads/{ticket_id}"


class HttpTicketClient(TicketPort):
    def __init__(
        self,
        base_url: str,
        caller_token: str,
        public_base_url: str = DEFAULT_UPLOAD_PUBLIC_BASE_URL,
        timeout_seconds: float = DEFAULT_TICKET_TIMEOUT_SECONDS,
        http: httpx.AsyncClient | None = None,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._caller_token = caller_token
        self.public_base_url = public_base_url.rstrip("/")
        self._timeout = timeout_seconds
        self._http = http

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self._caller_token}"}

    async def _request(
        self, method: str, path: str, json: dict[str, Any]
    ) -> httpx.Response:
        url = f"{self._base_url}{path}"
        owns_client = self._http is None
        client = self._http or httpx.AsyncClient(timeout=self._timeout)
        try:
            response = await client.request(
                method, url, headers=self._headers(), json=json
            )
        except httpx.HTTPError as exc:
            logger.info(
                "storage-api %s %s unreachable: %s", method, path, type(exc).__name__
            )
            raise TicketClientError("Upload ticket service is unreachable.") from exc
        finally:
            if owns_client:
                await client.aclose()
        return response

    @staticmethod
    def _map_error(status_code: int, operation: str) -> TicketClientError:
        if status_code == 422:
            return TicketClientError(
                "Upload ticket fields were rejected (filename, encoding, sha256, or size).",
                status_code,
            )
        if status_code == 429:
            return TicketClientError("Upload ticket quota exceeded.", status_code)
        if status_code in {401, 403}:
            return TicketClientError(
                "Upload ticket service rejected the MCP caller identity.",
                status_code,
            )
        if status_code == 404:
            return TicketClientError(
                "Upload ticket service could not complete the request.",
                status_code,
            )
        return TicketClientError(
            f"Upload ticket {operation} failed.",
            status_code,
        )

    async def put_credential(
        self, user_id: str, mcp_session_id: str, api_token: str
    ) -> None:
        response = await self._request(
            "PUT",
            "/bzm-credentials",
            {
                "user_id": user_id,
                "mcp_session_id": mcp_session_id,
                "api_token": api_token,
            },
        )
        if response.status_code >= 400:
            logger.info("credential put status %s", response.status_code)
            raise self._map_error(response.status_code, "credential")

    async def mint(
        self,
        user_id: str,
        mcp_session_id: str,
        test_id: int,
        filename: str,
        declared_size: int,
        encoding: str,
        sha256: str,
    ) -> MintedTicket:
        response = await self._request(
            "POST",
            "/upload-tickets",
            {
                "user_id": user_id,
                "mcp_session_id": mcp_session_id,
                "test_id": test_id,
                "filename": filename,
                "declared_size": declared_size,
                "encoding": encoding,
                "sha256": sha256,
            },
        )
        if response.status_code >= 400:
            logger.info("mint status %s test %s", response.status_code, test_id)
            raise self._map_error(response.status_code, "mint")
        payload = response.json()
        ticket_id = str(payload["id"])
        logger.info("minted ticket %s test %s", ticket_id, test_id)
        return MintedTicket(
            id=ticket_id,
            token=str(payload["token"]),
            redeem_deadline=str(payload["redeem_deadline"]),
            upload_deadline=str(payload["upload_deadline"]),
            size_ceiling=int(payload["size_ceiling"]),
        )


def build_ticket_client(
    transport: Literal["stdio", "streamable-http"],
    storage_base_url: str | None = None,
) -> TicketPort | None:
    if transport != "streamable-http":
        return None
    base_url = (storage_base_url or os.getenv("BZM_STORAGE_API_BASE_URL", "")).strip()
    if not base_url:
        raise ValueError(
            "BZM_STORAGE_API_BASE_URL is required for streamable-http transport."
        )
    timeout_raw = os.getenv("BZM_MCP_TICKET_STORAGE_TIMEOUT_SECONDS", "")
    timeout_seconds = (
        float(timeout_raw) if timeout_raw.strip() else DEFAULT_TICKET_TIMEOUT_SECONDS
    )
    return HttpTicketClient(
        base_url=base_url,
        caller_token=os.getenv(
            "BZM_MCP_TICKET_STORAGE_CALLER_TOKEN", DEV_MCP_CALLER_TOKEN
        ).strip()
        or DEV_MCP_CALLER_TOKEN,
        public_base_url=os.getenv(
            "BZM_MCP_UPLOAD_PUBLIC_BASE_URL", DEFAULT_UPLOAD_PUBLIC_BASE_URL
        ).strip()
        or DEFAULT_UPLOAD_PUBLIC_BASE_URL,
        timeout_seconds=timeout_seconds,
    )
