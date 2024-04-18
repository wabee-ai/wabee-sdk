from __future__ import annotations

import json
import logging
from typing import Any, Type

from langchain_community.llms.fake import FakeListLLM

from semantix_agent_tools import (
    SemantixAgentTool,
    SemantixAgentToolConfig,
    SemantixAgentToolInput,
    SemantixAgentToolInputField,
    semantix_agent_tool_field_validator,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s: \t  %(message)s")


class DivisionToolConfig(SemantixAgentToolConfig): ...


class DivisionToolInput(SemantixAgentToolInput):
    a: float = SemantixAgentToolInputField(
        name="a", description="numerator", example=1.0
    )
    b: float = SemantixAgentToolInputField(
        name="b", description="denominator", example=2.0
    )

    @semantix_agent_tool_field_validator("b")
    def check_denominator(cls, value: float) -> float:
        if value == 0:
            raise ZeroDivisionError("denominator should be different than zero!")
        return value


def _create_tool(**kwargs: Any) -> SemantixAgentTool:
    return DivisionTool.create(DivisionToolConfig(**kwargs))


class DivisionTool(SemantixAgentTool):
    args_schema: Type[SemantixAgentToolInput] = DivisionToolInput

    def execute(self, division_tool_input: DivisionToolInput) -> str:
        return str(division_tool_input.a / division_tool_input.b)

    @classmethod
    def create(cls, division_tool_config: DivisionToolConfig) -> DivisionTool:
        return cls(
            name="division_tool",
            description="tool that divides two numbers",
            llm=division_tool_config.llm,
        )


def main() -> None:
    division_tool_config = {
        "llm": FakeListLLM(responses=["any_response"]),
    }
    division_tool = _create_tool(**division_tool_config)
    logging.info(f"Creating DivisionTool with config: {division_tool_config}")

    logging.info("Displaying tool information:")
    print(f"name: {division_tool.name}")
    print(f"description: {division_tool.description}")
    print(f"args: {division_tool.args}")

    division_tool_query = json.dumps({"a": 1, "b": 0})
    logging.info(f"Calling DivisionTool with query: {division_tool_query}")

    try:
        division_tool_output = division_tool._run(division_tool_query)
        logging.info(f"DivisionTool returned output: {division_tool_output}")
    except Exception as e:
        logging.error(f"DivisionTool returned an error: {str(e)}")
