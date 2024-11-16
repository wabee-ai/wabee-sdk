import os
import shutil
from typing import Literal

class CreateToolService:
    TOOL_TYPES = Literal["simple", "complete"]
    
    def __init__(self):
        self.templates_dir = os.path.join(os.path.dirname(__file__), "templates")
        
    def create_tool(self, name: str, tool_type: TOOL_TYPES) -> None:
        """Create a new tool project with the given name and type."""
        # Create project directory
        os.makedirs(name, exist_ok=True)
        
        # Create tool file
        tool_file = os.path.join(name, f"{name.lower()}_tool.py")
        with open(tool_file, "w") as f:
            if tool_type == "simple":
                f.write(self._get_simple_tool_template(name))
            else:
                f.write(self._get_complete_tool_template(name))
                
        # Create Dockerfile and s2i files
        self._create_docker_files(name)
        
    def _get_simple_tool_template(self, name: str) -> str:
        class_name = "".join(word.capitalize() for word in name.split("_"))
        return f'''from typing import Optional
from pydantic import BaseModel
from wabee.tools.simple_tool import simple_tool
from wabee.tools.tool_error import ToolError

class {class_name}Input(BaseModel):
    message: str

@simple_tool(schema={class_name}Input)
async def {name.lower()}_tool(input_data: {class_name}Input) -> str:
    """
    A simple tool that processes the input message.
    
    Args:
        input_data: The input data containing the message to process
        
    Returns:
        The processed message
    """
    return f"Processed: {{input_data.message}}"
'''

    def _get_complete_tool_template(self, name: str) -> str:
        class_name = "".join(word.capitalize() for word in name.split("_"))
        return f'''from typing import Optional, Type
from pydantic import BaseModel
from wabee.tools.base_tool import BaseTool
from wabee.tools.tool_error import ToolError

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
                type="EXECUTION_ERROR",
                message=str(e),
                original_error=e
            )

    @classmethod
    def create(cls) -> "{class_name}Tool":
        """Factory method to create an instance of this tool."""
        return cls()
'''

    def _create_docker_files(self, name: str) -> None:
        """Create Dockerfile and s2i configuration files."""
        # Create Dockerfile
        dockerfile = os.path.join(name, "Dockerfile")
        with open(dockerfile, "w") as f:
            f.write('''FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
''')

        # Create s2i files
        s2i_dir = os.path.join(name, ".s2i")
        os.makedirs(s2i_dir, exist_ok=True)
        
        # Create environment file
        env_file = os.path.join(s2i_dir, "environment")
        with open(env_file, "w") as f:
            f.write('''UPGRADE_PIP_TO_LATEST=true
ENABLE_PIPENV=true
''')

        # Create requirements.txt
        requirements = os.path.join(name, "requirements.txt")
        with open(requirements, "w") as f:
            f.write('''wabee
pydantic>=2.0.0
''')
