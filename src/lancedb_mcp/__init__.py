"""LanceDB MCP Server."""

from lancedb_mcp.models import SearchQuery, TableConfig, VectorData
from lancedb_mcp.server import set_db_uri

__version__ = "0.1.0"

__all__ = [
    "SearchQuery",
    "TableConfig",
    "VectorData",
    "set_db_uri",
]
