import json

import pytest

from wabee.tools.wabee_agent_tool_config import WabeeAgentToolConfig
from wabee.tools.wabee_agent_tool_field_validator import (
    tool_field_validator,
)
from wabee.tools.wabee_agent_tool_input import WabeeAgentToolInput


class TestWabeeAgentToolFieldValidator:
    def test_should_validate_agent_tool_fields_on_config(self) -> None:
        class WabeeAgentToolConfigChild(WabeeAgentToolConfig):
            x: int
            y: int

            @tool_field_validator("x", "y")
            def check_fields(cls, value: int) -> int:
                if value <= 0:
                    raise ValueError("Field cannot be smaller than zero!")
                return value

        with pytest.raises(Exception):
            WabeeAgentToolConfigChild(
                x=-1, y=0, name="any_name", description="any_description"
            )

    def test_should_validate_agent_tool_fields_on_input(self) -> None:
        class WabeeAgentToolInputChild(WabeeAgentToolInput):
            x: int

            @tool_field_validator("x")
            def check_fields(cls, value: int) -> int:
                if value <= 0:
                    raise ValueError("Field cannot be smaller than zero!")
                return value

        with pytest.raises(Exception):
            WabeeAgentToolInputChild.query_to_tool_input(json.dumps({"x": -1}))

        with pytest.raises(Exception):
            WabeeAgentToolInputChild.query_to_tool_input(json.dumps({"x": -1}))
