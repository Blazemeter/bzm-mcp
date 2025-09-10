from typing import List, Any, Union

from models.workspace import WorkspaceDetailed, Workspace
from tools.utils import get_date_time_iso


def format_workspaces(workspaces: List[Any], detailed: bool = False) -> List[
    Union[WorkspaceDetailed, Workspace]]:
    normalized_workspaces = []
    for workspace in workspaces:

        workspace_element = {
            "workspace_id": workspace["id"],
            "workspace_name": workspace["name"],
            "account_id": workspace["accountId"],
            "created": get_date_time_iso(workspace["created"]),
            "updated": get_date_time_iso(workspace["updated"]),
            "enabled": workspace["enabled"],
        }
        if detailed:
            workspace_element.update({
                "owner": workspace["owner"],
                "allowance": workspace["allowance"],
                "users_count": workspace["membersCount"],
                "locations": workspace["locations"],
            })
        workspace_object = WorkspaceDetailed(**workspace_element) if detailed else Workspace(**workspace_element)
        normalized_workspaces.append(workspace_object)
    return normalized_workspaces


def format_workspaces_detailed(workspaces: List[Any]) -> List[
    Union[WorkspaceDetailed, Workspace]]:
    return format_workspaces(workspaces=workspaces, detailed=True)
