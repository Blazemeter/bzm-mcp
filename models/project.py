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