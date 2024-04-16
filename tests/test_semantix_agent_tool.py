import asyncio

import pytest
from langchain_community.llms.fake import FakeListLLM

from semantix_agent_tools.dates.date_handler import DateHandler
from semantix_agent_tools.files.file_handler import FileHandler
from semantix_agent_tools.semantix_agent_tool import SemantixAgentTool
from semantix_agent_tools.semantix_agent_tool_config import SemantixAgentToolConfig


class TestSemantixAgentTool:
    def test_ensure_semantix_agent_tool_contains_name_and_description_and_llm_and_handlers_by_default(
        self,
    ) -> None:
        fake_llm = FakeListLLM(responses=["any_response"])
        sut = SemantixAgentTool(
            name="any_name", description="any_description", llm=fake_llm
        )

        assert sut.name == "any_name"
        assert sut.description == "any_description"
        assert sut.llm == fake_llm
        assert isinstance(sut.date_handler, DateHandler)
        assert isinstance(sut.file_handler, FileHandler)

    def test_ensure_children_of_semantix_agent_tool_cannot_be_created_without_implement_the_parent_interface(
        self,
    ) -> None:
        with pytest.raises(Exception):

            class SemantixAgentToolChild(SemantixAgentTool):
                def execute(self, query: str) -> int:
                    return 0

    def test_ensure_semantix_agent_tool_allow_user_to_override_only_the_sync_execute_method(
        self,
    ) -> None:
        class SemantixAgentToolConfigChild(SemantixAgentToolConfig): ...

        class SemantixAgentToolChild(SemantixAgentTool):
            def execute(self, query: str) -> str:
                return "execute"

            @classmethod
            def create(
                cls, semantix_agent_tool_config: SemantixAgentToolConfigChild
            ) -> SemantixAgentTool:
                return cls(
                    name=semantix_agent_tool_config.name,
                    description=semantix_agent_tool_config.description,
                    llm=semantix_agent_tool_config.llm,
                )

        async def get_tool_output():
            semantix_agent_tool_child = SemantixAgentToolChild.create(
                SemantixAgentToolConfigChild(
                    name="any_name",
                    description="any_description",
                    llm=FakeListLLM(responses=["any_response"]),
                )
            )
            output = await semantix_agent_tool_child._arun("any_query")
            return output

        assert asyncio.run(get_tool_output()) == "execute"
