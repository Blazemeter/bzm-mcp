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
