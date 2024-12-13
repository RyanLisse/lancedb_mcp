"""Test fixtures."""

import contextlib
import os
import tempfile

import pytest
import pytest_asyncio
from lancedb_mcp.server import LanceDBServer
from mcp.shared.context import RequestContext


@contextlib.asynccontextmanager
async def request_context(context: RequestContext):
    """Request context manager."""
    from mcp.server import request_ctx

    token = request_ctx.set(context)
    try:
        yield
    finally:
        request_ctx.reset(token)


@pytest.fixture
def temp_db_path():
    """Temporary database path fixture."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield os.path.join(tmpdir, "test.db")


@pytest_asyncio.fixture
async def server(temp_db_path):
    """Server fixture."""
    server = LanceDBServer(uri=temp_db_path)
    context = RequestContext(request_id="test_request", meta=None, session=None)
    server.context = context

    # Start server before yielding
    await server.start()
    yield server

    # Stop server after test
    await server.stop()


@pytest.fixture
def mock_request_context():
    """Mock request context fixture."""
    return RequestContext(request_id="test_request", meta=None, session=None)
