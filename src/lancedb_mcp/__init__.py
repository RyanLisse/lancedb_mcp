"""LanceDB MCP initialization."""

import os
import re
from pathlib import Path
from typing import Any

import tomlkit
from pydantic import BaseModel

# Constants
PYPROJECT_FILE = "pyproject.toml"
PACKAGE_NAME = "lancedb_mcp"


class PyProjectClass(BaseModel):
    """PyProject class."""

    name: str
    version: str
    description: str | None = None
    authors: list[str] | None = None
    dependencies: dict[str, str] | None = None
    dev_dependencies: dict[str, str] | None = None


def get_package_directory() -> Path:
    """Get the package directory."""
    return Path(os.path.dirname(os.path.abspath(__file__)))


def check_package_name(name: str) -> bool:
    """Check if package name is valid."""
    return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", name))


class PyProject:
    """PyProject configuration."""

    def __init__(self, pyproject_path: Path) -> None:
        """Initialize PyProject."""
        self.pyproject_path = pyproject_path
        self.data = {}

        if pyproject_path.exists():
            try:
                with open(pyproject_path) as f:
                    self.data = tomlkit.load(f)
            except Exception as err:
                raise RuntimeError(f"Failed to load {pyproject_path}") from err
        else:
            self.data = {
                "project": {
                    "name": "",
                    "version": "0.1.0",
                    "description": "",
                },
            }

    @property
    def settings(self) -> dict[str, Any]:
        """Get project settings."""
        return self.data.get("project", {})

    def save(self) -> None:
        """Save configuration to pyproject.toml."""
        with open(self.pyproject_path, "w") as f:
            tomlkit.dump(self.data, f)


def get_version() -> str:
    """Get version from pyproject.toml."""
    try:
        pyproject = PyProject(get_package_directory().parent.parent / PYPROJECT_FILE)
        return pyproject.settings.get("version", "0.1.0")
    except Exception:
        return "0.1.0"
