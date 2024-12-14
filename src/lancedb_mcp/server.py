"""FastAPI server for LanceDB."""

import logging
import os
from contextlib import asynccontextmanager

import lancedb
import pyarrow as pa
from fastapi import FastAPI, HTTPException

from lancedb_mcp.models import SearchQuery, TableConfig, VectorData

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global database URI
DB_URI = os.getenv("LANCEDB_URI", ".lancedb")


def set_db_uri(uri: str) -> None:
    """Set the database URI."""
    global DB_URI
    DB_URI = uri
    logger.info(f"Set database URI to {uri}")


def get_db() -> lancedb.LanceDB:
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


app = FastAPI(lifespan=lifespan)


@app.post("/table")
async def create_table(config: TableConfig) -> dict[str, str]:
    """Create a new table."""
    db = get_db()
    try:
        # Create empty table with PyArrow schema
        empty_data = pa.Table.from_arrays(
            [
                pa.array([], type=pa.list_(pa.float32(), config.dimension)),
                pa.array([], type=pa.string()),
            ],
            names=["vector", "text"],
        )
        logger.info(f"Creating table {config.name}")
        db.create_table(config.name, data=empty_data, mode="overwrite")
        return {"message": f"Created table {config.name}"}
    except Exception as err:
        logger.error(f"Failed to create table: {err}")
        raise HTTPException(status_code=400, detail=str(err)) from err


@app.post("/vector/{table_name}")
async def add_vector(table_name: str, data: VectorData) -> dict[str, str]:
    """Add vector to table."""
    db = get_db()
    try:
        table = db[table_name]
        logger.info(f"Adding vector to table {table_name}")
        table.add([{"vector": data.vector, "text": data.text}])
        return {"message": "Added vector to table"}
    except Exception as err:
        logger.error(f"Failed to add vector: {err}")
        if "does not exist" in str(err):
            raise HTTPException(
                status_code=404, detail=f"Table {table_name} not found"
            ) from err
        raise HTTPException(status_code=400, detail=str(err)) from err


@app.post("/search/{table_name}")
async def search_vectors(table_name: str, query: SearchQuery) -> dict[str, list]:
    """Search vectors in table."""
    db = get_db()
    try:
        table = db[table_name]
        logger.info(f"Searching in table {table_name}")
        results = table.search(query.vector).limit(query.limit).to_list()
        return {"results": results}
    except Exception as err:
        logger.error(f"Failed to search vectors: {err}")
        if "does not exist" in str(err):
            raise HTTPException(
                status_code=404, detail=f"Table {table_name} not found"
            ) from err
        raise HTTPException(status_code=400, detail=str(err)) from err
