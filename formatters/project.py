from typing import List, Any, Optional

from models.project import Project
from tools.utils import get_date_time_iso


def format_projects(projects: List[Any], params: Optional[dict] = None) -> List[Project]:
    formatted_projects = []
    for project in projects:
        formatted_projects.append(
            Project(
                project_id=project.get("id"),
                project_name=project.get("name", "Unknown"),
                description=project.get("description", ""),
                created=get_date_time_iso(project.get("created")),
                updated=get_date_time_iso(project.get("updated")),
                workspace_id=project.get("workspaceId", 0),
                tests_count=project.get("testsCount", 0)
            )
        )
    return formatted_projects
