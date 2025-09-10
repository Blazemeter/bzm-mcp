from typing import List, Any

from tools.utils import get_date_time_iso


def format_projects(projects: List[Any]) -> List[Any]:
    formatted_projects = []
    for project in projects:
        formatted_project = {
            "project_id": project.get("id"),
            "project_name": project.get("name", "Unknown"),
            "description": project.get("description", ""),
            "created": get_date_time_iso(project.get("created")),
            "updated": get_date_time_iso(project.get("updated")),
            "workspace_id": project.get("workspaceId", 0),
            "tests_count": project.get("testsCount", 0)
        }
        formatted_projects.append(formatted_project)
    return formatted_projects
