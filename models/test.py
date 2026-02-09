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
from typing import Optional, Dict, Any, List

from pydantic import BaseModel, Field


class Test(BaseModel):
    """Test basic information structure."""
    test_id: int = Field(description="The unique identifier for the test. Also known as a testId")
    test_name: str = Field(description="The test name")
    description: str = Field(description="A description of the test")
    created: Optional[str] = Field(description="The datetime that the test was created.", default=None)
    updated: Optional[str] = Field(description="The datetime that the test was updated", default=None)
    project_id: int = Field(description="The Project ID")
    configuration: Dict[str, Any] = Field(description="Contains all the advanced BlazeMeter related configurations")
    override_executions: List[Optional[Any]] = Field(description="The test settings used when running the test in BlazeMeter")
