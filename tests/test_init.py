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
"""
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text(pyproject_content)

    project = PyProject(pyproject_path)
    assert project.settings["project"]["name"] == "test-project"
    assert project.settings["project"]["version"] == "0.1.0"


def test_get_package_directory(tmp_path: Path) -> None:
    """Test package directory detection."""
    src_dir = tmp_path / "src" / "test_package"
    src_dir.mkdir(parents=True)
    (src_dir / "__init__.py").touch()

    package_dir = get_package_directory(tmp_path)
    assert package_dir == src_dir


def test_check_package_name() -> None:
    """Test package name validation."""
    # Test valid package names
    assert check_package_name("valid_name") is True
    assert check_package_name("valid-name") is True
    assert check_package_name("valid123") is True

    # Test invalid package names
    assert check_package_name("invalid name") is False
    assert check_package_name("123invalid") is False
    assert check_package_name("") is False


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

    update_pyproject_settings(tmp_path, "new-name", "New description", "1.0.0")
    pyproject = PyProject(pyproject_path)
    assert pyproject.settings["project"]["name"] == "new-name"
    assert pyproject.settings["project"]["description"] == "New description"
    assert pyproject.settings["project"]["version"] == "1.0.0"


def test_version_from_pyproject(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test that version is correctly read from pyproject.toml."""
    pyproject_content = """
[project]
name = "test-project"
version = "1.2.3"
description = "Test project"
"""
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text(pyproject_content)

    monkeypatch.setattr("pathlib.Path.cwd", lambda: tmp_path)
    assert get_version() == "1.2.3"


def test_pyproject_missing_file(tmp_path: Path) -> None:
    """Test handling of missing pyproject.toml file."""
    pyproject = PyProject(tmp_path / "pyproject.toml")
    assert pyproject.settings["project"]["version"] == "0.1.0"
