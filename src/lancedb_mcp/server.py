"""
LanceDB MCP Server Implementation
Provides vector database operations through MCP protocol
"""

import asyncio
import logging
import json
import time
from typing import Dict, List, Optional, Any, Union, AsyncIterator
import os
from contextlib import contextmanager, suppress
from datetime import datetime, timezone, timedelta

import lancedb
import numpy as np
import pandas as pd
from mcp.server import Server, request_ctx
from mcp.server.models import InitializationOptions
from mcp.types import (
    Resource, TextContent, ServerCapabilities,
    ToolsCapability, ResourcesCapability, Tool,
    Implementation, ClientCapabilities, CallToolResult,
    JSONRPCNotification
)
from pydantic import AnyUrl, BaseModel, Field, ConfigDict
import pyarrow as pa

logger = logging.getLogger('mcp_lancedb_server')

class VectorData(BaseModel):
    """Vector data model for LanceDB operations"""
    vector: List[float]
    text: Optional[str] = None
    metadata: Optional[Dict] = None
    model_config = ConfigDict(arbitrary_types_allowed=True)

class DatabaseError(Exception):
    """Base exception for database operations"""
    pass

class LanceDBServer(Server):
    """LanceDB MCP Server implementation"""
    
    def __init__(self, db_uri: str = "data/vectors"):
        """Initialize the LanceDB server.
        
        Args:
            db_uri: Path to the database directory
        """
        super().__init__(name="lancedb_mcp")
        self.db_uri = db_uri
        self.db = None
        self.tables: Dict[str, Any] = {}
        self.start_time = None
        self._lock = asyncio.Lock()

    def _get_timestamp(self) -> str:
        """Get current UTC timestamp in ISO format"""
        return datetime.now(timezone.utc).isoformat()

    async def _send_log(self, level: str, message: str):
        """Send log message to client if context available"""
        logger.log(getattr(logging, level), message)
        try:
            ctx = request_ctx.get()
            if hasattr(ctx, 'session'):
                notification = JSONRPCNotification(
                    jsonrpc="2.0",
                    method="log",
                    params={"level": level, "data": message}
                )
                await ctx.session.send_notification(notification)
        except LookupError:
            # No request context available
            pass

    async def start(self) -> None:
        """Start the server and connect to the database"""
        try:
            async with self._lock:
                # Create database directory if it doesn't exist
                db_path = os.path.abspath(self.db_uri)
                db_dir = os.path.dirname(db_path)
                if db_dir:  # Only create directory if db_uri has a parent directory
                    os.makedirs(db_dir, exist_ok=True)
                
                try:
                    await self._send_log("INFO", f"Connecting to database at {db_path}")
                    
                    # Create an empty DataFrame to initialize the database
                    empty_df = pd.DataFrame({"dummy": [0]})  # Need at least one row
                    self.db = await asyncio.to_thread(lambda: lancedb.connect(db_path))
                    await asyncio.to_thread(lambda: self.db.create_table("_init", empty_df, mode="overwrite"))
                    await self._send_log("INFO", "Connected to database")
                    
                    # Initialize tables dict
                    self.tables = {}
                    
                    # Get list of existing tables
                    table_names = await asyncio.to_thread(lambda: list(self.db.table_names()))
                    table_names = [name for name in table_names if name != "_init"]  # Exclude init table
                    await self._send_log("INFO", f"Found {len(table_names)} existing tables")
                    
                    # Open existing tables
                    for table_name in table_names:
                        try:
                            self.tables[table_name] = await asyncio.to_thread(
                                self.db.open_table, table_name
                            )
                            await self._send_log("INFO", f"Opened table {table_name}")
                        except Exception as e:
                            await self._send_log("WARNING", f"Failed to open table {table_name}: {str(e)}")
                    
                    # Set server start time
                    self.start_time = self._get_timestamp()
                    await self._send_log("INFO", "Server started successfully")
                    
                except Exception as e:
                    self.db = None
                    await self._send_log("ERROR", f"Failed to connect to database: {str(e)}")
                    raise DatabaseError(f"Failed to connect to database: {str(e)}")
                
        except Exception as e:
            await self._send_log("ERROR", f"Failed to start server: {str(e)}")
            raise DatabaseError(f"Failed to start server: {str(e)}")

    async def stop(self):
        """Stop the LanceDB server"""
        try:
            async with self._lock:
                # Clear all table references first
                for table_name in list(self.tables.keys()):
                    self.tables[table_name] = None
                self.tables.clear()
                
                # Close database connection
                if self.db is not None:
                    self.db = None
                    
                self.start_time = None
                await self._send_log("INFO", "Server stopped successfully")
        except Exception as e:
            await self._send_log("ERROR", f"Error stopping server: {str(e)}")
            raise DatabaseError(f"Error stopping server: {str(e)}")

    async def get_implementation(self) -> Implementation:
        """Get server implementation details"""
        return Implementation(
            name="lancedb_mcp",
            version="0.1.0",
            vendor="LanceDB"
        )

    async def get_capabilities(self) -> ServerCapabilities:
        """Get server capabilities"""
        return ServerCapabilities(
            tools=ToolsCapability(
                tools=[
                    Tool(
                        name="create_table",
                        description="Create a new vector table",
                        parameters={
                            "table_name": "string",
                            "dimension": "integer"
                        }
                    ),
                    Tool(
                        name="add_vector",
                        description="Add a vector to a table",
                        parameters={
                            "table_name": "string",
                            "vector": "List[float]",
                            "metadata": "Optional[Dict]"
                        }
                    ),
                    Tool(
                        name="search_vectors",
                        description="Search for similar vectors",
                        parameters={
                            "table_name": "string",
                            "query_vector": "List[float]",
                            "limit": "integer"
                        }
                    )
                ]
            ),
            resources=ResourcesCapability(
                supports_create=True,
                supports_delete=True,
                supports_update=True
            )
        )

    async def list_resources(self) -> List[Resource]:
        """List available tables"""
        try:
            async with self._lock:
                if not self.db:
                    return []  # Return empty list if database is not initialized
                
                tables = []
                table_names = await asyncio.to_thread(lambda: list(self.db.table_names()))
                table_names = [name for name in table_names if name != "_init"]  # Exclude init table
                for table_name in table_names:
                    tables.append(Resource(
                        id=table_name,
                        name=table_name,
                        uri=f"table://{table_name}",
                        type="table",
                        content=TextContent(
                            type="text",
                            text=f"Vector table: {table_name}"
                        )
                    ))
                return tables
        except Exception as e:
            await self._send_log("ERROR", f"Failed to list tables: {str(e)}")
            raise DatabaseError(f"Failed to list tables: {str(e)}")

    def _validate_db_state(self) -> bool:
        """Validate database connection state"""
        if not self.db:
            raise DatabaseError("Database not initialized")
        return True

    async def create_table(self, table_name: str, dimension: int) -> Dict[str, str]:
        """Create a new table with the specified name and vector dimension"""
        try:
            async with self._lock:
                self._validate_db_state()
                if dimension <= 0:
                    raise ValueError("Vector dimension must be positive")
                
                # Create schema with proper types
                schema = pa.schema([
                    pa.field("vector", pa.list_(pa.float32(), dimension)),
                    pa.field("text", pa.string(), nullable=True),
                    pa.field("metadata", pa.string(), nullable=True)  # Store metadata as JSON string
                ])
                
                # Create empty DataFrame with proper vector type
                empty_data = pd.DataFrame({
                    "vector": [[0.0] * dimension],  # Initialize with a zero vector
                    "text": [None],
                    "metadata": [None]
                })
                
                # Create the table
                try:
                    self.tables[table_name] = await asyncio.to_thread(
                        lambda: self.db.create_table(
                            table_name,
                            data=empty_data,
                            schema=schema,
                            mode="overwrite"
                        )
                    )
                    await self._send_log("INFO", f"Created table {table_name}")
                    return {"status": "success", "message": f"Created table {table_name}"}
                except Exception as e:
                    await self._send_log("ERROR", f"Failed to create table {table_name}: {str(e)}")
                    raise DatabaseError(f"Failed to create table: {str(e)}")
        except Exception as e:
            await self._send_log("ERROR", f"Failed to create table {table_name}: {str(e)}")
            raise DatabaseError(f"Failed to create table: {str(e)}")

    async def add_vector(self, table_name: str, vector: List[float], text: Optional[str] = None, metadata: Optional[Dict] = None) -> Dict[str, str]:
        """Add a vector to the specified table"""
        try:
            async with self._lock:
                self._validate_db_state()

                if table_name not in self.tables:
                    # Try to open the table if it exists
                    try:
                        self.tables[table_name] = await asyncio.to_thread(self.db.open_table, table_name)
                    except Exception as e:
                        raise DatabaseError(f"Table {table_name} not found: {str(e)}")

                table = self.tables[table_name]
                table_schema = await asyncio.to_thread(lambda: table.schema)
                expected_dim = table_schema.field("vector").type.list_size
                
                if len(vector) != expected_dim:
                    raise ValueError(f"Vector dimension mismatch: expected {expected_dim}, got {len(vector)}")

                # Convert metadata to JSON string if present
                metadata_str = json.dumps(metadata) if metadata else None

                # Create data frame with proper types
                data = {
                    "vector": [vector],
                    "text": [text] if text else [None],
                    "metadata": [metadata_str] if metadata_str else [None]
                }
                df = pd.DataFrame(data)

                # Add to table
                try:
                    await asyncio.to_thread(lambda: table.add(df))
                    await self._send_log("INFO", f"Added vector to table {table_name}")
                    return {"status": "success", "message": f"Added vector to table {table_name}"}
                except Exception as e:
                    await self._send_log("ERROR", f"Failed to add vector to table {table_name}: {str(e)}")
                    raise DatabaseError(f"Failed to add vector to table {table_name}: {str(e)}")

        except Exception as e:
            await self._send_log("ERROR", f"Failed to add vector: {str(e)}")
            raise DatabaseError(str(e))

    async def search_vectors(
        self, table_name: str, query_vector: List[float], limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Search for similar vectors in the specified table"""
        try:
            async with self._lock:
                self._validate_db_state()

                if table_name not in self.tables:
                    # Try to open the table if it exists
                    try:
                        self.tables[table_name] = await asyncio.to_thread(self.db.open_table, table_name)
                    except Exception:
                        raise DatabaseError(f"Table {table_name} not found")

                table = self.tables[table_name]
                table_schema = await asyncio.to_thread(lambda: table.schema)
                expected_dim = table_schema.field("vector").type.list_size
                
                if len(query_vector) != expected_dim:
                    raise ValueError(f"Query vector dimension mismatch: expected {expected_dim}, got {len(query_vector)}")

                # Perform search
                results = await asyncio.to_thread(
                    lambda: table.search(query_vector).limit(limit).to_list()
                )
                await self._send_log("INFO", f"Found {len(results)} results in table {table_name}")
                return results

        except Exception as e:
            await self._send_log("ERROR", f"Failed to search vectors: {str(e)}")
            raise DatabaseError(f"Failed to search vectors: {str(e)}")

async def main():
    """Run the LanceDB MCP server"""
    server = LanceDBServer()
    await server.start()
    try:
        # Keep the server running
        while True:
            await asyncio.sleep(1)
    finally:
        await server.stop()

if __name__ == "__main__":
    asyncio.run(main())