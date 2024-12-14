"""CLI for LanceDB MCP."""

from pathlib import Path

import click

from lancedb_mcp import check_package_name, create_project


@click.command()
@click.option(
    "--path", type=click.Path(), default=".", help="Path to create project in"
)
@click.option("--name", required=True, help="Project name")
@click.option("--version", type=str, default="0.1.0", help="Project version")
@click.option("--description", required=True, help="Project description")
def cli(path: str, name: str, version: str, description: str) -> None:
    """Create new project."""
    if not check_package_name(name):
        click.echo("Invalid package name", err=True)
        raise click.Abort()

    project_path = Path(path) / "src" / name
    if project_path.exists():
        click.echo("Directory already exists", err=True)
        raise click.Abort()

    create_project(Path(path), name, description, version)
