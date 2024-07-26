import os

import pytest

from wabee.cli.tools.create_tool_service import CreateToolService


def clean_folder(folder_name: str) -> None:
    for file in os.listdir(folder_name):
        os.remove(os.path.join(folder_name, file))
    os.rmdir(folder_name)


class TestCreateToolService:
    def test_should_create_a_new_tool(self) -> None:
        sut = CreateToolService()

        tool_dir = sut.execute("my test-tool")

        assert tool_dir == "my_test_tool"
        assert os.path.isfile("my_test_tool/my_test_tool.py")
        assert os.path.isfile("my_test_tool/test_my_test_tool.py")
        assert os.path.isfile("my_test_tool/README.md")
        assert os.path.isfile("my_test_tool/CHANGES.txt")
        assert os.path.isfile("my_test_tool/__init__.py")

        with open("my_test_tool/my_test_tool.py", "r") as f:
            content = f.read()

            assert "class MyTestToolConfig(WabeeAgentToolConfig)" in content
            assert "class MyTestToolInput(WabeeAgentToolInput)" in content
            assert "class MyTestTool(WabeeAgentTool)" in content
            assert "def execute(self, my_test_tool_input: MyTestToolInput)"
            assert (
                "def create(cls, my_test_tool_config: MyTestToolConfig) -> MyTestTool"
            )
            assert "return MyTestTool.create(MyTestToolConfig(**kwargs))"

        with open("my_test_tool/test_my_test_tool.py", "r") as f:
            content = f.read()

            assert "class TestMyTestTool:" in content
            assert (
                "from my_test_tool.my_test_tool import _create_tool, MyTestToolInput"
                in content
            )

        clean_folder("my_test_tool")

    def test_should_not_create_a_duplicated_tool(self) -> None:
        sut = CreateToolService()

        sut.execute("duplicated-tool")

        with pytest.raises(ValueError):
            sut.execute("duplicated-tool")

        clean_folder("duplicated_tool")

    def test_should_not_create_a_tool_with_name_that_cannot_be_turned_into_a_python_module(
        self,
    ) -> None:
        sut = CreateToolService()

        with pytest.raises(ValueError):
            sut.execute("12345")
