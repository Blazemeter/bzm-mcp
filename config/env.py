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
from typing import Optional

logger = logging.getLogger(__name__)

# TODO(env): CACHE_METHOD adds its own env parsing (config/cache.py _env_bool/_env_number,
# full BZM_CACHE_* names). When both branches land in STREAMABLE_HTTP, move it onto
# these helpers so there is a single parser (prefix, defaults, invalid-value policy).
# Tunables read from the environment use this prefix (e.g. BZM_MCP_MAX_PARALLEL_TASKS).
ENV_PREFIX = "BZM_MCP_"


def _raw(name: str) -> Optional[str]:
    value = os.getenv(f"{ENV_PREFIX}{name}")
    if value is None or not value.strip():
        return None
    return value.strip()


def env_str(name: str, default: str = "") -> str:
    """``BZM_MCP_<name>`` as a string, or ``default`` when unset or blank."""
    value = _raw(name)
    return default if value is None else value


def env_int(name: str, default: int, *, minimum: Optional[int] = None) -> int:
    """``BZM_MCP_<name>`` as an int; invalid or below ``minimum`` falls back to ``default``."""
    value = _raw(name)
    if value is None:
        return default
    try:
        parsed = int(value)
    except ValueError:
        logger.warning("Invalid %s%s=%r; using default %s", ENV_PREFIX, name, value, default)
        return default
    if minimum is not None and parsed < minimum:
        logger.warning("%s%s=%s is below %s; using default %s", ENV_PREFIX, name, parsed, minimum, default)
        return default
    return parsed


def env_float(name: str, default: float, *, minimum: Optional[float] = None) -> float:
    """``BZM_MCP_<name>`` as a float; invalid or below ``minimum`` falls back to ``default``."""
    value = _raw(name)
    if value is None:
        return default
    try:
        parsed = float(value)
    except ValueError:
        logger.warning("Invalid %s%s=%r; using default %s", ENV_PREFIX, name, value, default)
        return default
    if minimum is not None and parsed < minimum:
        logger.warning("%s%s=%s is below %s; using default %s", ENV_PREFIX, name, parsed, minimum, default)
        return default
    return parsed
