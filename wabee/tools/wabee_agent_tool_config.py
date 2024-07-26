from typing import Any

from langchain.pydantic_v1 import BaseModel, Field
from langchain.schema.language_model import BaseLanguageModel

from wabee.tools.wabee_agent_tool_field_validator import (
    tool_field_validator,
)


class WabeeAgentToolConfig(BaseModel):
    llm: Any | None = Field(default=None, alias="_llm")

    @tool_field_validator("llm")
    def check_llm(cls, value: Any) -> Any:
        if value is None:
            return value
        if not isinstance(value, BaseLanguageModel):
            raise ValueError(
                "Provided llm does not implement the BaseLanguageModel interface"
            )
        return value
