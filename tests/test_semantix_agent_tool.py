import asyncio
import json
from typing import Type

from langchain_community.llms.fake import FakeListLLM

from semantix_agent_tools.semantix_agent_tool import SemantixAgentTool
from semantix_agent_tools.semantix_agent_tool_config import SemantixAgentToolConfig
from semantix_agent_tools.semantix_agent_tool_input import SemantixAgentToolInput


class TestSemantixAgentTool:
    def test_ensure_semantix_agent_tool_contains_name_and_description_and_llm_and_agrs_schema_by_default(
        self,
    ) -> None:
        fake_llm = FakeListLLM(responses=["any_response"])
        sut = SemantixAgentTool(
            name="any_name",
            description="any_description",
            llm=fake_llm,
            args_schema=SemantixAgentToolInput,
        )

        assert sut.name == "any_name"
        assert sut.description == "any_description"
        assert sut.llm == fake_llm
        assert sut.args_schema == SemantixAgentToolInput

    def test_ensure_semantix_agent_tool_allow_user_to_override_only_the_sync_execute_method(
        self,
    ) -> None:
        class SemantixAgentToolConfigChild(SemantixAgentToolConfig): ...

        class SemantixAgentToolInputChild(SemantixAgentToolInput):
            value: str

        class SemantixAgentToolChild(SemantixAgentTool):
            args_schema: Type[SemantixAgentToolInput] = SemantixAgentToolInputChild

            def execute(
                self,
                semantix_agent_tool_input: SemantixAgentToolInputChild,
            ) -> str:
                return "execute"

            @classmethod
            def create(
                cls,
                semantix_agent_tool_config: SemantixAgentToolConfigChild,
            ) -> SemantixAgentTool:
                return cls(
                    name="any_name",
                    description="any_description",
                    llm=semantix_agent_tool_config.llm,
                )

        async def get_tool_output():
            semantix_agent_tool_child = SemantixAgentToolChild.create(
                SemantixAgentToolConfigChild(
                    llm=FakeListLLM(responses=["any_response"]),
                )
            )
            output = await semantix_agent_tool_child.arun(
                json.dumps({"value": "any_value"})
            )
            return output

        assert asyncio.run(get_tool_output()) == "execute"

    def test_ensure_semantix_agent_tool_executes_with_typed_input(self) -> None:
        class SemantixAgentToolConfigChild(SemantixAgentToolConfig): ...

        class Y(SemantixAgentToolInput):
            a: str

        class Z(SemantixAgentToolInput):
            b: float

        class SemantixAgentToolInputChild(SemantixAgentToolInput):
            x: int
            y: Y
            z: list[Z]

        class SemantixAgentToolChild(SemantixAgentTool):
            args_schema: Type[SemantixAgentToolInput] = SemantixAgentToolInputChild

            def execute(
                self,
                semantix_agent_tool_input: SemantixAgentToolInputChild,
            ) -> str:
                return str(semantix_agent_tool_input)

            @classmethod
            def create(
                cls,
                semantix_agent_tool_config: SemantixAgentToolConfigChild,
            ) -> SemantixAgentTool:
                return cls(
                    name="any_name",
                    description="any_description",
                    llm=semantix_agent_tool_config.llm,
                )

        async def get_tool_output():
            semantix_agent_tool_child = SemantixAgentToolChild.create(
                SemantixAgentToolConfigChild(
                    llm=FakeListLLM(responses=["any_response"]),
                )
            )
            output = await semantix_agent_tool_child.arun(
                json.dumps({"x": 0, "y": {"a": "any_string"}, "z": [{"b": 0.5}]})
            )
            return output, semantix_agent_tool_child.args

        output, args = asyncio.run(get_tool_output())
        assert output == "x=0 y=Y(a='any_string') z=[Z(b=0.5)]"
        assert args == {
            "title": "SemantixAgentToolInputChild",
            "type": "object",
            "properties": {
                "x": {"title": "X", "type": "integer"},
                "y": {"$ref": "#/definitions/Y"},
                "z": {
                    "title": "Z",
                    "type": "array",
                    "items": {"$ref": "#/definitions/Z"},
                },
            },
            "required": ["x", "y", "z"],
            "definitions": {
                "Y": {
                    "title": "Y",
                    "type": "object",
                    "properties": {"a": {"title": "A", "type": "string"}},
                    "required": ["a"],
                },
                "Z": {
                    "title": "Z",
                    "type": "object",
                    "properties": {"b": {"title": "B", "type": "number"}},
                    "required": ["b"],
                },
            },
        }
