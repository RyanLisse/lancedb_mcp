"""Test configuration."""

import logging
import shutil

import pytest
from fastapi.testclient import TestClient
from lancedb_mcp.server import app, set_db_uri

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def test_db_path(tmp_path):
    """Create test database path."""
    db_path = tmp_path / "test.db"
    db_path.mkdir(exist_ok=True)
    logger.info(f"Created test database path: {db_path}")
    set_db_uri(str(db_path))
    yield str(db_path)
    if db_path.exists():
        shutil.rmtree(db_path)
        logger.info(f"Cleaned up test database: {db_path}")


@pytest.fixture(scope="function")
def test_client(test_db_path):
    """Test client fixture."""
    with TestClient(app) as client:
        logger.info("Created test client")
        yield client
    logger.info("Cleaned up test client")
