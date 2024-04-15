from asyncio import get_event_loop, AbstractEventLoop
from functools import partial
from typing import Any, Awaitable

from langchain.tools import BaseTool
from langchain.callbacks.manager import CallbackManagerForToolRun

class SemantixAgentTool(BaseTool):
    name: str
    description: str

    def _run(self, query: str, run_manager: CallbackManagerForToolRun | None = None) -> str:
        return "_run_output"

    async def _arun(self, query: str, run_manager: CallbackManagerForToolRun | None = None) -> Awaitable[str]:
        async def run(*args: Any, loop: AbstractEventLoop | None=None, executor: Any=None, **kwargs: Any):
            if loop is None:
                loop = get_event_loop()
            pfunc = partial(lambda : "_arun_output", *args, **kwargs)
            return await loop.run_in_executor(executor, pfunc)
        return await run(query)

class TestSemantixAgentTool:
    def test_ensure_semantix_agent_tool_contains_name_and_description_by_default(self) -> None:
        sut = SemantixAgentTool(name="any_name", description="any_description")

        assert sut.name == "any_name"
        assert sut.description == "any_description"
