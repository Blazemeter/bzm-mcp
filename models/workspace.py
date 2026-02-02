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
from typing import Optional, Dict, List, Any

from pydantic import Field, BaseModel


class Workspace(BaseModel):
    """Workspace basic information structure."""
    workspace_id: int = Field(description="The unique identifier for the workspace. Also known as a workspaceId")
    workspace_name: str = Field(description="The name of this workspace")
    account_id: int = Field(description="The account id of this workspace")
    created: Optional[str] = Field(description="The datetime for when the workspace was created", default=None)
    updated: Optional[str] = Field(description="The datetime for when the workspace was updated", default=None)
    enabled: bool = Field(description="Denotes if the workspace is enabled or not")


class WorkspaceDetailed(Workspace):
    """Workspace detailed information structure."""
    owner: Dict[str, Any] = Field(description="The details of the owner of the workspace")
    allowance: Dict[str, Any] = Field(description="The available billing usage details")
    users_count: int = Field(description="The number of users in the workspace")
    test_available_locations: Dict[str, Any] = Field(description="The location details available for test in the workspace")
