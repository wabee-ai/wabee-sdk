from __future__ import annotations

import json
import logging
from typing import Any, Type

from langchain_community.llms.fake import FakeListLLM

from wabee.tools import (
    WabeeAgentTool,
    WabeeAgentToolConfig,
    WabeeAgentToolInput,
    WabeeAgentToolField,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s: \t  %(message)s")


class PowerToolConfig(WabeeAgentToolConfig):
    exponent: float


class PowerToolInput(WabeeAgentToolInput):
    base: float = WabeeAgentToolField(
        name="base", description="exponent base", example=2.0
    )


def _create_tool(**kwargs: Any) -> WabeeAgentTool:
    return PowerTool.create(PowerToolConfig(**kwargs))


class PowerTool(WabeeAgentTool):
    args_schema: Type[WabeeAgentToolInput] = PowerToolInput
    exponent: float

    def execute(self, power_tool_input: PowerToolInput) -> str:
        return str(power_tool_input.base**self.exponent)

    @classmethod
    def create(cls, power_tool_config: PowerToolConfig) -> PowerTool:
        return cls(
            name="power_tool",
            description="tool that raises a number to the power of other number",
            exponent=power_tool_config.exponent,
            llm=power_tool_config.llm,
        )


def main() -> None:
    power_tool_config = {
        "exponent": 2,
        "_llm": FakeListLLM(responses=["any_response"]),
    }
    power_tool = _create_tool(**power_tool_config)
    logging.info(f"Creating PowerTool with config: {power_tool_config}")

    logging.info("Displaying tool information:")
    print(f"name: {power_tool.name}")
    print(f"description: {power_tool.description}")
    print(f"args: {power_tool.args}")

    power_tool_query = json.dumps({"base": 3})
    logging.info(f"Calling PowerTool with query: {power_tool_query}")

    power_tool_output = power_tool.run(power_tool_query)
    logging.info(f"PowerTool returned output: {power_tool_output}")
