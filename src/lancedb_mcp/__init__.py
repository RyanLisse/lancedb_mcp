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


def check_package_name(name: str) -> None:
    """Check package name.

    Args:
    ----
        name: Package name
    """
    if " " in name:
        click.echo("❌ Name must not contain spaces", err=True)
        sys.exit(1)

    if not re.match(r"^[a-zA-Z0-9_-]+$", name):
        click.echo("❌ Invalid name", err=True)
        sys.exit(1)


class PyProject:
    """PyProject configuration."""

    def __init__(self, pyproject_path: Path | None = None) -> None:
        """Initialize PyProject configuration.

        Args:
        ----
            pyproject_path: Path to pyproject.toml
        """
        self.pyproject_path = pyproject_path or Path("pyproject.toml")
        self.data = {
            "project": {
                "name": "",
                "version": "0.1.0",
                "description": "",
                "scripts": {},
            }
        }

        if self.pyproject_path.exists():
            self.data = self._load_config()

    def _load_config(self) -> dict[str, Any]:
        """Load configuration from pyproject.toml.

        Returns
        -------
            Dict[str, Any]: Configuration data
        """
        if not self.pyproject_path.exists():
            raise FileNotFoundError(f"File not found: {self.pyproject_path}")

        return toml.load(self.pyproject_path)

    @property
    def name(self) -> str:
        """Get project name.

        Returns
        -------
            str: Project name
        """
        return self.data["project"]["name"]

    @property
    def version(self) -> str:
        """Get project version.

        Returns
        -------
            str: Project version
        """
        return self.data["project"].get("version", "0.1.0")

    @property
    def first_binary(self) -> str:
        """Get first binary name.

        Returns
        -------
            str: Binary name
        """
        scripts = self.data.get("project", {}).get("scripts", {})
        return next(iter(scripts.keys())) if scripts else ""


def update_pyproject_settings(path: Path, settings: dict[str, Any]) -> None:
    """Update pyproject.toml settings.

    Args:
    ----
        path: Project root path
        settings: Settings to update
    """
    pyproject_path = path / "pyproject.toml"
    if not pyproject_path.exists():
        pyproject = PyProject(pyproject_path)
        pyproject.data["project"].update(settings)
    else:
        pyproject = PyProject(pyproject_path)
        pyproject.data["project"].update(settings)

    with open(pyproject.pyproject_path, "w") as f:
        toml.dump(pyproject.data, f)


def copy_template(
    path: Path, name: str, description: str, version: str = "0.1.0"
) -> None:
    """Copy template files into src/<project_name>.

    Args:
    ----
        path: Project root path
        name: Project name
        description: Project description
        version: Project version
    """
    # Get template directory
    template_parent = Path(__file__).parent
    if "test" in str(template_parent):
        # If we're in a test, use the test template directory
        template_dir = Path(__file__).parent / "template"
    else:
        # Otherwise, use the package template directory
        template_dir = template_parent / "template"

    target_dir = path / "src" / name

    # Debug logging
    print(f"Template directory: {template_dir}", file=sys.stderr)
    print(f"Target directory: {target_dir}", file=sys.stderr)
    print(f"Template directory exists: {template_dir.exists()}", file=sys.stderr)
    if template_dir.exists():
        print(
            f"Template directory contents: {list(template_dir.iterdir())}",
            file=sys.stderr,
        )

    # Ensure target directory exists
    target_dir.mkdir(parents=True, exist_ok=True)

    from jinja2 import Environment, FileSystemLoader

    env = Environment(loader=FileSystemLoader(str(template_dir)))

    files = [
        ("__init__.py.jinja2", "__init__.py", target_dir),
        ("server.py.jinja2", "server.py", target_dir),
        ("README.md.jinja2", "README.md", path),
    ]

    pyproject = PyProject(path / "pyproject.toml")
    bin_name = pyproject.first_binary

    template_vars = {
        "binary_name": bin_name,
        "server_name": name,
        "server_version": version,
        "server_description": description,
        "server_directory": str(path.resolve()),
    }

    try:
        for template_file, output_file, output_dir in files:
            template = env.get_template(template_file)
            rendered = template.render(**template_vars)

            out_path = output_dir / output_file
            out_path.write_text(rendered)

    except Exception as e:
        print(f"Error copying template: {e}", file=sys.stderr)
        raise


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
    check_package_name(name)

    # Create src directory
    src_dir = path / "src" / name
    src_dir.mkdir(parents=True, exist_ok=True)

    # Create pyproject.toml
    settings = {
        "name": name,
        "version": version,
        "description": description,
        "scripts": {
            name: f"{name}.__main__:main",
        },
    }
    update_pyproject_settings(path, settings)

    # Copy template files
    copy_template(path, name, description, version)


def get_version() -> str:
    """Get version from pyproject.toml.

    Returns
    -------
        str: Version
    """
    return PyProject().version
