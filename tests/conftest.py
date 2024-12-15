"""Test configuration."""

import os

# Set environment variables for testing
os.environ["LANCEDB_URI"] = ".lancedb"

# Configure pytest for async tests
pytest_plugins = ["pytest_asyncio"]
