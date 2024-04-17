from typing import Any

from langchain.schema.language_model import BaseLanguageModel
from pydantic import BaseModel

from semantix_agent_tools.semantix_agent_tool_field_validator import (
    semantix_agent_tool_field_validator,
)


class SemantixAgentToolConfig(BaseModel):
    llm: Any

    @semantix_agent_tool_field_validator("llm")
    def check_llm(cls, value: Any) -> Any:
        if not isinstance(value, BaseLanguageModel):
            raise ValueError(
                "Provided llm does not implement the BaseLanguageModel interface"
            )
        return value
