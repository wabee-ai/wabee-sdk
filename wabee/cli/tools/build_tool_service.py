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
        print(f"Preparing builder image {builder_name}")
        s2i_dir = self.template_dir / "s2i"
        print(f"Using S2I directory: {s2i_dir}")
        
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            print(f"Created temp directory: {tmp_path}")
            
            # Create s2i directory structure
            (tmp_path / "s2i" / "bin").mkdir(parents=True)
            print(f"Created S2I bin directory: {tmp_path / 's2i' / 'bin'}")
            
            # Copy S2I scripts
            for script in ["assemble", "run", "usage"]:
                src = s2i_dir / "bin" / script
                dst = tmp_path / "s2i" / "bin" / script
                print(f"Copying {src} to {dst}")
                shutil.copy(src, dst)
                
                # Ensure scripts are executable
                os.chmod(
                    dst,
                    stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH
                )
                print(f"Made {script} executable")
            
            # Copy Dockerfile
            dockerfile_src = s2i_dir / "Dockerfile"
            dockerfile_dst = tmp_path / "Dockerfile"
            print(f"Copying Dockerfile from {dockerfile_src} to {dockerfile_dst}")
            shutil.copy(dockerfile_src, dockerfile_dst)
            
            # Build the builder image
            print(f"Building Docker image {builder_name}")
            try:
                subprocess.run(
                    ["docker", "build", "-t", builder_name, str(tmp_path)],
                    check=True,
                    capture_output=True,
                    text=True
                )
                print("Successfully built builder image")
            except subprocess.CalledProcessError as e:
                print(f"Error building image: {e.stdout}\n{e.stderr}")
                raise

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
        builder_name: str = "wabee-tool-builder:latest"
    ) -> None:
        """Build a tool using s2i."""
        print(f"Starting build process...")
        print(f"Template directory: {self.template_dir}")
        print(f"S2I directory: {self.template_dir / 's2i'}")
        
        self._download_s2i()
        tool_dir = Path(tool_path)
        
        # Add verification of s2i scripts
        s2i_scripts_dir = self.template_dir / "s2i" / "bin"
        print(f"Checking S2I scripts in {s2i_scripts_dir}")
        for script in ["assemble", "run", "usage"]:
            script_path = s2i_scripts_dir / script
            if script_path.exists():
                print(f"Found script: {script}")
            else:
                print(f"Missing script: {script}")
        
        # Validate tool directory has required files
        if not tool_dir.exists():
            raise ValueError(f"Tool directory not found: {tool_path}")
            
        if not (tool_dir / "pyproject.toml").exists():
            raise ValueError(f"No pyproject.toml found in {tool_path}")
        
        # Generate protos in tool directory
        self._generate_protos(tool_dir)
            
        if not image_name:
            # Use directory name as image name
            image_name = f"{tool_name}:latest"
            
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
                    "--environment-file",
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
