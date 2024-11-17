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
from pathlib import Path
from typing import Optional

class BuildToolService:
    S2I_VERSION = "v1.4.0"
    PYTHON_BUILDER = "registry.access.redhat.com/ubi8/python-39:latest"
    
    def __init__(self):
        self.s2i_dir = Path.home() / ".wabee" / "s2i"
        self.s2i_path = self.s2i_dir / self._get_s2i_binary_name()
        
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
        tool_module: str = "tool",
        tool_name: str = "tool",
        image_name: Optional[str] = None,
        builder_name: Optional[str] = None
    ) -> None:
        """Build a tool using s2i."""
        print(f"Starting build process...")
        
        self._download_s2i()
        tool_dir = Path(tool_path)
        
        # Validate tool directory has required files
        if not tool_dir.exists():
            raise ValueError(f"Tool directory not found: {tool_path}")
            
        if not (tool_dir / "requirements.txt").exists():
            raise ValueError(f"No requirements.txt found in {tool_path}")
        
        # Generate protos in tool directory
        self._generate_protos(tool_dir)
            
        if not image_name:
            image_name = f"{tool_name}:latest"
            
        if not builder_name:
            builder_name = self.PYTHON_BUILDER
            
        # Create environment file with tool configuration
        env_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        try:
            env_file.write(f"WABEE_TOOL_MODULE={tool_module}\n")
            env_file.write(f"WABEE_TOOL_NAME={tool_name}\n")
            env_file.close()
            
            # Run s2i build directly
            subprocess.run(
                [
                    str(self.s2i_path),
                    "build",
                    "--env-file", env_file.name,
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
