![PyPI - Downloads](https://img.shields.io/pypi/dm/wabee)
![PyPI - Format](https://img.shields.io/pypi/format/wabee)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/wabee)
![PyPI - License](https://img.shields.io/pypi/l/wabee)
![PyPI - Status](https://img.shields.io/pypi/status/wabee)
![PyPI - Version](https://img.shields.io/pypi/v/wabee)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/wabee)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/wabee)

![Wabee AI](https://wabee-public-assets.s3.amazonaws.com/images/wabee-small-box-white.png)

# Wabee SDK

**wabee-sdk** is a Python module for development of modules and extensions for the Wabee agentic AI platform.

## Installation

```bash
pip install wabee
```

## Command Line Interface (CLI)

The Wabee SDK includes a powerful CLI tool to streamline the development of Wabee agent tools.

### Creating a New Tool

Create a new tool using the interactive CLI:

```bash
wabee tools create
```

This command will prompt you for:
- Tool name
- Tool type (simple or complete)
- Tool description
- Initial version

#### Tool Types

1. **Simple Tool**: 
   - Ideal for straightforward, single-function tools
   - Uses the `@simple_tool` decorator
   - Less boilerplate code
   - Perfect for quick implementations

2. **Complete Tool**:
   - Full class implementation
   - More control over tool behavior
   - Better for complex tools with multiple operations
   - Includes error handling infrastructure

### Building Tool Containers

Build a tool into a container image:

```bash
wabee tools build <tool_directory> [options]
```

Options:
- `--image`: Specify custom image name (default: toolname:latest)

Example:
```bash
wabee tools build ./my-tool
```

## Tool Project Structure

When you create a new tool, the following structure is generated:

```
my_tool/
├── my_tool_tool.py      # Main tool implementation
├── requirements.txt     # Python dependencies
├── server.py           # gRPC server implementation
└── toolspec.yaml       # Tool specification and metadata
```

## RPC Server

Each built tool runs as a gRPC server that exposes a standardized interface for tool execution. The server:

- Listens on port 50051 by default (configurable via WABEE_GRPC_PORT)
- Automatically handles input validation using your Pydantic schemas
- Provides standardized error handling and reporting
- Supports streaming responses for long-running operations

When you build a tool with `wabee tools build`, the resulting container image includes:
- Your tool implementation
- All dependencies
- A pre-configured gRPC server
- Generated protocol buffers for type-safe communication

You can run the built container with:
```bash
docker run -p 50051:50051 mytool:latest
```

### toolspec.yaml

The tool specification file contains metadata about your tool:

```yaml
tool:
  name: MyTool
  description: Your tool description
  version: 0.1.0
  entrypoint: my_tool_tool.py
```

### Requirements

- Python >=3.11,<3.12
- Docker (for building containers)
- Internet connection (for downloading S2I builder)

## Development Examples

### Simple Tool Example

```python
from pydantic import BaseModel
from wabee.tools.simple_tool import simple_tool

class MyToolInput(BaseModel):
    message: str

@simple_tool(schema=MyToolInput)
async def my_tool(input_data: MyToolInput) -> str:
    return f"Processed: {input_data.message}"
```

### Complete Tool Example

```python
from typing import Optional, Type
from pydantic import BaseModel
from wabee.tools.base_tool import BaseTool
from wabee.tools.tool_error import ToolError

class MyToolInput(BaseModel):
    message: str

class MyTool(BaseTool):
    args_schema: Type[BaseModel] = MyToolInput

    async def execute(self, input_data: MyToolInput) -> tuple[Optional[str], Optional[ToolError]]:
        try:
            result = f"Processed: {input_data.message}"
            return result, None
        except Exception as e:
            return None, ToolError(type="EXECUTION_ERROR", message=str(e))
```

## Contributing

Suggestions are welcome! Please feel free to submit bug reports or feedbacks as a Github issues.

## Links

- Website: https://wabee.ai/
- Documentation: https://documentation.wabee.ai
- GitHub: https://github.com/wabee-ai/wabee-sdk

