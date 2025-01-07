import os
import yaml
import logging
import importlib
from typing import Dict, Any, Optional, Type
from pathlib import Path
from pydantic import BaseModel

from wabee.tools.base_tool import BaseTool

logger = logging.getLogger(__name__)

class ToolLoadError(Exception):
    """Raised when tool loading fails"""
    pass

class ConfigurationError(Exception):
    """Raised when tool configuration is invalid"""
    pass

class ToolConfig(BaseModel):
    """Configuration for tool loading"""
    module_name: str
    tool_name: str
    args: Optional[Dict[str, Any]] = None

class ToolLoader:
    """Handles loading of tool instances from various sources"""

    @staticmethod
    def load_from_env() -> BaseTool:
        """Load tool based on environment variables"""
        module_name = os.environ.get('WABEE_TOOL_MODULE')
        tool_name = os.environ.get('WABEE_TOOL_NAME')
        
        if not module_name or not tool_name:
            raise ConfigurationError(
                "WABEE_TOOL_MODULE and WABEE_TOOL_NAME environment variables are required"
            )

        config = ToolConfig(
            module_name=module_name,
            tool_name=tool_name,
            args=ToolLoader._load_args_from_spec()
        )
        
        return ToolLoader.load_tool(config)

    @staticmethod
    def load_from_spec(spec_path: Path) -> BaseTool:
        """Load tool from toolspec.yaml"""
        if not spec_path.exists():
            raise ConfigurationError(f"Tool spec not found: {spec_path}")

        try:
            with open(spec_path) as f:
                spec = yaml.safe_load(f)
        except Exception as e:
            raise ConfigurationError(f"Failed to load tool spec: {e}")

        if not isinstance(spec, dict) or 'tool' not in spec:
            raise ConfigurationError("Invalid tool spec format")

        tool_spec = spec['tool']
        config = ToolConfig(
            module_name=tool_spec.get('module', tool_spec.get('entrypoint', '').replace('.py', '')),
            tool_name=f"{tool_spec.get('name')}Tool",
            args=ToolLoader._parse_tool_args(tool_spec.get('tool_args', []))
        )

        return ToolLoader.load_tool(config)

    @staticmethod
    def load_tool(config: ToolConfig) -> BaseTool:
        """Core tool loading logic"""
        try:
            logger.info(f"Loading tool module: {config.module_name}")
            module = importlib.import_module(config.module_name)
            
            logger.info(f"Loading tool class/function: {config.tool_name}")
            tool_class = getattr(module, config.tool_name)
            
            if hasattr(tool_class, 'create'):
                logger.info("Creating tool instance using create() method")
                return tool_class.create(**(config.args or {}))
            elif isinstance(tool_class, Type):
                logger.info("Creating tool instance directly")
                return tool_class(**(config.args or {}))
            else:
                logger.info("Using function-based tool")
                return tool_class

        except ImportError as e:
            raise ToolLoadError(f"Failed to import tool module: {e}")
        except AttributeError as e:
            raise ToolLoadError(f"Failed to load tool class/function: {e}")
        except Exception as e:
            raise ToolLoadError(f"Failed to create tool instance: {e}")

    @staticmethod
    def _load_args_from_spec() -> Optional[Dict[str, Any]]:
        """Load tool arguments from toolspec.yaml if present"""
        spec_path = os.environ.get('WABEE_TOOLSPEC_PATH', 'toolspec.yaml')
        if not os.path.exists(spec_path):
            return None

        try:
            with open(spec_path) as f:
                spec = yaml.safe_load(f)
            if isinstance(spec, dict) and 'tool' in spec and 'tool_args' in spec['tool']:
                return ToolLoader._parse_tool_args(spec['tool']['tool_args'])
        except Exception as e:
            logger.warning(f"Failed to load tool args from spec: {e}")
        return None

    @staticmethod
    def _parse_tool_args(args_list: list) -> Dict[str, Any]:
        """Parse tool arguments from spec format to dictionary"""
        return {arg['name']: arg['value'] for arg in args_list if 'name' in arg and 'value' in arg}
