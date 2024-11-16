import os
import platform
import subprocess
import sys
import requests
import stat
import tarfile
import tempfile
from pathlib import Path
from typing import Optional

class BuildToolService:
    S2I_VERSION = "v1.4.0"
    S2I_COMMIT = "d3544c7e"
    PYTHON_IMAGE = "python:3.11-slim"
    
    def __init__(self, s2i_commit: str | None = None):
        self.s2i_dir = Path.home() / ".wabee" / "s2i"
        if s2i_commit:
            self.S2I_COMMIT = s2i_commit
        self.s2i_path = self.s2i_dir / self._get_s2i_binary_name()
        self.template_dir = Path(__file__).parent / "templates"
        
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
        
    def _prepare_builder_image(self, builder_name: str = "wabee-tool-builder:latest") -> None:
        """Prepare the S2I builder image."""
        s2i_dir = self.template_dir / "s2i"
        
        # Create temporary build context
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            
            # Copy S2I configuration
            shutil.copytree(s2i_dir, tmp_path / "s2i")
            
            # Copy Dockerfile
            shutil.copy(s2i_dir / "Dockerfile", tmp_path / "Dockerfile")
            
            # Build the builder image
            subprocess.run(
                ["docker", "build", "-t", builder_name, str(tmp_path)],
                check=True
            )

    def build_tool(
        self,
        tool_path: str,
        tool_module: str = "tool",
        tool_name: str = "tool",
        image_name: Optional[str] = None,
        builder_name: str = "wabee-tool-builder:latest"
    ) -> None:
        """Build a tool using s2i."""
        self._download_s2i()
        
        # Validate tool path
        tool_dir = Path(tool_path)
        if not tool_dir.exists():
            raise ValueError(f"Tool directory not found: {tool_path}")
            
        if not image_name:
            # Use directory name as image name
            image_name = f"{tool_dir.name}:latest"
            
        # Ensure builder image exists
        try:
            subprocess.run(
                ["docker", "inspect", builder_name],
                check=True,
                capture_output=True
            )
        except subprocess.CalledProcessError:
            print(f"Building S2I builder image: {builder_name}")
            self._prepare_builder_image(builder_name)
            
        print(f"Building tool image: {image_name}")
        
        # Create environment file
        env_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        try:
            env_file.write(f"WABEE_TOOL_MODULE={tool_module}\n")
            env_file.write(f"WABEE_TOOL_NAME={tool_name}\n")
            env_file.close()
            
            # Build the tool image using S2I
            subprocess.run(
                [
                    str(self.s2i_path),
                    "build",
                    "--env-file",
                    env_file.name,
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