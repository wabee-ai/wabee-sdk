import json

import pytest

from semantix_agents.tools.semantix_agent_tool_config import SemantixAgentToolConfig
from semantix_agents.tools.semantix_agent_tool_field_validator import (
    semantix_agent_tool_field_validator,
)
from semantix_agents.tools.semantix_agent_tool_input import SemantixAgentToolInput


class TestSemantixAgentToolFieldValidator:
    def test_should_validate_agent_tool_fields_on_config(self) -> None:
        class SemantixAgentToolConfigChild(SemantixAgentToolConfig):
            x: int
            y: int

            @semantix_agent_tool_field_validator("x", "y")
            def check_fields(cls, value: int) -> int:
                if value <= 0:
                    raise ValueError("Field cannot be smaller than zero!")
                return value

        with pytest.raises(Exception):
            SemantixAgentToolConfigChild(
                x=-1, y=0, name="any_name", description="any_description"
            )

    def test_should_validate_agent_tool_fields_on_input(self) -> None:
        class SemantixAgentToolInputChild(SemantixAgentToolInput):
            x: int

            @semantix_agent_tool_field_validator("x")
            def check_fields(cls, value: int) -> int:
                if value <= 0:
                    raise ValueError("Field cannot be smaller than zero!")
                return value

        with pytest.raises(Exception):
            SemantixAgentToolInputChild.query_to_tool_input(json.dumps({"x": -1}))

        with pytest.raises(Exception):
            SemantixAgentToolInputChild.query_to_tool_input(json.dumps({"x": -1}))
