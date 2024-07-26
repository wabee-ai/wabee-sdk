from wabee.tools.wabee_agent_tool_field import WabeeAgentToolField
from wabee.tools.wabee_agent_tool_input import WabeeAgentToolInput


class TestWabeeAgentToolInput:
    def test_should_return_the_input_props(self) -> None:
        class WabeeAgentToolInputChild2(WabeeAgentToolInput):
            x: float = WabeeAgentToolField(
                name="x", description="x description", example=0.5
            )

        class WabeeAgentToolInputChild(WabeeAgentToolInput):
            a: int = WabeeAgentToolField(
                name="a", description="a description", example=0
            )
            b: list[str] = WabeeAgentToolField(
                name="b", description="b description", example=["b"]
            )
            c: list[WabeeAgentToolInputChild2] = WabeeAgentToolField(
                name="c",
                description="c description",
                example=[WabeeAgentToolInputChild2.props()],
            )
            d: tuple[WabeeAgentToolInputChild2, WabeeAgentToolInputChild2] = (
                WabeeAgentToolField(
                    name="d",
                    description="d description",
                    example=(
                        WabeeAgentToolInputChild2.props(),
                        WabeeAgentToolInputChild2.props(),
                    ),
                )
            )
            e: dict[str, WabeeAgentToolInputChild2] = WabeeAgentToolField(
                name="e",
                description="e description",
                example={"key": WabeeAgentToolInputChild2.props()},
            )

        props = WabeeAgentToolInputChild.props()

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
                "items": {"$ref": "#/definitions/WabeeAgentToolInputChild2"},
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
                    {"$ref": "#/definitions/WabeeAgentToolInputChild2"},
                    {"$ref": "#/definitions/WabeeAgentToolInputChild2"},
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
                    "$ref": "#/definitions/WabeeAgentToolInputChild2"
                },
            },
        }
