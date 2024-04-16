from __future__ import annotations

from typing import Awaitable

from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.schema.language_model import BaseLanguageModel
from langchain.tools import BaseTool
from langchain_core.runnables.config import run_in_executor

from semantix_agent_tools.dates.date_handler import DateHandler
from semantix_agent_tools.exec.python_execution_handler import PythonExecutionHandler
from semantix_agent_tools.files.file_handler import FileHandler
from semantix_agent_tools.semantix_agent_tool_config import SemantixAgentToolConfig


class SemantixAgentTool(BaseTool):
    name: str
    description: str
    llm: BaseLanguageModel
    date_handler: DateHandler = DateHandler()
    file_handler: FileHandler = FileHandler()
    python_execution_handler: PythonExecutionHandler = PythonExecutionHandler()

    def execute(self, query: str) -> str:
        raise NotImplementedError("abstract method")

    async def execute_async(self, query: str) -> Awaitable[str]:
        raise NotImplementedError("abstract method")

    @classmethod
    def create(
        cls, semantix_agent_tool_config: SemantixAgentToolConfig
    ) -> SemantixAgentTool:
        raise NotImplementedError("abstract class method")

    def _run(
        self, query: str, run_manager: CallbackManagerForToolRun | None = None
    ) -> str:
        return self.execute(query)

    async def _arun(
        self, query: str, run_manager: CallbackManagerForToolRun | None = None
    ) -> Awaitable[str]:
        try:
            return await self.execute_async(query)
        except NotImplementedError:
            return await run_in_executor(None, self._run, query)  # type: ignore

    def __init_subclass__(cls) -> None:
        if not (
            hasattr(cls, "execute")
            and callable(cls.execute)
            and (
                cls.execute.__annotations__ == {"query": str, "return": str}
                or cls.execute.__annotations__ == {"query": "str", "return": "str"}
            )
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
