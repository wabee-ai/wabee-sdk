import asyncio
import importlib
import os
from wabee.rpc.server import serve
from typing import Dict, Any

def load_tools() -> Dict[str, Any]:
    tools = {}
    tool_module = os.environ.get('WABEE_TOOL_MODULE', 'tool')
    tool_name = os.environ.get('WABEE_TOOL_NAME', 'tool')
    
    print(f"Loading tool module: {tool_module}")
    print(f"Loading tool name: {tool_name}")

    # Load tool_args from toolspec.yaml, this is a list of name, value items
    # todo: load tool_args from toolspec.yaml
    
    try:
        module = importlib.import_module(tool_module)
        tool = getattr(module, tool_name)
        
        # create an instance of the tool and pass the tool_args using the static create method that all tools have
        # todo: pass tool_args to the tool instance

        tools[tool_name] = tool
    except Exception as e:
        print(f"Error loading tool: {str(e)}")
        raise
        
    return tools

def main():
    port = int(os.environ.get('WABEE_GRPC_PORT', '50051'))
    tools = load_tools()
    print(f"Starting gRPC server with tools: {list(tools.keys())}")
    asyncio.run(serve(tools, port=port))

if __name__ == '__main__':
    main()
