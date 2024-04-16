from __future__ import annotations

from typing import Any, Awaitable

from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.tools import BaseTool


class SemantixAgentTool(BaseTool):
    name: str
    description: str

    def execute(self, query: str) -> str:
        raise NotImplementedError("abstract method")

    async def execute_async(self, query: str) -> Awaitable[str]:
        raise NotImplementedError("abstract method")

    @classmethod
    def create(cls, semantix_agent_tool_factory_input: Any) -> SemantixAgentTool:
        raise NotImplementedError("abstract class method")

    def _run(
        self, query: str, run_manager: CallbackManagerForToolRun | None = None
    ) -> str:
        return self.execute(query)

    async def _arun(
        self, query: str, run_manager: CallbackManagerForToolRun | None = None
    ) -> Awaitable[str]:
        return await self.execute_async(query)

    def __init_subclass__(cls) -> None:
        if not (
            hasattr(cls, "execute")
            and callable(cls.execute)
            and cls.execute.__annotations__ == {"query": "str", "return": "str"}
            and hasattr(cls, "execute_async")
            and callable(cls.execute_async)
            and cls.execute_async.__annotations__
            == {"query": "str", "return": "Awaitable[str]"}
            and hasattr(cls, "create")
            and callable(cls.create)
        ):
            raise NotImplementedError(
                f"{cls.__name__} does not correct implement the SemantixAgentTool interface"
            )
