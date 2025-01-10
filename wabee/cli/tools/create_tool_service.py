import os
import re
import shutil
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
                f.write(self._get_simple_tool_template(sanitized_name, camel_case_name, description))
            else:
                f.write(self._get_complete_tool_template(sanitized_name, camel_case_name, description))
        
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
            f.write(self._get_ts_client_template(sanitized_name, camel_case_name, description))
        
        # Copy the server.js template
        server_template_path = os.path.join(os.path.dirname(__file__), "templates", "js_server.js")
        shutil.copy2(server_template_path, os.path.join(sanitized_name, "server.js"))
        
        # Create protos directory and copy proto file
        protos_dir = os.path.join(sanitized_name, "protos")
        os.makedirs(protos_dir, exist_ok=True)
        
        # Copy the proto file from the wabee package
        proto_source = os.path.join(os.path.dirname(__file__), "..", "..", "rpc", "protos", "tool_service.proto")
        proto_dest = os.path.join(protos_dir, "tool_service.proto")
        shutil.copy2(proto_source, proto_dest)
        
        # Create tsconfig.json
        tsconfig_file = os.path.join(sanitized_name, "tsconfig.json")
        with open(tsconfig_file, "w") as f:
            f.write(self._get_tsconfig_template())
        
    def _get_simple_tool_template(self, snake_name: str, class_name: str, description: str) -> str:
        return f'''from typing import Optional
from pydantic import BaseModel
from wabee.tools.simple_tool import simple_tool
from wabee.tools.tool_error import ToolError
from wabee.tools.base_model import StructuredToolResponse

class {class_name}Input(BaseModel):
    message: str

@simple_tool(
    name="{class_name}",
    description="{description}",
    schema={class_name}Input
)
async def {snake_name.lower()}_tool(input_data: {class_name}Input) -> StructuredToolResponse:
    """
    {description}
    
    Args:
        input_data: The input data containing the message to process
        
    Returns:
        A structured response containing the processed message
    """
    return StructuredToolResponse(
        variable_name="result",
        content=f"Processed: {{input_data.message}}",
        memory_push=False
    )
'''

    def _get_complete_tool_template(self, snake_name: str, class_name: str, description: str) -> str:
        return f'''from typing import Optional, Type
from pydantic import BaseModel
from wabee.tools.base_tool import BaseTool
from wabee.tools.base_model import StructuredToolResponse
from wabee.tools.tool_error import ToolError, ToolErrorType

class {class_name}Input(BaseModel):
    message: str

class {class_name}Tool(BaseTool):
    args_schema: Type[BaseModel] = {class_name}Input

    def __init__(self, **kwargs):
        """Initialize the tool with configuration."""
        super().__init__(
            name="{class_name}",
            description="{description}",
            **kwargs
        )

    async def execute(self, input_data: {class_name}Input) -> tuple[Optional[StructuredToolResponse], Optional[ToolError]]:
        """
        {description}
        
        Args:
            input_data: The validated input data
            
        Returns:
            A tuple of (result, error) where one will be None
        """
        try:
            result = StructuredToolResponse(
                variable_name="result",
                content=f"Processed: {{input_data.message}}",
                memory_push=False
            )
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
  entrypoint: {name.lower()}_tool.py
'''

    def _get_requirements_template(self, name: str, description: str, version: str) -> str:
        return '''wabee>=0.2.7
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
    "build": "npx tsc",
    "start": "node server.js",
    "test": "jest"
  }},
  "dependencies": {{
    "@wabee_ai/sdk": "^0.1.5",
    "@grpc/grpc-js": "^1.8.0",
    "@grpc/proto-loader": "^0.7.0",
    "zod": "^3.21.0"
  }},
  "devDependencies": {{
    "@types/node": "^18.0.0",
    "typescript": "^4.9.0",
    "jest": "^29.0.0",
    "ts-jest": "^29.0.0",
    "@types/jest": "^29.0.0",
    "ts-proto": "^1.181.2"
  }}
}}'''

    def _get_ts_client_template(self, name: str, class_name: str, description: str) -> str:
        return f'''import {{ z }} from 'zod';
import {{ simpleTool, ToolOptions, StructuredToolResponse }} from '@wabee_ai/sdk';

export const {class_name}Schema = z.object({{
    message: z.string().describe("Message to be displayed")
}}).describe("{description}");

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
        template_path = os.path.join(os.path.dirname(__file__), "templates", "python_server.py")
        shutil.copy2(template_path, os.path.join(name, "server.py"))
