"""Tests for __init__.py functionality."""

from pathlib import Path

import pytest
from lancedb_mcp import (
    PyProject,
    check_package_name,
    get_package_directory,
    get_version,
    update_pyproject_settings,
)


def test_pyproject_class(tmp_path: Path) -> None:
    """Test PyProject class functionality."""
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

    project = PyProject(pyproject_path)
    assert project.name == "test-project"
    assert project.first_binary == "test-script"


def test_get_package_directory(tmp_path: Path) -> None:
    """Test package directory detection."""
    src_dir = tmp_path / "src" / "test_package"
    src_dir.mkdir(parents=True)
    (src_dir / "__init__.py").touch()

    result = get_package_directory(tmp_path)
    assert result == src_dir


def test_check_package_name() -> None:
    """Test package name validation."""
    # Valid names should not raise SystemExit
    check_package_name("valid-name")
    check_package_name("valid_name")
    check_package_name("valid123")

    # Invalid names should raise SystemExit
    with pytest.raises(SystemExit):
        check_package_name("Invalid Name")

    with pytest.raises(SystemExit):
        check_package_name("invalid@name")


def test_update_pyproject_settings(tmp_path: Path) -> None:
    """Test updating pyproject.toml settings."""
    pyproject_content = """
[project]
name = "test-project"
version = "0.1.0"
description = "Old description"
"""
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text(pyproject_content)

    settings = {
        "version": "1.0.0",
        "description": "New description",
    }
    update_pyproject_settings(tmp_path, settings)

    project = PyProject(pyproject_path)
    assert project.data["project"]["version"] == "1.0.0"
    assert project.data["project"]["description"] == "New description"


def test_version_from_pyproject(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test that version is correctly read from pyproject.toml."""
    pyproject_content = """
[project]
name = "test-project"
version = "1.0.0"
"""
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text(pyproject_content)

    monkeypatch.chdir(tmp_path)
    assert get_version() == "1.0.0"


def test_pyproject_load() -> None:
    """Test loading PyProject configuration."""
    project = PyProject()
    assert isinstance(project.data, dict)


def test_pyproject_missing_file(tmp_path: Path) -> None:
    """Test handling of missing pyproject.toml file."""
    with pytest.raises(FileNotFoundError):
        PyProject(tmp_path / "nonexistent.toml")._load_config()


def test_pyproject_custom_path(tmp_path: Path) -> None:
    """Test loading PyProject from custom path."""
    pyproject_content = """
[project]
name = "test"
"""
    pyproject_path = tmp_path / "custom_pyproject.toml"
    pyproject_path.write_text(pyproject_content)
    project = PyProject(pyproject_path)
    assert project.data["project"]["name"] == "test"
