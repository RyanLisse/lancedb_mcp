"""Test initialization functionality."""

from pathlib import Path

import pytest
from lancedb_mcp import (
    PyProject,
    check_package_name,
    copy_template,
    create_project,
    get_package_directory,
    update_pyproject_settings,
)


@pytest.fixture
def template_dir(tmp_path: Path) -> Path:
    """Create a template directory with required files."""
    template_dir = tmp_path / "template"
    template_dir.mkdir()
    (template_dir / "__init__.py.jinja2").write_text("# Template __init__.py")
    (template_dir / "server.py.jinja2").write_text("# Template server.py")
    (template_dir / "README.md.jinja2").write_text("# Template README.md")
    return template_dir


def test_get_package_directory(tmp_path: Path) -> None:
    """Test package directory detection."""
    src_dir = tmp_path / "src" / "test_package"
    src_dir.mkdir(parents=True)
    (src_dir / "__init__.py").touch()

    result = get_package_directory(tmp_path)
    assert result == src_dir


def test_check_package_name() -> None:
    """Test package name validation."""
    # Valid names
    check_package_name("valid_name")
    check_package_name("valid-name")
    check_package_name("valid123")

    # Invalid names should raise SystemExit
    with pytest.raises(SystemExit):
        check_package_name("invalid name")

    with pytest.raises(SystemExit):
        check_package_name("invalid@name")


def test_update_pyproject_settings(tmp_path: Path) -> None:
    """Test updating pyproject.toml settings."""
    settings = {
        "name": "test-project",
        "version": "0.1.0",
        "description": "Test project",
    }
    update_pyproject_settings(tmp_path, settings)

    pyproject = PyProject(tmp_path / "pyproject.toml")
    assert pyproject.data["project"]["name"] == "test-project"
    assert pyproject.data["project"]["version"] == "0.1.0"
    assert pyproject.data["project"]["description"] == "Test project"


def test_copy_template(
    tmp_path: Path, template_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test copying template files."""
    # Create project structure
    src_dir = tmp_path / "src" / "test_package"
    src_dir.mkdir(parents=True)
    (src_dir / "__init__.py").touch()

    # Create pyproject.toml
    pyproject_content = """
[project]
name = "test-project"
version = "0.1.0"
description = "Test project"

[project.scripts]
test-script = "test_project.__main__:main"
"""
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text(pyproject_content)

    monkeypatch.setattr("lancedb_mcp.__init__.Path.__file__", str(template_dir.parent))
    copy_template(
        path=tmp_path,
        name="test-project",
        description="Test project",
        version="0.1.0",
    )

    assert (src_dir / "server.py").exists()
    assert (tmp_path / "README.md").exists()


def test_create_project(
    tmp_path: Path, template_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test project creation."""
    monkeypatch.setattr("lancedb_mcp.__init__.Path.__file__", str(template_dir.parent))
    create_project(
        path=tmp_path,
        name="test-project",
        description="Test project",
        version="0.1.0",
    )

    assert (tmp_path / "src" / "test_project" / "server.py").exists()
    assert (tmp_path / "README.md").exists()
    assert (tmp_path / "pyproject.toml").exists()
