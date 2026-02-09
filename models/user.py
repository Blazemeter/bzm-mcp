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
from pydantic import BaseModel, Field


class User(BaseModel):
    user_id: int = Field(description="The unique identifier for the user. Also known as a userId")
    display_name: str = Field(description="Display name of the user")
    first_name: str = Field(description="First name of the user")
    last_name: str = Field(description="Last name of the user")
    email: str = Field(description="Email of the user")
    access: str = Field(description="Last access to the user")
    login: str = Field(description="Last login of the user")
    created: str = Field(description="Datetime that the user was created.")
    updated: str = Field(description="Datetime that the user was updated.")
    time_zone: int = Field(description="Time zone of the user")
    enabled: bool = Field(description="If the user is enabled")
    default_project_id: int = Field(description="Default project id of the user")
