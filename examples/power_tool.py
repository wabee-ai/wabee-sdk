from __future__ import annotations

import json
import logging
from typing import Any

from langchain_community.llms.fake import FakeListLLM

from semantix_agent_tools import (
    SemantixAgentTool,
    SemantixAgentToolConfig,
    SemantixAgentToolInput,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s: \t  %(message)s")


class PowerToolConfig(SemantixAgentToolConfig):
    exponent: float


class PowerToolInput(SemantixAgentToolInput):
    base: float


def _create_tool(**kwargs: Any) -> SemantixAgentTool:
    return PowerTool.create(PowerToolConfig(**kwargs))


class PowerTool(SemantixAgentTool):
    exponent: float

    def execute(self, query: str) -> str:
        power_tool_input = PowerToolInput.query_to_tool_input(query)
        return str(power_tool_input.base**self.exponent)

    @classmethod
    def create(cls, power_tool_config: PowerToolConfig) -> PowerTool:
        return cls(
            name=power_tool_config.name,
            description=power_tool_config.description,
            exponent=power_tool_config.exponent,
        )


def main() -> None:
    power_tool_config = {
        "name": "power_tool",
        "description": "tool that raises a number to the power of other number",
        "exponent": 2,
        "llm": FakeListLLM(responses=["any_response"]),
    }
    power_tool = _create_tool(**power_tool_config)
    logging.info(f"Creating PowerTool with config: {power_tool_config}")

    power_tool_query = json.dumps({"base": 3})
    logging.info(f"Calling PowerTool with query: {power_tool_query}")

    power_tool_output = power_tool._run(power_tool_query)
    logging.info(f"PowerTool returned output: {power_tool_output}")
