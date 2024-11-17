import os
import platform
import subprocess
import sys
import requests
import stat
import shutil
import tarfile
import tempfile
import pkg_resources
import re
from pathlib import Path
from typing import Optional

class BuildToolService:
    S2I_VERSION = "v1.4.0"
    PYTHON_BUILDER = "registry.access.redhat.com/ubi8/python-311:latest"
    
    def __init__(self, s2i_commit: Optional[str] = None):
        self.s2i_dir = Path.home() / ".wabee" / "s2i"
        self.s2i_path = self.s2i_dir / self._get_s2i_binary_name()
        self.S2I_COMMIT = s2i_commit or "27f0729"  # Default commit if none provided
        
    def _get_s2i_binary_name(self) -> str:
        """Get the name of the s2i binary."""
        return "s2i"
        
    def _get_s2i_archive_name(self) -> str:
        """Get the appropriate s2i archive name for the current platform."""
        system = platform.system().lower()
        machine = platform.machine().lower()
        
        arch = "arm64" if ("arm" in machine or "aarch64" in machine) else "amd64"
        
        if system == "darwin":
            platform_name = "darwin"
        elif system == "linux":
            platform_name = "linux"
        else:
            raise ValueError(f"Unsupported platform: {system}-{machine}")
            
        return f"source-to-image-{self.S2I_VERSION}-{self.S2I_COMMIT}-{platform_name}-{arch}.tar.gz"
            
    def _download_s2i(self) -> None:
        """Download and extract s2i binary if not present."""
        if self.s2i_path.exists():
            return
            
        self.s2i_dir.mkdir(parents=True, exist_ok=True)
        archive_name = self._get_s2i_archive_name()
        download_url = (
            f"https://github.com/openshift/source-to-image/releases/download/"
            f"{self.S2I_VERSION}/{archive_name}"
        )
        
        print("Downloading s2i...")
        response = requests.get(download_url, stream=True)
        response.raise_for_status()
        
        # Create a temporary file to store the downloaded archive
        with tempfile.NamedTemporaryFile(suffix='.tar.gz', delete=False) as tmp_file:
            for chunk in response.iter_content(chunk_size=8192):
                tmp_file.write(chunk)
            tmp_file.flush()
            
            # Extract the s2i binary from the archive
            with tarfile.open(tmp_file.name, 'r:gz') as tar:
                # Find the s2i binary in the archive
                s2i_path = None
                for member in tar.getmembers():
                    if member.name.endswith('/s2i') or member.name == 's2i':
                        s2i_path = member.name
                        break
                
                if not s2i_path:
                    raise RuntimeError("Could not find s2i binary in archive")
                
                s2i_binary = tar.extractfile(s2i_path)
                if s2i_binary:
                    with open(self.s2i_path, 'wb') as f:
                        f.write(s2i_binary.read())
                        
        # Clean up the temporary file
        os.unlink(tmp_file.name)
                
        # Make binary executable
        self.s2i_path.chmod(self.s2i_path.stat().st_mode | stat.S_IEXEC)
        

    def _generate_protos(self, tool_dir: Path) -> None:
        """Generate gRPC code from proto definitions in the tool directory."""
        # Create protos directory in tool dir
        protos_dir = tool_dir / "protos"
        protos_dir.mkdir(exist_ok=True)
        
        # Get the proto file from the installed package
        proto_resource = pkg_resources.resource_filename(
            'wabee', 'rpc/protos/tool_service.proto'
        )
        
        # Copy proto file to tool directory
        shutil.copy2(proto_resource, protos_dir / "tool_service.proto")
        
        # Generate the gRPC code
        try:
            subprocess.run([
                "python", "-m", "grpc_tools.protoc",
                "-I", str(tool_dir),
                f"--python_out={tool_dir}",
                f"--grpc_python_out={tool_dir}",
                f"--pyi_out={tool_dir}",
                str(protos_dir / "tool_service.proto")
            ], check=True)
            print("Successfully generated proto code")
        except subprocess.CalledProcessError as e:
            print(f"Error generating proto code: {e}", file=sys.stderr)
            raise

    def build_tool(
        self,
        tool_path: str,
        tool_module: Optional[str] = None,
        tool_name: Optional[str] = None,
        image_name: Optional[str] = None,
        builder_name: Optional[str] = None
    ) -> None:
        """Build a tool using s2i.
        
        Args:
            tool_path: Path to the tool directory
            tool_module: Optional module name. If not provided, will be derived from the tool file
            tool_name: Optional tool name. If not provided, will be derived from the tool file
            image_name: Optional custom image name
            builder_name: Optional custom builder image name
        """
        print(f"Starting build process...")
        
        self._download_s2i()
        tool_dir = Path(tool_path)
        
        # Validate tool directory has required files
        if not tool_dir.exists():
            raise ValueError(f"Tool directory not found: {tool_path}")
            
        if not (tool_dir / "requirements.txt").exists():
            raise ValueError(f"No requirements.txt found in {tool_path}")

        # Find the tool module file if not explicitly provided
        if tool_module is None:
            python_files = list(tool_dir.glob("*_tool.py"))
            if not python_files:
                raise ValueError(f"No *_tool.py file found in {tool_path}")
            if len(python_files) > 1:
                raise ValueError(f"Multiple tool files found in {tool_path}. Please specify tool_module.")
            
            # Get the filename without .py extension
            tool_module = python_files[0].stem

        # If tool_name not provided, try to find the tool class/function name
        if tool_name is None:
            tool_file = tool_dir / f"{tool_module}.py"
            with open(tool_file, 'r') as f:
                content = f.read()
                
            # Look for class definition first (complete tool)
            class_match = re.search(r'class\s+(\w+)(?<!Input)(?:\s*\([^)]*\))?\s*:', content)
            if class_match:
                tool_name = class_match.group(1)
            else:
                # Look for decorated function (simple tool)
                func_match = re.search(r'@simple_tool[^\n]*\s*async\s+def\s+(\w+)', content)
                if func_match:
                    tool_name = func_match.group(1)
                else:
                    raise ValueError(f"Could not find tool class or function in {tool_file}")
        
        # Generate protos in tool directory
        self._generate_protos(tool_dir)
            
        if not image_name:
            image_name = f"{tool_module}:latest"  # Use module name for image
            
        if not builder_name:
            builder_name = self.PYTHON_BUILDER
            
        # Create environment file with tool configuration
        env_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        try:
            env_file.write(f"WABEE_TOOL_MODULE={tool_module}\n")
            env_file.write(f"WABEE_TOOL_NAME={tool_name}\n")
            env_file.write("APP_FILE=server.py\n")
            env_file.close()
            
            print(f"Building with environment:")
            print(f"  WABEE_TOOL_MODULE={tool_module}")
            print(f"  WABEE_TOOL_NAME={tool_name}")
            
            # Run s2i build directly
            subprocess.run(
                [
                    str(self.s2i_path),
                    "build",
                    "--environment-file", env_file.name,
                    str(tool_dir),
                    builder_name,
                    image_name,
                ],
                check=True
            )
            
            print(f"Successfully built image: {image_name}")
        except subprocess.CalledProcessError as e:
            print(f"Error building image: {e}", file=sys.stderr)
            raise
        finally:
            os.unlink(env_file.name)
