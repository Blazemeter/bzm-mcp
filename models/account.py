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
from typing import Optional

from pydantic import BaseModel, Field


class Account(BaseModel):
    account_id: int = Field("The unique identifier of the account")
    account_name: str = Field("The name of the account")
    description: str = Field("The description of the account")
    ai_consent: Optional[bool] = Field("The AI Consent")
    created: str = Field("The datetime that the account was created")
    updated: str = Field("The datetime that the account was updated")
