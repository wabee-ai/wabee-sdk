from semantix_agents.tools.semantix_agent_tool_field import SemantixAgentToolField


class TestSemantixAgentToolField:
    def test_should_return_a_pydantic_field(self) -> None:
        field = SemantixAgentToolField(
            name="any_name", description="any_description", example="any_example", alias="_any_alias"
        )

        assert field.title == "any_name"
        assert field.description == "any_description"
        assert field.extra["example"] == "any_example"
        assert field.alias == "_any_alias"
