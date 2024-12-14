"""FastAPI server for LanceDB."""

import logging
import os
from contextlib import asynccontextmanager
from typing import Annotated

import lancedb
import pyarrow as pa
from fastapi import Depends, FastAPI, HTTPException

from lancedb_mcp.models import SearchQuery, TableConfig, VectorData

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global database URI
DB_URI = os.getenv("LANCEDB_URI", ".lancedb")


async def get_db() -> lancedb.LanceDB:
    """Get database connection."""
    logger.info(f"Connecting to database at {DB_URI}")
    try:
        return lancedb.connect(DB_URI)
    except Exception as err:
        logger.error(f"Failed to connect to database: {err}")
        raise HTTPException(status_code=500, detail=str(err)) from err


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage database connection lifecycle."""
    yield


app = FastAPI(
    title="LanceDB MCP",
    description="Vector database operations via MCP protocol",
    lifespan=lifespan,
)

DB = Annotated[lancedb.LanceDB, Depends(get_db)]


@app.post("/table")
async def create_table(config: TableConfig, db: DB) -> dict[str, str]:
    """Create a new table."""
    try:
        schema = pa.schema(
            [
                ("vector", pa.list_(pa.float32(), config.dimension)),
                ("text", pa.string()),
            ]
        )
        db.create_table(config.name, schema=schema)
        logger.info(f"Created table {config.name}")
        return {"message": f"Created table {config.name}"}
    except Exception as err:
        logger.error(f"Failed to create table: {err}")
        raise HTTPException(status_code=500, detail=str(err)) from err


@app.post("/table/{table_name}/vector")
async def add_vector(table_name: str, data: VectorData, db: DB) -> dict[str, str]:
    """Add vector to table."""
    try:
        table = db.open_table(table_name)
        table.add(
            [
                {
                    "vector": data.vector,
                    "text": data.text,
                }
            ]
        )
        logger.info(f"Added vector to table {table_name}")
        return {"message": f"Added vector to table {table_name}"}
    except Exception as err:
        logger.error(f"Failed to add vector: {err}")
        raise HTTPException(status_code=500, detail=str(err)) from err


@app.post("/table/{table_name}/search")
async def search_vectors(
    table_name: str,
    query: SearchQuery,
    db: DB,
) -> list[dict[str, str | float]]:
    """Search vectors in table."""
    try:
        table = db.open_table(table_name)
        results = table.search(query.vector).limit(query.limit).to_list()
        logger.info(f"Searched table {table_name}")
        return results
    except Exception as err:
        logger.error(f"Failed to search vectors: {err}")
        raise HTTPException(status_code=500, detail=str(err)) from err
