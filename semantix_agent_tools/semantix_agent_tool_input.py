from __future__ import annotations

from pydantic import BaseModel


class SemantixAgentToolInput(BaseModel):
    @classmethod
    def query_to_tool_input(cls, query: str) -> SemantixAgentToolInput:
        return cls.model_validate_json(query)
