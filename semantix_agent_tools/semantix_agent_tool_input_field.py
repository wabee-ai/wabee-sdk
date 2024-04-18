from typing import Any

from langchain.pydantic_v1 import Field


def SemantixAgentToolInputField(name: str, description: str, example: Any) -> Any:
    return Field(title=name, description=description, example=example)
