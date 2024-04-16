# from langchain.schema.language_model import BaseLanguageModel
from typing import Any

from pydantic import BaseModel


class SemantixAgentToolConfig(BaseModel):
    name: str
    description: str
    llm: Any
