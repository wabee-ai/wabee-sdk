from semantix_agents.tools.semantix_agent_tool_input_field import SemantixAgentToolInputField


class TestSemantixAgentToolInputField:
    def test_should_return_a_pydantic_field(self) -> None:
        field = SemantixAgentToolInputField(
            name="any_name", description="any_description", example="any_example"
        )

        assert field.title == "any_name"
        assert field.description == "any_description"
        assert field.extra["example"] == "any_example"
