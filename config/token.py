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

    def __init__(self, id: str, secret: str):
        if not id or not isinstance(id, str):
            raise BzmTokenError(f"Invalid ID: {id!r}")
        if not secret or not isinstance(secret, str):
            raise BzmTokenError(f"Invalid secret: {secret!r}")

        self.id = id
        self.secret = secret

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

        return cls(id=id_val, secret=secret_val)

    def as_basic_auth(self) -> str:
        """
        Returns the HTTP Basic Authentication header:
            "Basic <base64(id:secret)>"
        """
        combo = f"{self.id}:{self.secret}".encode("utf-8")
        token_b64 = base64.b64encode(combo).decode("utf-8")
        return f"Basic {token_b64}"

    def __repr__(self):
        return f"<BzmToken id={self.id!r} secret={'*'*8}>" 

