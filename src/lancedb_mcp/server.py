"""LanceDB MCP server."""

import logging
import os
import pathlib
from typing import Any

import lancedb
import mcp.server.stdio
import mcp.types as types
import pandas as pd
from lancedb.pydantic import pydantic_to_schema
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions

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


def get_db() -> lancedb.DBConnection:
    """Get database connection."""
    logger.info(f"Connecting to database at {DB_URI}")
    try:
        pathlib.Path(DB_URI).parent.mkdir(parents=True, exist_ok=True)
        return lancedb.connect(DB_URI)
    except Exception as err:
        logger.error(f"Failed to connect to database: {err}")
        raise err


# Create MCP server instance
server = Server("lancedb-server")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="create_table",
            description="Create a new table",
            arguments=[
                types.ToolArgument(
                    name="config",
                    description="Table configuration",
                    schema=TableConfig.model_json_schema(),
                )
            ],
        ),
        types.Tool(
            name="add_vector",
            description="Add a vector to a table",
            arguments=[
                types.ToolArgument(
                    name="table_name", description="Name of the table", type="string"
                ),
                types.ToolArgument(
                    name="data",
                    description="Vector data",
                    schema=VectorData.model_json_schema(),
                ),
            ],
        ),
        types.Tool(
            name="search_vectors",
            description="Search vectors in a table",
            arguments=[
                types.ToolArgument(
                    name="table_name", description="Name of the table", type="string"
                ),
                types.ToolArgument(
                    name="query",
                    description="Search query",
                    schema=SearchQuery.model_json_schema(),
                ),
            ],
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any]
) -> list[types.TextContent]:
    """Handle tool calls."""
    try:
        db = get_db()

        if name == "create_table":
            config = TableConfig.model_validate(arguments["config"])
            schema = pydantic_to_schema(VectorData)
            db.create_table(
                name=config.name,
                schema=schema,
                mode="overwrite",
            )
            logger.info(f"Created table {config.name}")
            return [types.TextContent(type="text", text="Table created successfully")]

        elif name == "add_vector":
            table_name = arguments["table_name"]
            data = VectorData.model_validate(arguments["data"])
            table = db.open_table(table_name)
            df = pd.DataFrame([data.model_dump()])
            table.add(df)
            logger.info(f"Added vector to table {table_name}")
            return [
                types.TextContent(
                    type="text", text=f"Added vector to table {table_name}"
                )
            ]

        elif name == "search_vectors":
            table_name = arguments["table_name"]
            query = SearchQuery.model_validate(arguments["query"])
            table = db.open_table(table_name)
            results = table.search(query.vector).limit(query.limit).to_pandas()
            logger.info(f"Searched table {table_name}")
            results_dict = results.to_dict(orient="records")
            # Convert numpy arrays to lists for JSON serialization
            for result in results_dict:
                if "_distance" in result:
                    result["score"] = float(result["_distance"])
                    del result["_distance"]
                if "vector" in result:
                    result["vector"] = result["vector"].tolist()
            return [types.TextContent(type="text", text=str(results_dict))]

        else:
            raise ValueError(f"Unknown tool: {name}")

    except FileNotFoundError:
        logger.error(f"Table {arguments.get('table_name')} not found")
        raise
    except Exception as err:
        logger.error(f"Failed to execute tool {name}: {err}")
        raise


async def run():
    """Run the server."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="lancedb-server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
