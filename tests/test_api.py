"""FastAPI endpoint tests."""

import pytest
from fastapi.testclient import TestClient
from lancedb_mcp.models import SearchQuery, TableConfig, VectorData
from lancedb_mcp.server import app


@pytest.fixture
def test_client():
    """Test client fixture."""
    return TestClient(app)


def test_api_table_operations(test_client):
    """Test table API operations."""
    # Test table creation
    config = TableConfig(name="test_table", dimension=3)
    response = test_client.post("/table", json=config.model_dump())
    assert response.status_code == 200
    assert response.json()["message"] == "Created table test_table"

    # Test invalid table creation (empty name)
    with pytest.raises(ValueError):
        TableConfig(name="", dimension=3)

    # Test invalid dimension
    with pytest.raises(ValueError):
        TableConfig(name="test", dimension=0)


def test_api_vector_operations(test_client):
    """Test vector API operations."""
    # Create table first
    config = TableConfig(name="vector_test", dimension=3)
    response = test_client.post("/table", json=config.model_dump())
    assert response.status_code == 200

    # Test vector addition
    vector_data = VectorData(vector=[1.0, 2.0, 3.0], text="test vector")
    response = test_client.post("/vector/vector_test", json=vector_data.model_dump())
    assert response.status_code == 200
    assert response.json()["message"] == "Added vector to table"

    # Test invalid vector (empty)
    with pytest.raises(ValueError):
        VectorData(vector=[], text="test")

    # Test empty text
    with pytest.raises(ValueError):
        VectorData(vector=[1.0], text="")


def test_api_search_operations(test_client):
    """Test search API operations."""
    # Create and populate table
    config = TableConfig(name="search_test", dimension=3)
    response = test_client.post("/table", json=config.model_dump())
    assert response.status_code == 200

    vector_data = VectorData(vector=[1.0, 2.0, 3.0], text="test vector")
    response = test_client.post("/vector/search_test", json=vector_data.model_dump())
    assert response.status_code == 200

    # Test search
    query = SearchQuery(vector=[1.0, 2.0, 3.0])
    response = test_client.post("/search/search_test", json=query.model_dump())
    assert response.status_code == 200
    assert "results" in response.json()

    # Test custom k and distance
    query = SearchQuery(vector=[1.0, 2.0, 3.0], k=5, distance="l2")
    response = test_client.post("/search/search_test", json=query.model_dump())
    assert response.status_code == 200


def test_api_error_handling(test_client):
    """Test API error handling."""
    # Test nonexistent table
    vector_data = VectorData(vector=[1.0], text="test")
    response = test_client.post("/vector/nonexistent", json=vector_data.model_dump())
    assert response.status_code == 404
    assert "Table nonexistent not found" in response.json()["detail"]

    # Test invalid vector dimension
    config = TableConfig(name="dim_test", dimension=2)
    test_client.post("/table", json=config.model_dump())
    vector_data = VectorData(vector=[1.0, 2.0, 3.0], text="wrong dim")
    response = test_client.post("/vector/dim_test", json=vector_data.model_dump())
    assert response.status_code == 400

    # Test invalid search query
    with pytest.raises(ValueError):
        SearchQuery(vector=[], k=-1)
