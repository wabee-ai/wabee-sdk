from __future__ import annotations

import json
from typing import Any, Awaitable, Callable, Type

from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.schema.language_model import BaseLanguageModel
from langchain.tools import BaseTool
from langchain_core.runnables.config import run_in_executor

from wabee.tools.wabee_agent_tool_input import WabeeAgentToolInput


def return_validation_error(e: Exception) -> str:
    return str(e)


class WabeeAgentTool(BaseTool):
    name: str
    description: str
    llm: BaseLanguageModel | None = None
    args_schema: Type[WabeeAgentToolInput]
    handle_validation_error: Callable[[Exception], str] = return_validation_error

    def execute(self, wabee_agent_tool_input: Any) -> str:
        raise NotImplementedError("abstract method")

    async def execute_async(self, wabee_agent_tool_input: Any) -> Awaitable[str]:
        raise NotImplementedError("abstract method")

    @classmethod
    def create(cls, wabee_agent_tool_config: Any) -> WabeeAgentTool:
        raise NotImplementedError("abstract class method")

    def _run(
        self,
        wabee_agent_tool_input: WabeeAgentToolInput,
        run_manager: CallbackManagerForToolRun | None = None,
    ) -> str:
        return self.execute(wabee_agent_tool_input)

    async def _arun(
        self,
        wabee_agent_tool_input: WabeeAgentToolInput,
        run_manager: CallbackManagerForToolRun | None = None,
    ) -> Awaitable[str]:
        try:
            return await self.execute_async(wabee_agent_tool_input)
        except NotImplementedError:
            return await run_in_executor(None, self._run, wabee_agent_tool_input)  # type: ignore

    def _parse_input(
        self,
        tool_input: str | dict[Any, Any],
    ) -> str | dict[str, Any]:
        try:
            if isinstance(tool_input, str):
                self.args_schema.validate(json.loads(tool_input))
                return tool_input

            self.args_schema.validate(tool_input)
            return tool_input
        except json.decoder.JSONDecodeError:
            raise TypeError("Input is not Json valid")

    def _to_args_and_kwargs(self, tool_input: str | dict) -> tuple[tuple, dict]:
        if isinstance(tool_input, str):
            return (self.args_schema.parse_raw(tool_input),), {}
        return (self.args_schema(**tool_input),), {}

    def __init_subclass__(cls) -> None:
        if not (
            hasattr(cls, "execute")
            and callable(cls.execute)
            and hasattr(cls, "execute_async")
            and callable(cls.execute_async)
            and hasattr(cls, "create")
            and callable(cls.create)
        ):
            raise NotImplementedError(
                f"{cls.__name__} does not correct implement the wabeeAgentTool interface"
            )

    def __str__(self):
        description = self.description.replace("\n", " ").replace("\t", " ")
        return f"{self.name}:{description}. For the input use this JSON schema: {self.args}"
