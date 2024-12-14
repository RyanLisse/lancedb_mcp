"""LanceDB MCP initialization."""

import re
import sys
from pathlib import Path
from typing import Any

import click
import toml


def get_package_directory(path: Path) -> Path:
    """Get package directory.

    Args:
    ----
        path: Project root path

    Returns:
    -------
        Path: Package directory
    """
    src_dir = path / "src"
    if not src_dir.exists():
        src_dir.mkdir()

    package_dir = next(src_dir.glob("*/__init__.py"), None)
    if package_dir is None:
        raise FileNotFoundError("Package directory not found")

    return package_dir.parent


def check_package_name(name: str) -> bool:
    """Check package name.

    Args:
    ----
        name: Package name

    Returns:
    -------
        bool: True if name is valid, False otherwise
    """
    if " " in name:
        return False

    if not re.match(r"^[a-zA-Z][a-zA-Z0-9_-]*$", name):
        return False

    return True


class PyProject:
    """PyProject configuration."""

    def __init__(self, pyproject_path: Path) -> None:
        """Initialize PyProject.

        Args:
        ----
            pyproject_path: Path to pyproject.toml
        """
        self.pyproject_path = pyproject_path
        self.data = {}

        if pyproject_path.exists():
            with open(pyproject_path) as f:
                self.data = toml.load(f)
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
        """Get project settings.

        Returns
        -------
            dict[str, Any]: Project settings
        """
        return self.data

    def save(self) -> None:
        """Save configuration to pyproject.toml."""
        with open(self.pyproject_path, "w") as f:
            toml.dump(self.data, f)


def update_pyproject_settings(
    path: Path, name: str, description: str, version: str = "0.1.0"
) -> None:
    """Update pyproject.toml settings.

    Args:
    ----
        path: Project root path
        name: Project name
        description: Project description
        version: Project version
    """
    pyproject = PyProject(path / "pyproject.toml")
    pyproject.data["project"].update(
        {
            "name": name,
            "description": description,
            "version": version,
        }
    )
    pyproject.save()


def create_project(
    path: Path, name: str, description: str, version: str = "0.1.0"
) -> None:
    """Create new project.

    Args:
    ----
        path: Project root path
        name: Project name
        description: Project description
        version: Project version
    """
    if not check_package_name(name):
        click.echo("❌ Invalid name", err=True)
        sys.exit(1)

    package_dir = path / "src" / name
    package_dir.mkdir(parents=True, exist_ok=True)

    init_path = package_dir / "__init__.py"
    with open(init_path, "w") as f:
        f.write('"""Package initialization."""\n\n')
        f.write(f'__version__ = "{version}"\n')

    update_pyproject_settings(path, name, description, version)


def get_version() -> str:
    """Get version from pyproject.toml.

    Returns
    -------
        str: Version
    """
    pyproject = PyProject(Path.cwd() / "pyproject.toml")
    return pyproject.settings["project"]["version"]
