import os
import re
import shutil
from typing import Literal

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
        version: str
    ) -> None:
        """Create a new tool project with the given name and type."""
        # Sanitize the name
        sanitized_name = sanitize_name(name)
        # Get CamelCase version for class names
        camel_case_name = to_camel_case(name)
        
        # Create project directory
        os.makedirs(sanitized_name, exist_ok=True)
        
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
            f.write(self._get_toolspec_template(sanitized_name, description, version))

        # Create pyproject.toml
        pyproject_file = os.path.join(sanitized_name, "pyproject.toml")
        with open(pyproject_file, "w") as f:
            f.write(self._get_pyproject_template(sanitized_name, description, version))
                
        # Create Dockerfile and s2i files
        self._create_build_files(sanitized_name)
        
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
    def create(cls) -> "{class_name}Tool":
        """Factory method to create an instance of this tool."""
        return cls()
'''

    def _get_toolspec_template(self, name: str, description: str, version: str) -> str:
        return f'''tool:
  name: {name}
  description: {description}
  version: {version}
  entrypoint: {name}_tool.py
'''

    def _get_pyproject_template(self, name: str, description: str, version: str) -> str:
        return f'''[tool.poetry]
name = "{name}"
version = "{version}"
description = "{description}"
authors = ["Wabee <developers@wabee.ai>"]

[tool.poetry.dependencies]
python = ">=3.10,<3.12"
wabee = "*"
pydantic = ">=2.0.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
'''

    def _create_build_files(self, name: str) -> None:
        """Create build configuration files."""
        # Create s2i files
        s2i_dir = os.path.join(name, ".s2i")
        os.makedirs(s2i_dir, exist_ok=True)
        
        # Create environment file
        env_file = os.path.join(s2i_dir, "environment")
        with open(env_file, "w") as f:
            f.write('''UPGRADE_PIP_TO_LATEST=true
ENABLE_PIPENV=false
''')
