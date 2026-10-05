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
"""Random id format shared by tasks, dataframes and chat sessions."""
import secrets

# Lowercase base32 without i, l, o, u: unambiguous when an agent reads it back.
SIMPLE_ID_ALPHABET = "0123456789abcdefghjkmnpqrstvwxyz"
SIMPLE_ID_LENGTH = 8


def random_id(length: int = SIMPLE_ID_LENGTH) -> str:
    return "".join(secrets.choice(SIMPLE_ID_ALPHABET) for _ in range(length))
