from wabee.tools.wabee_agent_tool_field import WabeeAgentToolField


class TestWabeeAgentToolField:
    def test_should_return_a_pydantic_field(self) -> None:
        field = WabeeAgentToolField(
            name="any_name", description="any_description", example="any_example", alias="_any_alias"
        )

        assert field.title == "any_name"
        assert field.description == "any_description"
        assert field.extra["example"] == "any_example"
        assert field.alias == "_any_alias"
