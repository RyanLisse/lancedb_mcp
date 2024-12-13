"""Test main module functionality."""

from click.testing import CliRunner
from lancedb_mcp.cli import cli


def test_cli() -> None:
    """Test cli command."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(
            cli,
            ["--name", "test-project", "--description", "Test project"],
        )
        assert result.exit_code == 0


def test_cli_invalid_name() -> None:
    """Test cli with invalid name."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(
            cli,
            ["--name", "invalid name", "--description", "Test project"],
        )
        assert result.exit_code == 1
        assert "Invalid package name" in result.output


def test_cli_existing_directory() -> None:
    """Test cli with existing directory."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Create project first time
        result = runner.invoke(
            cli,
            ["--name", "test-project", "--description", "Test project"],
        )
        assert result.exit_code == 0

        # Try to create project again
        result = runner.invoke(
            cli,
            ["--name", "test-project", "--description", "Test project"],
        )
        assert result.exit_code == 1
        assert "Directory already exists" in result.output
