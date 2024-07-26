from __future__ import annotations


from typing import Any

from langchain.pydantic_v1 import BaseModel


class WabeeAgentToolInput(BaseModel):
    @classmethod
    def props(cls) -> dict[str, Any]:
        return cls.schema()["properties"]
