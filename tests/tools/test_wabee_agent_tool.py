import asyncio
import json
from typing import Type

import pytest
from langchain_community.llms.fake import FakeListLLM

from wabee.tools.wabee_agent_tool import WabeeAgentTool
from wabee.tools.wabee_agent_tool_config import WabeeAgentToolConfig
from wabee.tools.wabee_agent_tool_input import WabeeAgentToolInput


class TestWabeeAgentTool:
    def test_ensure_wabee_agent_tool_contains_name_and_description_and_llm_and_agrs_schema_by_default(
        self,
    ) -> None:
        fake_llm = FakeListLLM(responses=["any_response"])
        sut = WabeeAgentTool(
            name="any_name",
            description="any_description",
            llm=fake_llm,
            args_schema=WabeeAgentToolInput,
        )

        assert sut.name == "any_name"
        assert sut.description == "any_description"
        assert sut.llm == fake_llm
        assert sut.args_schema == WabeeAgentToolInput

    def test_ensure_wabee_agent_tool_allow_user_to_override_only_the_sync_execute_method(
        self,
    ) -> None:
        class WabeeAgentToolConfigChild(WabeeAgentToolConfig): ...

        class WabeeAgentToolInputChild(WabeeAgentToolInput):
            value: str

        class WabeeAgentToolChild(WabeeAgentTool):
            args_schema: Type[WabeeAgentToolInput] = WabeeAgentToolInputChild

            def execute(
                self,
                wabee_agent_tool_input: WabeeAgentToolInputChild,
            ) -> str:
                return "execute"

            @classmethod
            def create(
                cls,
                wabee_agent_tool_config: WabeeAgentToolConfigChild,
            ) -> WabeeAgentTool:
                return cls(
                    name="any_name",
                    description="any_description",
                    llm=wabee_agent_tool_config.llm,
                )

        async def get_tool_output():
            wabee_agent_tool_child = WabeeAgentToolChild.create(
                WabeeAgentToolConfigChild(
                    _llm=FakeListLLM(responses=["any_response"]),
                )
            )
            output = await wabee_agent_tool_child.arun(
                json.dumps({"value": "any_value"})
            )
            return output

        assert asyncio.run(get_tool_output()) == "execute"

    def test_ensure_wabee_agent_tool_executes_with_typed_input(self) -> None:
        class WabeeAgentToolConfigChild(WabeeAgentToolConfig): ...

        class Y(WabeeAgentToolInput):
            a: str

        class Z(WabeeAgentToolInput):
            b: float

        class WabeeAgentToolInputChild(WabeeAgentToolInput):
            x: int
            y: Y
            z: list[Z]

        class WabeeAgentToolChild(WabeeAgentTool):
            args_schema: Type[WabeeAgentToolInput] = WabeeAgentToolInputChild

            def execute(
                self,
                wabee_agent_tool_input: WabeeAgentToolInputChild,
            ) -> str:
                return str(wabee_agent_tool_input)

            @classmethod
            def create(
                cls,
                wabee_agent_tool_config: WabeeAgentToolConfigChild,
            ) -> WabeeAgentTool:
                return cls(
                    name="any_name",
                    description="any_description",
                    llm=wabee_agent_tool_config.llm,
                )

        async def get_tool_output():
            wabee_agent_tool_child = WabeeAgentToolChild.create(
                WabeeAgentToolConfigChild(
                    _llm=FakeListLLM(responses=["any_response"]),
                )
            )
            output = await wabee_agent_tool_child.arun(
                json.dumps({"x": 0, "y": {"a": "any_string"}, "z": [{"b": 0.5}]})
            )
            return output, wabee_agent_tool_child.args

        output, args = asyncio.run(get_tool_output())
        assert output == "x=0 y=Y(a='any_string') z=[Z(b=0.5)]"
        assert args == {
            "x": {"title": "X", "type": "integer"},
            "y": {"$ref": "#/definitions/Y"},
            "z": {
                "title": "Z",
                "type": "array",
                "items": {"$ref": "#/definitions/Z"},
            },
        }

    def test_wabee_agent_tool_raises_if_input_cannot_be_parsed_as_json(self) -> None:
        class WabeeAgentToolConfigChild(WabeeAgentToolConfig): ...

        class WabeeAgentToolInputChild(WabeeAgentToolInput):
            value: str

        class WabeeAgentToolChild(WabeeAgentTool):
            args_schema: Type[WabeeAgentToolInput] = WabeeAgentToolInputChild

            def execute(
                self,
                wabee_agent_tool_input: WabeeAgentToolInputChild,
            ) -> str:
                return "execute"

            @classmethod
            def create(
                cls,
                wabee_agent_tool_config: WabeeAgentToolConfigChild,
            ) -> WabeeAgentTool:
                return cls(
                    name="any_name",
                    description="any_description",
                    llm=wabee_agent_tool_config.llm,
                )

        wabee_agent_tool_child = WabeeAgentToolChild.create(
            WabeeAgentToolConfigChild(
                _llm=FakeListLLM(responses=["any_response"]),
            )
        )

        with pytest.raises(TypeError):
            wabee_agent_tool_child.run("invalid_input")

    def test_wabee_agent_tool_returns_error_message_if_input_cannot_be_parsed_as_json(
        self,
    ) -> None:
        class WabeeAgentToolConfigChild(WabeeAgentToolConfig): ...

        class WabeeAgentToolInputChild(WabeeAgentToolInput):
            value: str

        class WabeeAgentToolChild(WabeeAgentTool):
            args_schema: Type[WabeeAgentToolInput] = WabeeAgentToolInputChild

            def execute(
                self,
                wabee_agent_tool_input: WabeeAgentToolInputChild,
            ) -> str:
                return "execute"

            @classmethod
            def create(
                cls,
                wabee_agent_tool_config: WabeeAgentToolConfigChild,
            ) -> WabeeAgentTool:
                return cls(
                    name="any_name",
                    description="any_description",
                    llm=wabee_agent_tool_config.llm,
                )

        wabee_agent_tool_child = WabeeAgentToolChild.create(
            WabeeAgentToolConfigChild(
                _llm=FakeListLLM(responses=["any_response"]),
            )
        )

        assert (
            "field required (type=value_error.missing)"
            in wabee_agent_tool_child.run(json.dumps({"input": "invalid_input"}))
        )
