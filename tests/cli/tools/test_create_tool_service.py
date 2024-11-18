import os
import sys
import pytest
import asyncio
from typing import AsyncGenerator, Dict, Any
import importlib.util
from pathlib import Path

from wabee.cli.tools.create_tool_service import CreateToolService, sanitize_name
from wabee.rpc.server import ToolServicer
from wabee.tools.tool_error import ToolError

def clean_folder(folder_name: str) -> None:
    """Remove all files in the given folder and the folder itself."""
    folder = Path(folder_name)
    if folder.exists():
        for path in folder.rglob('*'):
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                path.rmdir()
        folder.rmdir()

@pytest.fixture
async def tool_servicer(tmp_path: Path) -> AsyncGenerator[ToolServicer, None]:
    """Fixture to create a ToolServicer with dynamically loaded tools."""
    tools: Dict[str, Any] = {}
    servicer = ToolServicer(tools)
    yield servicer

class TestCreateToolService:
    def test_should_create_simple_tool(self, tmp_path: Path) -> None:
        """Test creation of a simple tool with function-based implementation."""
        sut = CreateToolService()
        
        # Create the tool
        sut.create_tool(
            name="my-test-tool",
            tool_type="simple",
            description="A test tool",
            version="0.1.0"
        )

        # Verify file creation
        assert Path("my_test_tool/my_test_tool_tool.py").exists()
        assert Path("my_test_tool/toolspec.yaml").exists()
        assert Path("my_test_tool/requirements.txt").exists()
        assert Path("my_test_tool/server.py").exists()

        # Verify tool content
        with open("my_test_tool/my_test_tool_tool.py", "r") as f:
            content = f.read()
            assert "class MyTestToolInput(BaseModel)" in content
            assert "@simple_tool(schema=MyTestToolInput)" in content
            assert "async def my_test_tool_tool(input_data: MyTestToolInput)" in content
            assert "message: str" in content

        clean_folder("my_test_tool")

    def test_should_create_complete_tool(self) -> None:
        """Test creation of a complete tool with class-based implementation."""
        sut = CreateToolService()
        
        sut.create_tool(
            name="complete-test-tool",
            tool_type="complete",
            description="A complete test tool",
            version="0.1.0"
        )

        # Verify file creation
        assert Path("complete_test_tool/complete_test_tool_tool.py").exists()
        assert Path("complete_test_tool/toolspec.yaml").exists()
        assert Path("complete_test_tool/requirements.txt").exists()
        assert Path("complete_test_tool/server.py").exists()

        # Verify tool content
        with open("complete_test_tool/complete_test_tool_tool.py", "r") as f:
            content = f.read()
            assert "class CompleteTestToolInput(BaseModel)" in content
            assert "class CompleteTestToolTool(BaseTool)" in content
            assert "async def execute(self, input_data: CompleteTestToolInput)" in content
            assert "@classmethod" in content
            assert "def create(cls, **kwargs)" in content

        clean_folder("complete_test_tool")

    def test_name_sanitization(self) -> None:
        """Test that tool names are properly sanitized."""
        assert sanitize_name("my tool") == "my_tool"
        assert sanitize_name("12345") == "tool_12345"
        assert sanitize_name("my-cool-tool!") == "my_cool_tool"
        assert sanitize_name("__init__") == "tool_init"

    @pytest.mark.asyncio
    async def test_simple_tool_execution(self, tool_servicer: ToolServicer) -> None:
        """Test that a generated simple tool can be executed via the server."""
        sut = CreateToolService()
        
        # Create the tool
        sut.create_tool(
            name="simple-exec-tool",
            tool_type="simple",
            description="A test tool",
            version="0.1.0"
        )

        # Add tool directory to Python path
        sys.path.append(str(Path.cwd()))
        
        # Import the generated tool
        spec = importlib.util.spec_from_file_location(
            "simple_exec_tool_tool",
            "simple_exec_tool/simple_exec_tool_tool.py"
        )
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Add tool to servicer
            servicer = await anext(tool_servicer)
            servicer.tools["simple_exec_tool"] = module.simple_exec_tool_tool

            # Execute tool
            result, error = await servicer._execute_tool(
                servicer.tools["simple_exec_tool"],
                {"message": "test"}
            )
            
            assert error is None
            assert "Processed: test" in result

        # Cleanup
        sys.path.remove(str(Path.cwd()))
        clean_folder("simple_exec_tool")

    @pytest.mark.asyncio
    async def test_complete_tool_execution(self, tool_servicer: ToolServicer) -> None:
        """Test that a generated complete tool can be executed via the server."""
        sut = CreateToolService()
        
        # Create the tool
        sut.create_tool(
            name="complete-exec-tool",
            tool_type="complete",
            description="A test tool",
            version="0.1.0"
        )

        # Add tool directory to Python path
        sys.path.append(str(Path.cwd()))
        
        # Import the generated tool
        spec = importlib.util.spec_from_file_location(
            "complete_exec_tool_tool",
            "complete_exec_tool/complete_exec_tool_tool.py"
        )
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Create tool instance and add to servicer
            tool_instance = module.CompleteExecToolTool.create()
            servicer = await anext(tool_servicer)
            servicer.tools["complete_exec_tool"] = tool_instance

            # Execute tool
            result, error = await servicer._execute_tool(
                servicer.tools["complete_exec_tool"],
                {"message": "test"}
            )
            
            assert error is None
            assert "Processed: test" in result

        # Cleanup
        sys.path.remove(str(Path.cwd()))
        clean_folder("complete_exec_tool")
