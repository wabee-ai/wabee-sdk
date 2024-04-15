from __future__ import annotations
from asyncio import get_event_loop, AbstractEventLoop
from functools import partial
import json
import logging
from typing import Any, Awaitable

from semantix_agent_tools import (
    SemantixAgentTool,
    SemantixAgentToolInput,
    SemantixAgentToolConfig,
    semantix_agent_tool_field_validator
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s: \t  %(message)s")


class DivisionToolConfig(SemantixAgentToolConfig):
    ...

class DivisionToolInput(SemantixAgentToolInput):
    a: float
    b: float

    @semantix_agent_tool_field_validator("b")
    def check_denominator(cls, value: float) -> float:
        if value == 0:
            raise ZeroDivisionError("denominator should be different than zero!")
        return value


def _create_tool(**kwargs: Any) -> SemantixAgentTool:
    return DivisionTool.create(DivisionToolConfig(**kwargs))


class DivisionTool(SemantixAgentTool):
    def execute(self, query: str) -> str:
        division_tool_input = DivisionToolInput.query_to_tool_input(query)
        return str(division_tool_input.a / division_tool_input.b)

    async def execute_async(self, query: str) -> Awaitable[str]:
        async def run(*args: Any, loop: AbstractEventLoop | None=None, executor: Any=None, **kwargs: Any):
            if loop is None:
                loop = get_event_loop()
            pfunc = partial(self.execute, *args, **kwargs)
            return await loop.run_in_executor(executor, pfunc)
        return await run(query)

    @classmethod
    def create(cls, division_tool_config: DivisionToolConfig) -> DivisionTool:
        return cls(name=division_tool_config.name, description=division_tool_config.description)


def main() -> None:
    division_tool_config = {"name": "division_tool", "description": "tool that divides two numbers"}
    division_tool = _create_tool(**division_tool_config)
    logging.info(f"Creating DivisionTool with config: {division_tool_config}")

    division_tool_query = json.dumps({"a": 1, "b": 0})
    logging.info(f"Calling DivisionTool with query: {division_tool_query}")

    try:
        division_tool_output = division_tool._run(division_tool_query)
        logging.info(f"DivisionTool returned output: {division_tool_output}")
    except Exception as e:
        logging.error(f"DivisionTool returned an error: {str(e)}")
