from typing import Optional

from pydantic import Field

from models.result import BaseResult


class Project(BaseResult):
    project_id: int = Field("The unique identifier of the project")
    project_name: str = Field("The name of the project")
    description: Optional[str] = Field("The description of the project")
    created: str = Field("The date time when the project was created")
    updated: str = Field("The date time when the project was updated")
    workspace_id: int = Field("The unique identifier of the workspace")
    tests_count: int = Field("The amount of tests on the project")