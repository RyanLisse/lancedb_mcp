"""Models for LanceDB MCP."""

from lancedb.pydantic import LanceModel, Vector
from pydantic import Field


class TableConfig(LanceModel):
    """Configuration for creating a table."""

    name: str = Field(..., min_length=1, description="Name of the table")
    dimension: int = Field(default=512, gt=0, description="Vector dimension")
    metric: str = Field(default="cosine", description="Distance metric")


class VectorData(LanceModel):
    """Vector data with text and optional URI."""

    vector: Vector = Field(..., dim=512, description="Vector data")
    text: str = Field(default="", description="Text description")
    uri: str | None = Field(default=None, description="Optional URI")


class SearchQuery(LanceModel):
    """Search query for finding similar vectors."""

    vector: Vector = Field(..., dim=512, description="Query vector")
    limit: int = Field(default=10, gt=0, description="Maximum number of results")
