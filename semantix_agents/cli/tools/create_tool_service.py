import os
import re
from datetime import datetime

from langchain.pydantic_v1 import BaseModel, ValidationError, validator


class StringCases(BaseModel):
    original: str
    snake_case: str
    pascal_case: str

    @validator("original")
    def ensure_valid_python_module_can_be_created_from_tool_original_name(
        cls, value: str
    ) -> str:
        if not value.replace("_", "").replace("-", "").replace(" ", "").isalpha():
            raise ValueError(
                "Cannot create tool with this name! Try another one such as `my-tool`, `my tool` or `my_tool`"
            )
        return value


class CreateToolService:
    def execute(self, tool_name: str) -> str:
        try:
            tool_name_cases = StringCases(
                original=tool_name,
                snake_case=(
                    snake_case_tool_name := self.__convert_to_snake_case(tool_name)
                ),
                pascal_case=self.__convert_snake_case_to_pascal_case(
                    snake_case_tool_name
                ),
            )
        except ValidationError as e:
            raise ValueError(e.errors()[0]["msg"])

        try:
            os.mkdir(tool_name_cases.snake_case)
        except FileExistsError:
            raise ValueError(
                f"Its seems that a tool with name {tool_name_cases.snake_case} already exists in your current working directory!"
            )
        self.__create_tool_file(tool_name_cases)
        self.__create__init__file(tool_name_cases)
        self.__create_README_file(tool_name_cases)
        self.__create_test_tool_file(tool_name_cases)
        self.__create_changelog_file(tool_name_cases)

        return tool_name_cases.snake_case

    def __convert_to_snake_case(self, value: str) -> str:
        return "_".join(
            re.sub(
                "([A-Z][a-z]+)",
                r" \1",
                re.sub("([A-Z]+)", r" \1", value.replace("-", " ")),
            ).split()
        ).lower()

    def __convert_snake_case_to_pascal_case(self, value: str) -> str:
        return value.replace("_", " ").title().replace(" ", "")

    def __create_tool_file(self, tool_name_cases: StringCases) -> None:
        with open(
            f"{tool_name_cases.snake_case}/{tool_name_cases.snake_case}.py", "w"
        ) as f:
            f.write(f"""from __future__ import annotations

from typing import Any, Type

from semantix_agents.tools import (
    SemantixAgentTool,
    SemantixAgentToolConfig,
    SemantixAgentToolInput,
    SemantixAgentToolField,
    semantix_agent_tool_field_validator,
)


class {tool_name_cases.pascal_case}Config(SemantixAgentToolConfig):
    repeat: int

    @semantix_agent_tool_field_validator("repeat")
    def ensure_repeat_is_positive(cls, value: int) -> None:
        if value <= 0:
            raise ValueError("repeat must be greater than zero")
        return value


class {tool_name_cases.pascal_case}Input(SemantixAgentToolInput):
    text: str = SemantixAgentToolField(
        name="text", description="text to print", example="Hello, world!"
    )

    @semantix_agent_tool_field_validator("text")
    def ensure_text_has_length_smaller_than_100(cls, value: int) -> None:
        if len(value) > 100:
            raise ValueError("text should have at most 100 characters")
        return value


def _create_tool(**kwargs: Any) -> SemantixAgentTool:
    return {tool_name_cases.pascal_case}.create({tool_name_cases.pascal_case}Config(**kwargs))


class {tool_name_cases.pascal_case}(SemantixAgentTool):
    args_schema: Type[SemantixAgentToolInput] = {tool_name_cases.pascal_case}Input
    repeat: int

    def execute(self, {tool_name_cases.snake_case}_input: {tool_name_cases.pascal_case}Input) -> str:
        return {tool_name_cases.snake_case}_input.text * self.repeat

    @classmethod
    def create(cls, {tool_name_cases.snake_case}_config: {tool_name_cases.pascal_case}Config) -> {tool_name_cases.pascal_case}:
        return cls(
            name="{tool_name_cases.original}",
            description="tool description",
            llm={tool_name_cases.snake_case}_config.llm,
            repeat={tool_name_cases.snake_case}_config.repeat,
        )
""")

    def __create__init__file(self, tool_name_cases: StringCases) -> None:
        with open(f"{tool_name_cases.snake_case}/__init__.py", "w") as f:
            f.write("")

    def __create_README_file(self, tool_name_cases: StringCases) -> None:
        with open(f"{tool_name_cases.snake_case}/README.md", "w") as f:
            f.write(f"""# {tool_name_cases.original}

This is a template documentation file where you can add any revelavant information about the tool. It is highly recommended to change this file with your specifications to help others make use of your tool!

## Introduction

Use this section to answer the following questions one might have:

- What is this tool?
- What is the tool objective?
- What are its usecases?

## Examples

Give me some examples showing how to configure the tool, how to run it. For instace:

```python
from sum_tool.sum_tool import _create_tool, SumToolInput

tool = _create_tool()

output = tool.execute(SumTooInput(x=3, y=4))

print(output)
```

## Tests

Tell how to run the automatic tests for your tool, most python developers make use of pytest, therefore, it could be somehting like:

```sh
pytest -vv sum_tool/
```

Sometimes, there is necessary to build a test environment before running the test suite, this section can also be used to show to build or connect to such environment, for example, a testing database or an external api that your toool depends on.

## Tool Docs

This section serves to describe the tool configuration, input, output and the tool itself. You can use the format down below:

### class APIGatewayToolConfigure

#### Parameters

#### api_url (str)

base api url

#### api_key (str)

jwt api authorization key

### class APIGatewayToolInput

#### Parameters

##### method ('GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH')

request http method

##### path (str)

path to the request endpoint

##### body (map{{str, any}})

request body

##### headers (map{{str, any}})

request headers

##### params (map{{str, any}})

request parameters

### class APIGateway

#### Parameters

##### http_client (HTTPClient)

http client interface

#### Methods

##### execute

###### Inputs

- api_gateway_input (APIGatewayInput)

###### Outputs

- response staus code, i.e, 'status_code=200'

## References

Any resource used as reference to build this tool should be mentioned here, like academic papers, blog posts, books, and so on.
            """)

    def __create_test_tool_file(self, tool_name_cases: StringCases) -> None:
        with open(
            f"{tool_name_cases.snake_case}/test_{tool_name_cases.snake_case}.py", "w"
        ) as f:
            f.write(f"""from langchain_community.llms.fake import FakeListLLM

from {tool_name_cases.snake_case}.{tool_name_cases.snake_case} import _create_tool, {tool_name_cases.pascal_case}Input


class Test{tool_name_cases.pascal_case}:
    def test_should_return_correct_text(self) -> None:
        sut = _create_tool(**{{"_llm": FakeListLLM(responses=[""]), "repeat": 3}})

        output = sut.execute({tool_name_cases.pascal_case}Input(text="Hello, World!"))

        assert output == "Hello, World!Hello, World!Hello, World!"
        """)

    def __create_changelog_file(self, tool_name_cases: StringCases) -> None:
        with open(f"{tool_name_cases.snake_case}/CHANGES.txt", "w") as f:
            f.write(f"""Version 0.1.0
{datetime.now().strftime("%y-%m-%d")}
- Start tool implementation
            """)
