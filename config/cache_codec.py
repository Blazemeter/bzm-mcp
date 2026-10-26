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
JSON codec for values stored in a remote cache.

Cached results are typed (BaseResult holding Account/Workspace/Test models that
callers read as attributes) and some cached structures use non-string dict keys
(the help index), so plain JSON would change what a cache hit returns. Values
are encoded with small tagged wrappers and decoded back to the same types.

Only pydantic models from ``ALLOWED_MODEL_MODULES`` are rebuilt: the store never
decides which class gets instantiated.
"""
import importlib
from datetime import date, datetime
from typing import Any

from pydantic import BaseModel

ALLOWED_MODEL_MODULES = ("models.",)

_MODEL = "__model__"
_DICT = "__dict__"
_TUPLE = "__tuple__"
_SET = "__set__"
_DATETIME = "__datetime__"
_DATE = "__date__"
_RESERVED = frozenset({_MODEL, _DICT, _TUPLE, _SET, _DATETIME, _DATE})


class CacheCodecError(TypeError):
    """The value cannot be stored remotely (it is then simply not cached)."""


def _model_path(cls: type) -> str:
    return f"{cls.__module__}:{cls.__qualname__}"


def encode(value: Any) -> Any:
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, BaseModel):
        cls = type(value)
        if not cls.__module__.startswith(ALLOWED_MODEL_MODULES):
            raise CacheCodecError(f"Model {_model_path(cls)} is not allowed in the remote cache.")
        return {
            _MODEL: _model_path(cls),
            "fields": {name: encode(getattr(value, name)) for name in cls.model_fields},
            "set": sorted(value.model_fields_set),
        }
    if isinstance(value, datetime):
        return {_DATETIME: value.isoformat()}
    if isinstance(value, date):
        return {_DATE: value.isoformat()}
    if isinstance(value, dict):
        if all(isinstance(key, str) for key in value) and not (_RESERVED & value.keys()):
            return {key: encode(item) for key, item in value.items()}
        return {_DICT: [[encode(key), encode(item)] for key, item in value.items()]}
    if isinstance(value, list):
        return [encode(item) for item in value]
    if isinstance(value, tuple):
        return {_TUPLE: [encode(item) for item in value]}
    if isinstance(value, (set, frozenset)):
        return {_SET: [encode(item) for item in value]}
    raise CacheCodecError(f"Type {type(value).__name__} cannot be stored in the remote cache.")


def _load_model(path: str) -> type[BaseModel]:
    module_name, _, qualname = path.partition(":")
    if not module_name.startswith(ALLOWED_MODEL_MODULES) or not qualname:
        raise CacheCodecError(f"Model {path} is not allowed in the remote cache.")
    target: Any = importlib.import_module(module_name)
    for part in qualname.split("."):
        target = getattr(target, part)
    if not (isinstance(target, type) and issubclass(target, BaseModel)):
        raise CacheCodecError(f"{path} is not a model.")
    return target


def decode(value: Any) -> Any:
    if isinstance(value, list):
        return [decode(item) for item in value]
    if not isinstance(value, dict):
        return value
    if _MODEL in value:
        cls = _load_model(value[_MODEL])
        fields = {name: decode(item) for name, item in value.get("fields", {}).items()}
        # Built from a real instance's fields: restore them as they were.
        return cls.model_construct(_fields_set=set(value.get("set", fields)), **fields)
    if _DICT in value:
        return {_hashable(decode(key)): decode(item) for key, item in value[_DICT]}
    if _TUPLE in value:
        return tuple(decode(item) for item in value[_TUPLE])
    if _SET in value:
        return {_hashable(decode(item)) for item in value[_SET]}
    if _DATETIME in value:
        return datetime.fromisoformat(value[_DATETIME])
    if _DATE in value:
        return date.fromisoformat(value[_DATE])
    return {key: decode(item) for key, item in value.items()}


def _hashable(value: Any) -> Any:
    return tuple(_hashable(item) for item in value) if isinstance(value, list) else value
