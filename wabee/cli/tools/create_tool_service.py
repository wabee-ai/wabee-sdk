import os
import re
from typing import Literal, Optional, Type

def to_camel_case(name: str) -> str:
    """
    Convert a string to CamelCase.
    Example: 'my_cool_tool' -> 'MyCoolTool'
    """
    # First sanitize the name to ensure valid Python identifier
    sanitized = sanitize_name(name)
    # Split by underscore and capitalize each word
    return ''.join(word.capitalize() for word in sanitized.split('_'))

def sanitize_name(name: str) -> str:
    """
    Sanitize the tool name to be a valid Python identifier.
    
    - Converts to lowercase
    - Replaces spaces and invalid chars with underscores
    - Ensures it starts with a letter
    - Removes consecutive underscores
    """
    # Convert to lowercase and replace spaces/invalid chars with underscore
    name = re.sub(r'[^a-zA-Z0-9_]', '_', name.lower())
    
    # Ensure starts with letter
    if not name[0].isalpha():
        name = 'tool_' + name
        
    # Remove consecutive underscores
    name = re.sub(r'_+', '_', name)
    
    # Remove trailing underscore
    name = name.rstrip('_')
    
    return name

class CreateToolService:
    TOOL_TYPES = Literal["simple", "complete"]
    
    def __init__(self):
        self.templates_dir = os.path.join(os.path.dirname(__file__), "templates")
        
    def create_tool(
        self, 
        name: str, 
        tool_type: TOOL_TYPES,
        description: str,
        version: str,
        tool_language: Literal["python", "javascript"] = "python",
        generate_js: bool = True
    ) -> None:
        """Create a new tool project with the given name and type."""
        # Sanitize the name
        sanitized_name = sanitize_name(name)
        # Get CamelCase version for class names
        camel_case_name = to_camel_case(name)
        
        # Create project directory
        os.makedirs(sanitized_name, exist_ok=True)
        
        if tool_language == "python":
            # Create Python files
            self._create_python_files(sanitized_name, camel_case_name, tool_type, description, version)
            
            if generate_js:
                # Create JavaScript client
                self._create_js_files(sanitized_name, camel_case_name, description, version)
        else:  # javascript
            # Create only JavaScript files
            self._create_js_files(sanitized_name, camel_case_name, description, version)

    def _create_python_files(
        self,
        sanitized_name: str,
        camel_case_name: str,
        tool_type: TOOL_TYPES,
        description: str,
        version: str
    ) -> None:
        """Create Python-specific files for the tool."""
        # Create tool file
        tool_file = os.path.join(sanitized_name, f"{sanitized_name}_tool.py")
        with open(tool_file, "w") as f:
            if tool_type == "simple":
                f.write(self._get_simple_tool_template(sanitized_name, camel_case_name))
            else:
                f.write(self._get_complete_tool_template(sanitized_name, camel_case_name))
        
        # Create toolspec.yaml
        toolspec_file = os.path.join(sanitized_name, "toolspec.yaml")
        with open(toolspec_file, "w") as f:
            f.write(self._get_toolspec_template(camel_case_name, description, version))

        # Create requirements.txt
        requirements_file = os.path.join(sanitized_name, "requirements.txt")
        with open(requirements_file, "w") as f:
            f.write(self._get_requirements_template(sanitized_name, description, version))
                
        # Create server.py
        self._create_server_file(sanitized_name)

    def _create_js_files(
        self,
        sanitized_name: str,
        camel_case_name: str,
        description: str,
        version: str
    ) -> None:
        """Create JavaScript/TypeScript files for the tool."""
        # Create package.json
        package_file = os.path.join(sanitized_name, "package.json")
        with open(package_file, "w") as f:
            f.write(self._get_js_package_template(sanitized_name, description, version))
        
        # Create TypeScript client
        src_dir = os.path.join(sanitized_name, "src")
        os.makedirs(src_dir, exist_ok=True)
        client_file = os.path.join(src_dir, "index.ts")
        with open(client_file, "w") as f:
            f.write(self._get_ts_client_template(sanitized_name, camel_case_name))
        
        # Create tsconfig.json
        tsconfig_file = os.path.join(sanitized_name, "tsconfig.json")
        with open(tsconfig_file, "w") as f:
            f.write(self._get_tsconfig_template())
        
    def _get_simple_tool_template(self, snake_name: str, class_name: str) -> str:
        return f'''from typing import Optional
from pydantic import BaseModel
from wabee.tools.simple_tool import simple_tool
from wabee.tools.tool_error import ToolError

class {class_name}Input(BaseModel):
    message: str

@simple_tool(schema={class_name}Input)
async def {snake_name.lower()}_tool(input_data: {class_name}Input) -> str:
    """
    A simple tool that processes the input message.
    
    Args:
        input_data: The input data containing the message to process
        
    Returns:
        The processed message
    """
    return f"Processed: {{input_data.message}}"
'''

    def _get_complete_tool_template(self, snake_name: str, class_name: str) -> str:
        return f'''from typing import Optional, Type
from pydantic import BaseModel
from wabee.tools.base_tool import BaseTool
from wabee.tools.tool_error import ToolError, ToolErrorType

class {class_name}Input(BaseModel):
    message: str

class {class_name}Tool(BaseTool):
    args_schema: Type[BaseModel] = {class_name}Input

    async def execute(self, input_data: {class_name}Input) -> tuple[Optional[str], Optional[ToolError]]:
        """
        Execute the tool's main functionality.
        
        Args:
            input_data: The validated input data
            
        Returns:
            A tuple of (result, error) where one will be None
        """
        try:
            result = f"Processed: {{input_data.message}}"
            return result, None
        except Exception as e:
            return None, ToolError(
                type=ToolErrorType.EXECUTION_ERROR,
                message=str(e),
                original_error=e
            )

    @classmethod
    def create(cls, **kwargs) -> "{class_name}Tool":
        """Factory method to create an instance of this tool."""
        return cls(**kwargs)
'''

    def _get_toolspec_template(self, name: str, description: str, version: str) -> str:
        return f'''tool:
  name: {name}
  description: {description}
  version: {version}
  entrypoint: {name}_tool.py
'''

    def _get_requirements_template(self, name: str, description: str, version: str) -> str:
        return '''wabee>=0.2.1
pydantic>=2.0.0
'''

    def _get_js_package_template(self, name: str, description: str, version: str) -> str:
        return f'''{{
  "name": "{name}",
  "version": "{version}",
  "description": "{description}",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "scripts": {{
    "build": "tsc",
    "test": "jest"
  }},
  "dependencies": {{
    "@wabee_ai/sdk": "^0.1.0",
    "zod": "^3.21.0"
  }},
  "devDependencies": {{
    "@types/node": "^18.0.0",
    "typescript": "^4.9.0",
    "jest": "^29.0.0",
    "ts-jest": "^29.0.0",
    "@types/jest": "^29.0.0"
  }}
}}'''

    def _get_ts_client_template(self, name: str, class_name: str) -> str:
        return f'''import {{ z }} from 'zod';
import {{ simpleTool, ToolOptions }} from 'wabee-js';

export const {class_name}Schema = z.object({{
    message: z.string()
}});

export type {class_name}Input = z.infer<typeof {class_name}Schema>;

export function create{class_name}Tool(options?: ToolOptions) {{
    return simpleTool(
        '{name}',
        {class_name}Schema,
        options
    );
}}
'''

    def _get_tsconfig_template(self) -> str:
        return '''{
  "compilerOptions": {
    "target": "es2020",
    "module": "commonjs",
    "declaration": true,
    "outDir": "./dist",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}'''

    def _create_server_file(self, name: str) -> None:
        """Create the server.py file in the tool directory."""
        server_content = '''import asyncio
import importlib
import os
import yaml
from wabee.rpc.server import serve
from typing import Dict, Any, List, Tuple

def load_tools() -> Dict[str, Any]:
    tools = {}
    tool_module = os.environ.get('WABEE_TOOL_MODULE', 'tool')
    tool_name = os.environ.get('WABEE_TOOL_NAME', 'tool')

    tool_args: List[Tuple[str, Any]] = []
    toolspec_path = os.environ.get('WABEE_TOOLSPEC_PATH', 'toolspec.yaml')

    if os.path.exists(toolspec_path):
        with open(toolspec_path, 'r') as f:
            toolspec = yaml.safe_load(f)
            if isinstance(toolspec, dict) and 'tool_args' in toolspec['tool']:
                tool_args = [(arg['name'], arg['value']) for arg in toolspec['tool']['tool_args']]
    
    print(f"Loading tool module: {tool_module}")
    print(f"Loading tool name: {tool_name}")
    
    try:
        module = importlib.import_module(tool_module)
        tool = getattr(module, tool_name)
        config = dict(tool_args)
        tool_instance = tool.create(**config)
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
'''
        with open(os.path.join(name, "server.py"), "w") as f:
            f.write(server_content)
