"""Test server functionality."""

import os
import tempfile

import numpy as np
import pytest
from lancedb_mcp.models import SearchQuery, TableConfig, VectorData
from lancedb_mcp.server import set_db_uri
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


@pytest.fixture
async def client():
    """Create a test client."""
    # Create a temporary directory for the test database
    temp_dir = tempfile.mkdtemp()
    test_db = os.path.join(temp_dir, "test.lance")
    set_db_uri(test_db)

    # Create server parameters
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "lancedb_mcp.server"],
        env={"LANCEDB_URI": test_db},
    )

    # Create client session
    read, write = await stdio_client(server_params).__aenter__()
    session = await ClientSession(read, write).__aenter__()
    await session.initialize()

    yield session

    # Cleanup
    await session.__aexit__(None, None, None)
    await stdio_client(server_params).__aexit__(None, None, None)
    os.rmdir(temp_dir)


@pytest.mark.asyncio
async def test_create_table(client):
    """Test creating a table."""
    config = TableConfig(name="test_table", dimension=512)
    tools = await client.list_tools()
    assert len(tools) == 3
    result = await client.call_tool("create_table", {"config": config.model_dump()})
    assert "Table created successfully" in result[0].text


@pytest.mark.asyncio
async def test_add_vector(client):
    """Test adding a vector."""
    # Create table first
    config = TableConfig(name="test_table", dimension=512)
    await client.call_tool("create_table", {"config": config.model_dump()})

    # Add test vector
    vector = np.random.rand(512).tolist()
    data = VectorData(vector=vector, text="test vector")
    result = await client.call_tool(
        "add_vector", {"table_name": "test_table", "data": data.model_dump()}
    )
    assert "Added vector to table test_table" in result[0].text


@pytest.mark.asyncio
async def test_search_vectors(client):
    """Test searching vectors."""
    # Create table and add vector
    config = TableConfig(name="test_table", dimension=512)
    await client.call_tool("create_table", {"config": config.model_dump()})

    # Add test vector
    vector = np.random.rand(512).tolist()
    data = VectorData(vector=vector, text="test vector")
    await client.call_tool(
        "add_vector", {"table_name": "test_table", "data": data.model_dump()}
    )

    # Test search
    query = SearchQuery(vector=vector, limit=5)
    result = await client.call_tool(
        "search_vectors", {"table_name": "test_table", "query": query.model_dump()}
    )
    assert "test vector" in result[0].text
