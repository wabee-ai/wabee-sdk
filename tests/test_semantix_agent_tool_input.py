from __future__ import annotations
import json

from semantix_agent_tools.semantix_agent_tool_input import SemantixAgentToolInput


class TestSemantixAgentToolInput:
    def test_its_children_class_should_be_able_to_parse_json_string_to_its_instance(self) -> None:

        class SemantixAgentToolInputChild(SemantixAgentToolInput):
            input_1: str
            input_2: Input2

            class Input2(SemantixAgentToolInput):
                input_2_1: int


        sut = SemantixAgentToolInputChild

        semantix_agent_tool_input = sut.query_to_tool_input(json.dumps({"input_1": "x", "input_2": {"input_2_1": 0}}))

        assert semantix_agent_tool_input.input_1 == "x"
        assert semantix_agent_tool_input.input_2.input_2_1 == 0
