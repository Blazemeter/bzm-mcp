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
import json
import base64
from pathlib import Path
from typing import Union
from functools import lru_cache


class BzmTokenError(Exception):
    """Error when constructing or loading BzmToken."""
    pass


class BzmToken:
    __slots__ = ("id", "secret")

    def __init__(self, token_id: str, token_secret: str):
        if not token_id or not isinstance(token_id, str):
            raise BzmTokenError("Invalid Token ID format: expected non-empty string")
        if not token_secret or not isinstance(token_secret, str):
            raise BzmTokenError("Invalid Token secret format: expected non-empty string")

        self.id = token_id
        self.secret = token_secret

    @classmethod
    @lru_cache(maxsize=1)
    def from_file(cls, path: Union[str, Path]) -> "BzmToken":
        p = Path(path)
        if not p.exists() or not p.is_file():
            raise BzmTokenError(f"File does not exist: {p!r}")

        try:
            raw = p.read_text(encoding="utf-8")
            data = json.loads(raw)
        except Exception as e:
            raise BzmTokenError(f"Error reading/parsing JSON from {p!r}: {e}") from e

        try:
            id_val = data["id"]
            secret_val = data["secret"]
        except KeyError as e:
            raise BzmTokenError(f"Missing field {e.args[0]!r} in {p!r}") from e

        return cls(token_id=id_val, token_secret=secret_val)

    @classmethod
    def from_bearer_credentials(cls, credentials: str) -> "BzmToken":
        """
        Parse Bearer credential material into a BzmToken.

        Accepts plaintext ``id:secret`` or base64-encoded ``id:secret``.
        Does not call the BlazeMeter API.
        """
        raw = (credentials or "").strip()
        if not raw:
            raise BzmTokenError("Empty bearer credentials")

        # Plaintext id:secret (base64 alphabet has no ':')
        if ":" in raw:
            token_id, _, token_secret = raw.partition(":")
            return cls(token_id=token_id, token_secret=token_secret)

        try:
            pad = "=" * (-len(raw) % 4)
            decoded = base64.b64decode(raw + pad, validate=False).decode("utf-8")
        except Exception as e:
            raise BzmTokenError("Invalid bearer credentials encoding") from e

        if ":" not in decoded:
            raise BzmTokenError("Invalid bearer credentials format")

        token_id, _, token_secret = decoded.partition(":")
        return cls(token_id=token_id, token_secret=token_secret)

    def as_basic_auth(self) -> str:
        """
        Returns the HTTP Basic Authentication header:
            "Basic <base64(id:secret)>"
        """
        combo = f"{self.id}:{self.secret}".encode("utf-8")
        token_b64 = base64.b64encode(combo).decode("utf-8")
        return f"Basic {token_b64}"

    def __repr__(self):
        return "<BzmToken id=******** secret=********>"

