import os
import platform
import subprocess
import sys
import requests
import stat
from pathlib import Path
from typing import Optional

class BuildToolService:
    S2I_VERSION = "v1.3.9"
    PYTHON_IMAGE = "python:3.11-slim"
    
    def __init__(self):
        self.s2i_dir = Path.home() / ".wabee" / "s2i"
        self.s2i_path = self.s2i_dir / self._get_s2i_binary_name()
        
    def _get_s2i_binary_name(self) -> str:
        """Get the appropriate s2i binary name for the current platform."""
        system = platform.system().lower()
        machine = platform.machine().lower()
        
        if system == "darwin":
            if "arm" in machine or "aarch64" in machine:
                return "s2i-darwin-arm64"
            return "s2i-darwin-amd64"
        elif system == "linux":
            if "arm" in machine or "aarch64" in machine:
                return "s2i-linux-arm64"
            return "s2i-linux-amd64"
        else:
            raise ValueError(f"Unsupported platform: {system}-{machine}")
            
    def _download_s2i(self) -> None:
        """Download s2i binary if not present."""
        if self.s2i_path.exists():
            return
            
        self.s2i_dir.mkdir(parents=True, exist_ok=True)
        binary_name = self._get_s2i_binary_name()
        download_url = (
            f"https://github.com/openshift/source-to-image/releases/download/"
            f"{self.S2I_VERSION}/{binary_name}"
        )
        
        print("Downloading s2i...")
        response = requests.get(download_url, stream=True)
        response.raise_for_status()
        
        with open(self.s2i_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        # Make binary executable
        self.s2i_path.chmod(self.s2i_path.stat().st_mode | stat.S_IEXEC)
        
    def build_tool(self, tool_path: str, image_name: Optional[str] = None) -> None:
        """Build a tool using s2i."""
        self._download_s2i()
        
        # Validate tool path
        tool_dir = Path(tool_path)
        if not tool_dir.exists():
            raise ValueError(f"Tool directory not found: {tool_path}")
            
        if not image_name:
            # Use directory name as image name
            image_name = f"{tool_dir.name}:latest"
            
        print(f"Building tool image: {image_name}")
        try:
            subprocess.run(
                [
                    str(self.s2i_path),
                    "build",
                    str(tool_dir),
                    self.PYTHON_IMAGE,
                    image_name,
                ],
                check=True
            )
            print(f"Successfully built image: {image_name}")
        except subprocess.CalledProcessError as e:
            print(f"Error building image: {e}", file=sys.stderr)
            raise
