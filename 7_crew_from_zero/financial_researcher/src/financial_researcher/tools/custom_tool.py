from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel
from datetime import datetime

class DateToolInput(BaseModel):
    """Input schema for DateTool."""
    pass

class DateTool(BaseTool):
    name: str = "DateTool"
    description: str = (
        "A tool to get the current date."
    )
    args_schema: Type[BaseModel] = DateToolInput

    def _run(self) -> str:
        return datetime.now().strftime("%Y-%m-%d")
