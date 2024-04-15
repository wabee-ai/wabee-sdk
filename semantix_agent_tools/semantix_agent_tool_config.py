from pydantic import BaseModel


class SemantixAgentToolConfig(BaseModel):
    name: str
    description: str
