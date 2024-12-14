"""LanceDB MCP initialization."""

import os
from pathlib import Path

from pydantic import BaseModel, Field

# Constants
PACKAGE_NAME = "lancedb_mcp"
VERSION = "0.1.0"


class Config(BaseModel):
    """Package configuration."""

    name: str = Field(default=PACKAGE_NAME)
    version: str = Field(default=VERSION)
    description: str | None = Field(default=None)


def get_package_directory() -> Path:
    """Get the package directory."""
    return Path(os.path.dirname(os.path.abspath(__file__)))


def get_version() -> str:
    """Get package version."""
    return VERSION
