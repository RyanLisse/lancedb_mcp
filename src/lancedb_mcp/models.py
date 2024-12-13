"""Data models for LanceDB MCP server."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class VectorData(BaseModel):
    """Vector data model for LanceDB operations."""

    vector: list[float]
    text: str | None = None
    metadata: dict[str, Any] | None = None
    model_config = ConfigDict(arbitrary_types_allowed=True)


class TableConfig(BaseModel):
    """Table configuration model."""

    name: str = Field(..., description="Name of the table")
    dimension: int = Field(..., description="Dimension of vectors in the table", gt=0)
    model_config = ConfigDict(arbitrary_types_allowed=True)


class SearchConfig(BaseModel):
    """Search configuration model."""

    table_name: str = Field(..., description="Name of the table to search in")
    query_vector: list[float] = Field(
        ..., description="Query vector for similarity search"
    )
    limit: int = Field(10, description="Maximum number of results to return", gt=0)
    model_config = ConfigDict(arbitrary_types_allowed=True)
