"""Test server functionality."""

from collections.abc import AsyncGenerator
from pathlib import Path

import pytest
from lancedb_mcp.models import TableConfig, VectorData
from lancedb_mcp.server import DatabaseError, LanceDBServer


@pytest.fixture
async def server(tmp_path: Path) -> AsyncGenerator[LanceDBServer, None]:
    """Create a test server instance."""
    server = LanceDBServer(uri=tmp_path)
    await server.start()
    try:
        yield server
    finally:
        await server.stop()


@pytest.mark.asyncio
async def test_server_start_stop(tmp_path: Path) -> None:
    """Test server start and stop."""
    server = LanceDBServer(uri=tmp_path)
    await server.start()
    assert server.db is not None
    await server.stop()
    assert server.db is None


@pytest.mark.asyncio
async def test_create_table(server: LanceDBServer) -> None:
    """Test table creation."""
    config = TableConfig(name="test_table", dimension=3)
    await server.create_table(config)
    assert await server.table_exists("test_table")


@pytest.mark.asyncio
async def test_add_vector(server: LanceDBServer) -> None:
    """Test adding vector to table."""
    # Create table
    config = TableConfig(name="test_table", dimension=3)
    await server.create_table(config)

    # Add vector
    vector = VectorData(vector=[1.0, 0.0, 0.0], text="test")
    await server.add_vector("test_table", vector)

    # Verify vector was added
    table = await server.get_table("test_table")
    assert len(table) == 1


@pytest.mark.asyncio
async def test_search_vectors(server: LanceDBServer) -> None:
    """Test vector search."""
    # Create table and add vector
    config = TableConfig(name="test_table", dimension=3)
    await server.create_table(config)

    vector = VectorData(vector=[1.0, 0.0, 0.0], text="test")
    await server.add_vector("test_table", vector)

    # Search for vector
    results = await server.search_vectors("test_table", [1.0, 0.0, 0.0])
    assert len(results) == 1
    assert results[0]["text"] == "test"


@pytest.mark.asyncio
async def test_error_logging(server: LanceDBServer) -> None:
    """Test error logging."""
    with pytest.raises(DatabaseError):
        await server.add_vector(
            "nonexistent_table", VectorData(vector=[1.0, 0.0, 0.0], text="test")
        )


@pytest.mark.asyncio
async def test_database_error() -> None:
    """Test database error handling."""
    server = LanceDBServer(uri="/nonexistent/path")
    with pytest.raises(DatabaseError):
        await server.start()
