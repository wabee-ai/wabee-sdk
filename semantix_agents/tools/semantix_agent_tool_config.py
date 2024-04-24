from typing import Any

from langchain.pydantic_v1 import BaseModel, Field
from langchain.schema.language_model import BaseLanguageModel

from semantix_agents.tools.semantix_agent_tool_field_validator import (
    semantix_agent_tool_field_validator,
)


class SemantixAgentToolConfig(BaseModel):
    llm: Any | None = Field(default=None, alias="_llm")

    @semantix_agent_tool_field_validator("llm")
    def check_llm(cls, value: Any) -> Any:
        if value is None:
            return value
        if not isinstance(value, BaseLanguageModel):
            raise ValueError(
                "Provided llm does not implement the BaseLanguageModel interface"
            )
        return value
