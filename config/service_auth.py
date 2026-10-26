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
"""
How the MCP authenticates to the hosted services it calls.

Every request carries the MCP caller identity (a service token, as Bearer).
Session-scoped requests also carry the end-user credential the call runs with,
which the service checks against the session it was created with. Session,
partition and ticket clients share this contract instead of each building it.
"""
from typing import Optional

from config.env import env_str

# End-user credential of the current call (opaque; the service keeps only its HMAC).
CREDENTIAL_HEADER = "X-Bzm-Credential"


def service_caller_token() -> str:
    """MCP caller identity for the hosted services (BZM_MCP_STORAGE_CALLER_TOKEN, then the ticket one)."""
    return env_str("STORAGE_CALLER_TOKEN") or env_str("TICKET_STORAGE_CALLER_TOKEN")


def service_headers(caller_token: Optional[str], credential: Optional[str] = None) -> dict[str, str]:
    """Headers for a hosted-service request: caller identity, plus the end-user credential if any."""
    headers: dict[str, str] = {}
    if caller_token:
        headers["Authorization"] = f"Bearer {caller_token}"
    if credential:
        headers[CREDENTIAL_HEADER] = credential
    return headers
