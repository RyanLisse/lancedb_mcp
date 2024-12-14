"""Models for LanceDB MCP."""


from pydantic import BaseModel, Field


class TableConfig(BaseModel):
    """Configuration for creating a table."""

    name: str = Field(..., min_length=1)
    dimension: int = Field(..., gt=0)


class VectorData(BaseModel):
    """Vector data for adding to a table."""

    vector: list[float] = Field(..., min_length=1)
    text: str = Field(..., min_length=1)


class SearchQuery(BaseModel):
    """Search query for finding similar vectors."""

    vector: list[float] = Field(..., min_length=1)
    limit: int = Field(default=10, gt=0)
