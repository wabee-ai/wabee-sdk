from semantix_agent_tools.semantix_agent_tool import SemantixAgentTool

class TestSemantixAgentTool:
    def test_ensure_semantix_agent_tool_contains_name_and_description_by_default(self) -> None:
        sut = SemantixAgentTool(name="any_name", description="any_description")

        assert sut.name == "any_name"
        assert sut.description == "any_description"
