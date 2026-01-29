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
