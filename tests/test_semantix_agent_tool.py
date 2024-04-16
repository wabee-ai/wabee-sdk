import pytest

from semantix_agent_tools.semantix_agent_tool import SemantixAgentTool


class TestSemantixAgentTool:
    def test_ensure_semantix_agent_tool_contains_name_and_description_by_default(
        self,
    ) -> None:
        sut = SemantixAgentTool(name="any_name", description="any_description")

        assert sut.name == "any_name"
        assert sut.description == "any_description"
        assert sut.description == "any_description"

    def test_ensure_children_of_semantix_agent_tool_cannot_be_created_without_implement_the_parent_interface(
        self,
    ) -> None:
        with pytest.raises(Exception):

            class SemantixAgentToolChild(SemantixAgentTool):
                def execute(self, query: str) -> int:
                    return 0
