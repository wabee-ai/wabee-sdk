import asyncio
import importlib
import os
import yaml
from wabee.rpc.server import serve
from typing import Dict, Any, List, Tuple

def load_tools() -> Dict[str, Any]:
    tools = {}
    tool_module = os.environ.get('WABEE_TOOL_MODULE', 'tool')
    tool_name = os.environ.get('WABEE_TOOL_NAME', 'tool')
    
    print(f"Loading tool module: {tool_module}")
    print(f"Loading tool name: {tool_name}")

    # Load tool_args from toolspec.yaml
    tool_args: List[Tuple[str, Any]] = []
    toolspec_path = os.environ.get('WABEE_TOOLSPEC_PATH', 'toolspec.yaml')
    
    if os.path.exists(toolspec_path):
        with open(toolspec_path, 'r') as f:
            toolspec = yaml.safe_load(f)
            if isinstance(toolspec, dict) and 'tool_args' in toolspec:
                tool_args = [(arg['name'], arg['value']) for arg in toolspec['tool_args']]
    
    try:
        module = importlib.import_module(tool_module)
        tool = getattr(module, tool_name)
        
        # Create tool config from args
        config_class = getattr(module, f"{tool_name}Config")
        config = config_class(**dict(tool_args))
        
        # Create tool instance using the config
        tool_instance = tool.create(config)
        tools[tool_name] = tool_instance
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
