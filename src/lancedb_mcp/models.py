"""Models for LanceDB MCP."""

from typing import Annotated

from pydantic import BaseModel, Field, field_validator

Vector = Annotated[list[float], Field(min_length=1)]


class TableConfig(BaseModel):
    """Configuration for creating a table."""

    name: str = Field(..., min_length=1, description="Name of the table")
    dimension: int = Field(..., gt=0, description="Dimension of vectors in the table")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate table name."""
        if not v.isalnum():
            raise ValueError("Table name must be alphanumeric")
        return v


class VectorData(BaseModel):
    """Vector data for adding to a table."""

    vector: Vector = Field(..., description="Vector data")
    text: str = Field(..., min_length=1, description="Text associated with vector")


class SearchQuery(BaseModel):
    """Search query for finding similar vectors."""

    vector: Vector = Field(..., description="Query vector")
    limit: int = Field(
        default=10, gt=0, description="Maximum number of results to return"
    )
