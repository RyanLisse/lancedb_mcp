"""Server tests."""

from pathlib import Path

import pytest
from lancedb_mcp.models import TableConfig, VectorData
from lancedb_mcp.server import DatabaseError, LanceDBServer, LanceDBServerContext


@pytest.fixture
async def server(tmp_path: Path) -> LanceDBServer:
    """Server fixture."""
    server = LanceDBServer(uri=tmp_path)
    await server.start()
    yield server
    await server.stop()


@pytest.mark.asyncio
async def test_server_start_stop(tmp_path: Path) -> None:
    """Test server start and stop."""
    async with LanceDBServerContext(tmp_path) as server:
        assert server.db is not None
    assert server.db is None


@pytest.mark.asyncio
async def test_create_table(tmp_path: Path) -> None:
    """Test table creation."""
    async with LanceDBServerContext(tmp_path) as server:
        config = TableConfig(name="test_table", dimension=3)
        await server.create_table(config)


@pytest.mark.asyncio
async def test_add_vector(tmp_path: Path) -> None:
    """Test adding vector to table."""
    async with LanceDBServerContext(tmp_path) as server:
        # Create table
        config = TableConfig(name="test_table", dimension=3)
        await server.create_table(config)

        # Add vector
        data = VectorData(vector=[1.0, 0.0, 0.0], text="test")
        await server.add_vector("test_table", data)


@pytest.mark.asyncio
async def test_search_vectors(tmp_path: Path) -> None:
    """Test vector search."""
    async with LanceDBServerContext(tmp_path) as server:
        # Create table and add vector
        config = TableConfig(name="test_table", dimension=3)
        await server.create_table(config)
        data = VectorData(vector=[1.0, 0.0, 0.0], text="test")
        await server.add_vector("test_table", data)

        # Search vectors
        results = await server.search_vectors("test_table", [1.0, 0.0, 0.0])
        assert len(results) == 1
        assert results[0]["text"] == "test"


@pytest.mark.asyncio
async def test_error_logging(tmp_path: Path) -> None:
    """Test error logging."""
    async with LanceDBServerContext(tmp_path) as server:
        with pytest.raises(DatabaseError):
            await server.add_vector(
                "nonexistent_table", VectorData(vector=[1.0, 0.0, 0.0], text="test")
            )


@pytest.mark.asyncio
async def test_database_error(tmp_path: Path) -> None:
    """Test database error."""
    async with LanceDBServerContext(tmp_path) as server:
        server.db = None
        with pytest.raises(DatabaseError):
            await server.create_table(TableConfig(name="test", dimension=3))
