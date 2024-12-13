"""Test server initialization and basic operations"""

import os
import pytest
import tempfile
import shutil
import logging
from contextlib import contextmanager
from unittest.mock import patch, MagicMock, AsyncMock
from mcp.server import request_ctx
from mcp.shared.context import RequestContext
from mcp.shared.session import BaseSession
from mcp.types import JSONRPCNotification
from lancedb_mcp.server import LanceDBServer, DatabaseError

@pytest.fixture
def temp_db_path():
    """Create a temporary database directory"""
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = os.path.join(temp_dir, "test.db")
        yield db_path
        # Directory will be automatically cleaned up

@pytest.fixture
def mock_session():
    """Mock MCP session for testing log messages"""
    session = AsyncMock(spec=BaseSession)
    session.send_notification = AsyncMock()
    session.send_notification.return_value = None
    return session

@pytest.fixture
def mock_request_context(mock_session):
    """Mock request context for testing"""
    context = RequestContext(
        request_id="test_request",
        meta=None,
        session=mock_session
    )
    return context

@contextmanager
def request_context(context):
    """Context manager for request context"""
    token = request_ctx.set(context)
    try:
        yield
    finally:
        request_ctx.reset(token)

@pytest.mark.asyncio
async def test_server_initialization(temp_db_path):
    """Test basic server initialization"""
    server = LanceDBServer(db_uri=temp_db_path)
    assert server.db_uri == temp_db_path
    assert server.db is None
    assert server.start_time is None
    
    # Test implementation details
    impl = await server.get_implementation()
    assert impl.name == "lancedb_mcp"
    assert impl.version == "0.1.0"

@pytest.mark.asyncio
async def test_server_start_stop(temp_db_path, mock_request_context):
    """Test server start and stop operations"""
    server = LanceDBServer(db_uri=temp_db_path)
    
    with request_context(mock_request_context):
        # Test start
        await server.start()
        assert server.db is not None
        assert server.start_time is not None
        assert os.path.exists(os.path.dirname(temp_db_path))
        
        # Verify log message was sent
        assert mock_request_context.session.send_notification.called
        notification = mock_request_context.session.send_notification.call_args[0][0]
        assert notification.method == "log"
        assert notification.params["level"] == "INFO"
        assert "Server started successfully" in notification.params["data"]
        
        # Test stop
        await server.stop()
        assert server.db is None

@pytest.mark.asyncio
async def test_invalid_path():
    """Test server with invalid path"""
    server = LanceDBServer(db_uri="/dev/null/invalid")
    with pytest.raises(DatabaseError):
        await server.start()

@pytest.mark.asyncio
async def test_table_operations(temp_db_path, caplog):
    """Test basic table operations with logging"""
    caplog.set_level(logging.INFO)

    server = LanceDBServer(db_uri=temp_db_path)
    await server.start()

    # Test create table
    result = await server.create_table("test_table", dimension=3)
    assert result["status"] == "success"
    assert "Created table test_table" in caplog.text

    # Test add vector
    result = await server.add_vector("test_table", [1.0, 2.0, 3.0])
    assert result["status"] == "success"
    assert "Added vector to table test_table" in caplog.text

@pytest.mark.asyncio
async def test_error_logging(temp_db_path, caplog):
    """Test error logging"""
    caplog.set_level(logging.ERROR)

    server = LanceDBServer(db_uri=temp_db_path)
    await server.start()

    # Test non-existent table
    with pytest.raises(DatabaseError):
        await server.add_vector("nonexistent", [1.0, 2.0, 3.0])
    assert "Table nonexistent not found" in caplog.text

@pytest.mark.asyncio
async def test_start_error_logging(mock_request_context):
    """Test logging during start failure"""
    server = LanceDBServer(db_uri="/dev/null/invalid")
    
    with request_context(mock_request_context), pytest.raises(DatabaseError):
        await server.start()
    
    # Verify error log message was sent
    assert mock_request_context.session.send_notification.called
    notification = mock_request_context.session.send_notification.call_args[0][0]
    assert notification.method == "log"
    assert notification.params["level"] == "ERROR"
    assert "Failed to start server" in notification.params["data"]
