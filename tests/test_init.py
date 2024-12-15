"""Tests for __init__.py functionality."""


from lancedb_mcp import TableConfig, __version__


def test_config():
    """Test TableConfig model."""
    config = TableConfig(name="test_table")
    assert config.name == "test_table"
    assert isinstance(config.dimension, int)


def test_version():
    """Test version getter."""
    assert __version__ == "0.1.0"
