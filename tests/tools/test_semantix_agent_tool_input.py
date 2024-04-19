from semantix_agents.tools.semantix_agent_tool_input import SemantixAgentToolInput
from semantix_agents.tools.semantix_agent_tool_input_field import (
    SemantixAgentToolInputField,
)


class TestSemantixAgentToolInput:
    def test_should_return_the_input_props(self) -> None:
        class SemantixAgentToolInputChild2(SemantixAgentToolInput):
            x: float = SemantixAgentToolInputField(
                name="x", description="x description", example=0.5
            )

        class SemantixAgentToolInputChild(SemantixAgentToolInput):
            a: int = SemantixAgentToolInputField(
                name="a", description="a description", example=0
            )
            b: list[str] = SemantixAgentToolInputField(
                name="b", description="b description", example=["b"]
            )
            c: list[SemantixAgentToolInputChild2] = SemantixAgentToolInputField(
                name="c",
                description="c description",
                example=[SemantixAgentToolInputChild2.props()],
            )
            d: tuple[SemantixAgentToolInputChild2, SemantixAgentToolInputChild2] = (
                SemantixAgentToolInputField(
                    name="d",
                    description="d description",
                    example=(
                        SemantixAgentToolInputChild2.props(),
                        SemantixAgentToolInputChild2.props(),
                    ),
                )
            )
            e: dict[str, SemantixAgentToolInputChild2] = SemantixAgentToolInputField(
                name="e",
                description="e description",
                example={"key": SemantixAgentToolInputChild2.props()},
            )

        props = SemantixAgentToolInputChild.props()

        assert props == {
            "a": {
                "title": "a",
                "description": "a description",
                "example": 0,
                "type": "integer",
            },
            "b": {
                "title": "b",
                "description": "b description",
                "example": ["b"],
                "type": "array",
                "items": {"type": "string"},
            },
            "c": {
                "title": "c",
                "description": "c description",
                "example": [
                    {
                        "x": {
                            "title": "x",
                            "description": "x description",
                            "example": 0.5,
                            "type": "number",
                        }
                    }
                ],
                "type": "array",
                "items": {"$ref": "#/definitions/SemantixAgentToolInputChild2"},
            },
            "d": {
                "title": "d",
                "description": "d description",
                "example": (
                    {
                        "x": {
                            "title": "x",
                            "description": "x description",
                            "example": 0.5,
                            "type": "number",
                        }
                    },
                    {
                        "x": {
                            "title": "x",
                            "description": "x description",
                            "example": 0.5,
                            "type": "number",
                        }
                    },
                ),
                "type": "array",
                "minItems": 2,
                "maxItems": 2,
                "items": [
                    {"$ref": "#/definitions/SemantixAgentToolInputChild2"},
                    {"$ref": "#/definitions/SemantixAgentToolInputChild2"},
                ],
            },
            "e": {
                "title": "e",
                "description": "e description",
                "example": {
                    "key": {
                        "x": {
                            "title": "x",
                            "description": "x description",
                            "example": 0.5,
                            "type": "number",
                        }
                    }
                },
                "type": "object",
                "additionalProperties": {
                    "$ref": "#/definitions/SemantixAgentToolInputChild2"
                },
            },
        }
