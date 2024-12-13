"""LanceDB server implementation."""

import asyncio
import logging
from pathlib import Path
from typing import Any

import lancedb
from mcp.server import Server
from mcp.shared.session import BaseSession
from pydantic import BaseModel


class DatabaseError(Exception):
    """Database error."""


class VectorData(BaseModel):
    """Vector data model."""

    vector: list[float]
    text: str
    metadata: dict[str, Any]


class TableConfig(BaseModel):
    """Table configuration."""

    name: str


class SearchConfig(BaseModel):
    """Search configuration."""

    table_name: str
    query_vector: list[float]
    limit: int = 10


class LanceDBServer(Server):
    """LanceDB server implementation."""

    def __init__(self, uri: str | Path = None):
        """Initialize LanceDB server.

        Args:
        ----
            uri: Database URI
        """
        self.uri = uri or str(Path.home() / "lancedb")
        self.db = None
        self.logger = logging.getLogger(__name__)
        self._tables = {}  # Keep track of created tables

    async def start(self):
        """Start the LanceDB server."""
        try:
            self.db = lancedb.connect(self.uri)
            self.logger.info("Connected to LanceDB at %s", self.uri)
        except Exception as err:
            self.logger.error("Failed to connect to LanceDB: %s", err)
            raise DatabaseError("Failed to connect to database") from err

    async def stop(self):
        """Stop the LanceDB server."""
        if self.db:
            try:
                await self.db.close()
            except Exception as err:
                self.logger.error("Failed to close database: %s", err)
            finally:
                self.db = None
                self._tables = {}  # Clear table cache
            self.logger.info("Disconnected from LanceDB")

    async def list_resources(self) -> list[dict[str, Any]]:
        """List available resources.

        Returns
        -------
            List of resources
        """
        if not self.db:
            raise DatabaseError("Database not connected")

        try:
            tables = self.db.table_names()
            return [{"id": table, "type": "table"} for table in tables]
        except Exception as err:
            self.logger.error("Failed to list tables: %s", err)
            raise DatabaseError("Failed to list tables") from err

    async def create_table(self, config: TableConfig) -> dict[str, str]:
        """Create a new table in the database.

        Args:
        ----
            config: Table configuration

        Returns:
        -------
            Status message
        """
        if not self.db:
            raise DatabaseError("Database not connected")

        try:
            schema = {"vector": "vector", "text": "string", "metadata": "json"}

            self._tables[config.name] = self.db.create_table(
                config.name, schema=schema, mode="overwrite"
            )

            self.logger.info("Created table %s", config.name)
            return {"status": "success"}
        except Exception as err:
            self.logger.error("Failed to create table: %s", err)
            raise DatabaseError("Failed to create table") from err

    async def add_vector(self, table_name: str, data: VectorData) -> dict[str, str]:
        """Add a vector to a table.

        Args:
        ----
            table_name: Table name
            data: Vector data

        Returns:
        -------
            Status message
        """
        if not self.db:
            raise DatabaseError("Database not connected")

        try:
            table = self._tables.get(table_name) or self.db[table_name]
            self._tables[table_name] = table  # Cache table

            # Convert data to dictionary for insertion
            vector_dict = {
                "vector": data.vector,
                "text": data.text,
                "metadata": data.metadata,
            }

            table.add([vector_dict])
            return {"status": "success"}
        except Exception as err:
            self.logger.error("Failed to add vector: %s", err)
            raise DatabaseError("Failed to add vector") from err

    async def search_vectors(self, config: SearchConfig) -> list[dict[str, Any]]:
        """Search for similar vectors.

        Args:
        ----
            config: Search configuration

        Returns:
        -------
            List of search results
        """
        if not self.db:
            raise DatabaseError("Database not connected")

        try:
            table = self._tables.get(config.table_name) or self.db[config.table_name]
            self._tables[config.table_name] = table  # Cache table

            results = table.search(config.query_vector).limit(config.limit).to_list()

            return [
                {
                    "vector": result["vector"],
                    "text": result["text"],
                    "metadata": result["metadata"],
                }
                for result in results
            ]
        except Exception as err:
            self.logger.error("Failed to search vectors: %s", err)
            raise DatabaseError("Failed to search vectors") from err

    async def handle_request(self, session: BaseSession) -> None:
        """Handle incoming requests.

        Args:
        ----
            session: Session instance
        """
        try:
            if session.request.get("type") == "list_resources":
                resources = await self.list_resources()
                await session.send_response(resources)

            elif session.request.get("type") == "create_table":
                config = TableConfig(**session.request.get("config", {}))
                result = await self.create_table(config)
                await session.send_response(result)

            elif session.request.get("type") == "add_vector":
                table_name = session.request.get("table_name")
                data = VectorData(**session.request.get("data", {}))
                result = await self.add_vector(table_name, data)
                await session.send_response(result)

            elif session.request.get("type") == "search_vectors":
                config = SearchConfig(**session.request.get("config", {}))
                results = await self.search_vectors(config)
                await session.send_response(results)

            else:
                await session.send_error(f"Unknown request: {session.request}")

        except Exception as err:
            self.logger.error("Error handling request: %s", err)
            await session.send_error(str(err))


async def main() -> None:
    """Run the server."""
    server = LanceDBServer()
    await server.start()

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await server.stop()


if __name__ == "__main__":
    asyncio.run(main())
