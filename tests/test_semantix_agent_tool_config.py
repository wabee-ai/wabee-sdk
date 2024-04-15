from semantix_agent_tools.semantix_agent_tool_config import SemantixAgentToolConfig


class TestSemantixAgentToolConfig:
    def test_should_have_name_and_description_as_default_attributes(self) -> None:
        sut = SemantixAgentToolConfig(name="any_name", description="any_description")

        assert sut.name == "any_name"
        assert sut.description == "any_description"
