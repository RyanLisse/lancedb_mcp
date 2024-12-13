"""Command line interface for LanceDB MCP."""

from pathlib import Path

import click


@click.command()
@click.option(
    "--path",
    type=click.Path(),
    default=".",
    help="Path to create project in",
)
@click.option(
    "--name",
    type=str,
    default="lancedb-mcp",
    help="Project name",
)
@click.option(
    "--version",
    type=str,
    default="0.1.0",
    help="Project version",
)
@click.option(
    "--description",
    type=str,
    default="LanceDB MCP Server",
    help="Project description",
)
def cli(path: str, name: str, version: str, description: str) -> None:
    """Create a new LanceDB MCP server project."""
    from lancedb_mcp import create_project

    create_project(Path(path), name, description, version)
