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
