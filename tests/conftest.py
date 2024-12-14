"""Test configuration."""

from pathlib import Path

import pytest_asyncio
from lancedb_mcp.server import LanceDBServerContext


@pytest_asyncio.fixture
async def server(tmp_path: Path):
    """Server fixture."""
    async with LanceDBServerContext(tmp_path) as server:
        yield server
