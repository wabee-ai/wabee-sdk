from typing import Any

from langchain.pydantic_v1 import Field


def SemantixAgentToolField(name: str, description: str, example: Any, alias: str | None = None) -> Any:
    return Field(title=name, description=description, example=example, alias=alias)
