"""Test LanceDB server operations"""

import os
import pytest
import tempfile
import asyncio
from unittest.mock import AsyncMock, MagicMock
from lancedb_mcp.server import LanceDBServer, DatabaseError

@pytest.fixture
async def server():
    """Create a test server instance"""
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = os.path.join(temp_dir, "test.db")
        server = LanceDBServer(db_uri=db_path)
        await server.start()
        try:
            yield server
        finally:
            await server.stop()

@pytest.mark.asyncio
async def test_empty_resources():
    """Test listing resources when database is empty."""
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = os.path.join(temp_dir, "test.db")
        server = LanceDBServer(db_uri=db_path)
        await server.start()
        try:
            resources = await server.list_resources()
            assert len(resources) == 0
        finally:
            await server.stop()

@pytest.mark.asyncio
async def test_create_table():
    """Test creating a new table."""
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = os.path.join(temp_dir, "test.db")
        server = LanceDBServer(db_uri=db_path)
        await server.start()
        try:
            table_name = "test_vectors"
            dimension = 3
            result = await server.create_table(table_name=table_name, dimension=dimension)
            assert result["status"] == "success"
            
            # Verify table was created
            resources = await server.list_resources()
            assert len(resources) == 1
            assert resources[0].id == table_name
        finally:
            await server.stop()

@pytest.mark.asyncio
async def test_add_and_search_vectors():
    """Test adding and searching vectors."""
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = os.path.join(temp_dir, "test.db")
        server = LanceDBServer(db_uri=db_path)
        await server.start()
        try:
            # Create table
            table_name = "test_vectors"
            dimension = 3
            await server.create_table(table_name=table_name, dimension=dimension)
            
            # Add vectors
            vectors = [
                [1.0, 2.0, 3.0],
                [4.0, 5.0, 6.0],
                [7.0, 8.0, 9.0]
            ]
            for vector in vectors:
                result = await server.add_vector(table_name=table_name, vector=vector)
                assert result["status"] == "success"
            
            # Search vectors
            query_vector = [1.0, 2.0, 3.0]
            limit = 2
            results = await server.search_vectors(table_name=table_name, query_vector=query_vector, limit=limit)
            assert len(results) == limit
        finally:
            await server.stop()

@pytest.mark.asyncio
async def test_nonexistent_table():
    """Test error handling for non-existent tables."""
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = os.path.join(temp_dir, "test.db")
        server = LanceDBServer(db_uri=db_path)
        await server.start()
        try:
            table_name = "nonexistent_table"
            
            # Try to add vector to non-existent table
            with pytest.raises(DatabaseError) as exc_info:
                await server.add_vector(table_name=table_name, vector=[1.0, 2.0, 3.0])
            assert "not found" in str(exc_info.value)
            
            # Try to search in non-existent table
            with pytest.raises(DatabaseError) as exc_info:
                await server.search_vectors(table_name=table_name, query_vector=[1.0, 2.0, 3.0])
            assert "not found" in str(exc_info.value)
        finally:
            await server.stop()

@pytest.mark.asyncio
async def test_invalid_vector_dimension():
    """Test error handling for vectors with wrong dimensions."""
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = os.path.join(temp_dir, "test.db")
        server = LanceDBServer(db_uri=db_path)
        await server.start()
        try:
            # Create table with dimension 3
            table_name = "test_vectors"
            dimension = 3
            await server.create_table(table_name=table_name, dimension=dimension)
            
            # Try to add vector with wrong dimension
            with pytest.raises(DatabaseError) as exc_info:
                await server.add_vector(table_name=table_name, vector=[1.0, 2.0])
            assert "dimension" in str(exc_info.value).lower()
            
            # Try to search with wrong dimension
            with pytest.raises(DatabaseError) as exc_info:
                await server.search_vectors(table_name=table_name, query_vector=[1.0, 2.0])
            assert "dimension" in str(exc_info.value).lower()
        finally:
            await server.stop()

@pytest.mark.asyncio
async def test_concurrent_table_access():
    """Test concurrent access to the same table."""
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = os.path.join(temp_dir, "test.db")
        server = LanceDBServer(db_uri=db_path)
        await server.start()
        try:
            # Create table
            table_name = "test_vectors"
            dimension = 3
            await server.create_table(table_name=table_name, dimension=dimension)
            
            # Add vectors concurrently
            async def add_vector(vector):
                return await server.add_vector(table_name=table_name, vector=vector)
            
            vectors = [
                [float(i), float(i+1), float(i+2)]
                for i in range(10)
            ]
            
            # Add vectors concurrently and wait for all to complete
            tasks = [add_vector(vector) for vector in vectors]
            results = await asyncio.gather(*tasks)
            
            # Verify all adds were successful
            assert all(result["status"] == "success" for result in results)
            
            # Search vectors concurrently
            async def search_vectors(query_vector):
                return await server.search_vectors(table_name=table_name, query_vector=query_vector, limit=2)
            
            # Search with different query vectors concurrently
            search_tasks = [search_vectors(vector) for vector in vectors[:3]]
            search_results = await asyncio.gather(*search_tasks)
            
            # Verify all searches returned results
            assert all(len(result) == 2 for result in search_results)
        finally:
            await server.stop()