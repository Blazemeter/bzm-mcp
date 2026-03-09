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

import pytest

from config.token import BzmToken, BzmTokenError


class TestTokenErrorSanitization:
    def test_invalid_token_id_error_does_not_include_token_value(self):
        leaked_token_id = {"token_id": "my-super-secret-token-id"}
        with pytest.raises(BzmTokenError) as exc_info:
            BzmToken(leaked_token_id, "safe-secret")

        message = str(exc_info.value)
        assert "Invalid Token ID format" in message
        assert "my-super-secret-token-id" not in message

    def test_invalid_token_secret_error_does_not_include_secret_value(self):
        leaked_token_secret = {"secret": "my-super-secret-token-value"}
        with pytest.raises(BzmTokenError) as exc_info:
            BzmToken("safe-id", leaked_token_secret)

        message = str(exc_info.value)
        assert "Invalid Token secret format" in message
        assert "my-super-secret-token-value" not in message

    def test_repr_does_not_expose_token_id_or_secret(self):
        token = BzmToken("my-token-id", "my-token-secret")

        token_repr = repr(token)
        assert "my-token-id" not in token_repr
        assert "my-token-secret" not in token_repr
        assert token_repr == "<BzmToken id=******** secret=********>"
