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
Reused ``httpx.AsyncClient`` for the clients called on every tool call, so each
request reuses the connection instead of paying a new TCP/TLS (and HTTP/2)
handshake. Built on first use, rebuilt if closed, closed on server shutdown.

A shared client serves every caller (hosted: every user), so it never keeps
cookies: BlazeMeter answers with a ``bzm_sess`` session cookie, and a cookie
jar would send one user's session with the next user's requests.
"""
import weakref
from http.cookiejar import CookieJar, DefaultCookiePolicy
from typing import Callable, Optional

import httpx

_shared: "weakref.WeakSet[SharedAsyncClient]" = weakref.WeakSet()


class _NoCookies(DefaultCookiePolicy):
    def set_ok(self, cookie, request) -> bool:
        return False


class SharedAsyncClient:
    def __init__(self, factory: Callable[[], httpx.AsyncClient]) -> None:
        self._factory = factory
        self._client: Optional[httpx.AsyncClient] = None
        _shared.add(self)

    def get(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            client = self._factory()
            # A CookieJar is used as is; httpx.Cookies(...) would copy it into a default jar.
            client.cookies = CookieJar(policy=_NoCookies())
            self._client = client
        return self._client

    async def aclose(self) -> None:
        client, self._client = self._client, None
        if client is not None:
            await client.aclose()

    def discard(self) -> None:
        """Forget the client without closing it (its event loop is already gone)."""
        self._client = None


async def aclose_http_clients() -> None:
    """Close every shared client (server shutdown)."""
    for shared in list(_shared):
        await shared.aclose()


def discard_http_clients() -> None:
    """Forget every shared client; the next ``get()`` builds a new one."""
    for shared in list(_shared):
        shared.discard()
