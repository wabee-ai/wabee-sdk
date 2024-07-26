from __future__ import annotations

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


class PrintToolConfig(WabeeAgentToolConfig): ...


class PrintToolInput(WabeeAgentToolInput):
    text: str = WabeeAgentToolField(
        name="text", description="text to print", example="Hello, world!"
    )


def _create_tool(**kwargs: Any) -> WabeeAgentTool:
    return PrintTool.create(PrintToolConfig(**kwargs))


class PrintTool(WabeeAgentTool):
    args_schema: Type[WabeeAgentToolInput] = PrintToolInput

    def execute(self, print_tool_input: PrintToolInput) -> str:
        return print_tool_input.text

    @classmethod
    def create(cls, Print_tool_config: PrintToolConfig) -> PrintTool:
        return cls(
            name="print_tool",
            description="tool that prints a text",
            llm=Print_tool_config.llm,
        )


def main() -> None:
    print_tool_config = {
        "_llm": FakeListLLM(responses=["any_response"]),
    }
    print_tool = _create_tool(**print_tool_config)
    logging.info(f"Creating PrintTool with config: {print_tool_config}")

    logging.info("Displaying tool information:")
    print(f"name: {print_tool.name}")
    print(f"description: {print_tool.description}")
    print(f"args: {print_tool.args}")

    print_tool_query = "invalid_text"
    logging.info(f"Calling PrintTool with query: {print_tool_query}")

    try:
        print_tool_output = print_tool.run(print_tool_query)
        logging.info(f"PrintTool returned output: {print_tool_output}")
    except TypeError as e:
        logging.error(f"PrintTool returned an error: {str(e)}")
