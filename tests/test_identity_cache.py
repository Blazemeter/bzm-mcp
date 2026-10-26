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
import asyncio
from typing import Optional

from config.cache import InMemoryTTLCache, configure_cache
from config.identity import (
    BlazeMeterIdentityVerifier,
    CachedIdentityVerifier,
    Identity,
    IdentityPort,
    IdentityUnavailable,
    InvalidCredentials,
)
from config.token import BzmToken


class CountingIdentity(IdentityPort):
    """BlazeMeter stand-in: only ("key", "secret") is valid; can simulate an outage."""

    def __init__(self, delay: float = 0.0):
        self.calls = 0
        self.unavailable = False
        self.delay = delay

    async def verify(self, token: Optional[BzmToken]) -> Identity:
        self.calls += 1
        await asyncio.sleep(self.delay)
        if self.unavailable:
            raise IdentityUnavailable()
        if token is None or (token.id, token.secret) != ("key", "secret"):
            raise InvalidCredentials()
        return Identity(user_id="bzm-user")


class FakeClock:
    def __init__(self):
        self.now = 1000.0

    def __call__(self):
        return self.now


def _verify_many(verifier, tokens):
    async def scenario():
        results = []
        for token in tokens:
            try:
                results.append(await verifier.verify(token))
            except Exception as exc:
                results.append(exc)
        return results

    return asyncio.run(scenario())


def test_successful_check_is_reused_within_the_ttl():
    inner = CountingIdentity()
    results = _verify_many(CachedIdentityVerifier(inner, ttl_seconds=300), [BzmToken("key", "secret")] * 3)
    assert results == [Identity(user_id="bzm-user")] * 3
    assert inner.calls == 1


def test_check_runs_again_after_the_ttl():
    clock = FakeClock()
    configure_cache(InMemoryTTLCache(sweep_interval_seconds=0, clock=clock))
    inner = CountingIdentity()
    verifier = CachedIdentityVerifier(inner, ttl_seconds=300)
    _verify_many(verifier, [BzmToken("key", "secret")])
    clock.now += 301
    _verify_many(verifier, [BzmToken("key", "secret")])
    assert inner.calls == 2


def test_same_key_id_with_another_secret_is_checked_and_rejected():
    inner = CountingIdentity()
    verifier = CachedIdentityVerifier(inner, ttl_seconds=300)
    results = _verify_many(verifier, [BzmToken("key", "secret"), BzmToken("key", "forged")])
    assert results[0] == Identity(user_id="bzm-user")
    assert isinstance(results[1], InvalidCredentials)
    assert inner.calls == 2


def test_rejected_credentials_are_not_cached():
    inner = CountingIdentity()
    results = _verify_many(CachedIdentityVerifier(inner, ttl_seconds=300), [BzmToken("key", "bad")] * 2)
    assert all(isinstance(result, InvalidCredentials) for result in results)
    assert inner.calls == 2


def test_outage_is_not_cached():
    inner = CountingIdentity()
    inner.unavailable = True
    verifier = CachedIdentityVerifier(inner, ttl_seconds=300)
    first = _verify_many(verifier, [BzmToken("key", "secret")])
    inner.unavailable = False
    second = _verify_many(verifier, [BzmToken("key", "secret")])
    assert isinstance(first[0], IdentityUnavailable)
    assert second == [Identity(user_id="bzm-user")]
    assert inner.calls == 2


def test_missing_token_is_never_cached():
    inner = CountingIdentity()
    results = _verify_many(CachedIdentityVerifier(inner, ttl_seconds=300), [None, None])
    assert all(isinstance(result, InvalidCredentials) for result in results)
    assert inner.calls == 2


def test_concurrent_checks_of_one_credential_share_one_call():
    inner = CountingIdentity(delay=0.02)
    verifier = CachedIdentityVerifier(inner, ttl_seconds=300)

    async def scenario():
        return await asyncio.gather(*(verifier.verify(BzmToken("key", "secret")) for _ in range(5)))

    results = asyncio.run(scenario())
    assert results == [Identity(user_id="bzm-user")] * 5
    assert inner.calls == 1


def test_zero_ttl_checks_every_call():
    inner = CountingIdentity()
    _verify_many(CachedIdentityVerifier(inner, ttl_seconds=0), [BzmToken("key", "secret")] * 2)
    assert inner.calls == 2


def test_cache_key_never_contains_the_secret(isolated_cache):
    _verify_many(CachedIdentityVerifier(CountingIdentity(), ttl_seconds=300), [BzmToken("key", "secret")])
    keys = list(isolated_cache._data.keys())
    assert len(keys) == 1
    assert keys[0].startswith("global:identity:")
    assert "secret" not in keys[0]
    assert BzmToken("key", "secret").as_basic_auth().split()[-1] not in keys[0]


def test_runtime_reuses_identity_checks():
    from config.runtime import build_runtime

    identity = build_runtime("stdio").identity
    assert isinstance(identity, CachedIdentityVerifier)
    assert isinstance(identity._inner, BlazeMeterIdentityVerifier)
