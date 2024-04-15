from __future__ import annotations
from asyncio import get_event_loop, AbstractEventLoop
from functools import partial
import json
import logging
from typing import Any, Awaitable

from semantix_agent_tools import SemantixAgentTool, SemantixAgentToolInput, SemantixAgentToolConfig

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
        return str(power_tool_input.base ** self.exponent)

    async def execute_async(self, query: str) -> Awaitable[str]:
        async def run(*args: Any, loop: AbstractEventLoop | None=None, executor: Any=None, **kwargs: Any):
            if loop is None:
                loop = get_event_loop()
            pfunc = partial(self.execute, *args, **kwargs)
            return await loop.run_in_executor(executor, pfunc)
        return await run(query)

    @classmethod
    def create(cls, power_tool_config: PowerToolConfig) -> PowerTool:
        return cls(name=power_tool_config.name, description=power_tool_config.description, exponent=power_tool_config.exponent)


def main() -> None:
    power_tool_config = {"name": "power_tool", "description": "tool that raises a number to the power of other number", "exponent": 2}
    power_tool = _create_tool(**power_tool_config)
    logging.info(f"Creating PowerTool with config: {power_tool_config}")

    power_tool_query = json.dumps({"base": 3})
    logging.info(f"Calling PowerTool with query: {power_tool_query}")

    power_tool_output = power_tool._run(power_tool_query)
    logging.info(f"PowerTool returned output: {power_tool_output}")
