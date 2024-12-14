"""LanceDB server implementation."""

import logging
from pathlib import Path
from typing import Any

import lancedb
import pyarrow as pa
from lancedb.table import LanceTable

from lancedb_mcp.models import TableConfig, VectorData


class DatabaseError(Exception):
    """Database error."""


class LanceDBServer:
    """LanceDB server."""

    def __init__(self, uri: Path) -> None:
        """Initialize server.

        Args:
        ----
            uri: Database URI.
        """
        self.uri = uri
        self.db: lancedb.LanceDBConnection | None = None
        self.tables: dict[str, LanceTable] = {}
        self.logger = logging.getLogger(__name__)

    async def start(self) -> None:
        """Start server."""
        try:
            self.db = lancedb.connect(str(self.uri))
            self.logger.info("Server started")
        except Exception as e:
            self.logger.error(f"Failed to start server: {e}")
            raise DatabaseError(f"Failed to start server: {e}") from e

    async def stop(self) -> None:
        """Stop server."""
        try:
            if self.db is not None:
                self.tables.clear()
                self.db = None
            self.logger.info("Server stopped")
        except Exception as e:
            self.logger.error(f"Failed to stop server: {e}")
            raise DatabaseError(f"Failed to stop server: {e}") from e

    async def create_table(self, config: TableConfig) -> None:
        """Create table.

        Args:
        ----
            config: Table configuration.
        """
        try:
            if self.db is None:
                raise DatabaseError("Database not connected")
            schema = pa.schema(
                [
                    pa.field("vector", pa.list_(pa.float32(), config.dimension)),
                    pa.field("text", pa.string()),
                ]
            )
            self.tables[config.name] = self.db.create_table(
                config.name,
                schema=schema,
                mode="overwrite",
            )
            self.logger.info(f"Created table {config.name}")
        except Exception as e:
            self.logger.error(f"Failed to create table: {e}")
            raise DatabaseError(f"Failed to create table: {e}") from e

    async def add_vector(self, table_name: str, data: VectorData) -> None:
        """Add vector to table.

        Args:
        ----
            table_name: Table name.
            data: Vector data.
        """
        try:
            if self.db is None:
                raise DatabaseError("Database not connected")
            if table_name not in self.tables:
                raise DatabaseError(f"Table {table_name} does not exist")
            table = self.tables[table_name]
            table.add(
                [
                    {
                        "vector": data.vector,
                        "text": data.text,
                    }
                ]
            )
            self.logger.info(f"Added vector to table {table_name}")
        except Exception as e:
            self.logger.error(f"Failed to add vector: {e}")
            raise DatabaseError(f"Failed to add vector: {e}") from e

    async def search_vectors(
        self, table_name: str, query_vector: list[float]
    ) -> list[dict[str, Any]]:
        """Search vectors.

        Args:
        ----
            table_name: Table name.
            query_vector: Query vector.

        Returns:
        -------
            List of search results.
        """
        try:
            if self.db is None:
                raise DatabaseError("Database not connected")
            if table_name not in self.tables:
                raise DatabaseError(f"Table {table_name} does not exist")
            table = self.tables[table_name]
            results = table.search(query_vector).limit(10).to_list()
            self.logger.info(f"Searched vectors in table {table_name}")
            return results
        except Exception as e:
            self.logger.error(f"Failed to search vectors: {e}")
            raise DatabaseError(f"Failed to search vectors: {e}") from e


class LanceDBServerContext:
    """LanceDB server context manager."""

    def __init__(self, uri: Path) -> None:
        """Initialize context manager.

        Args:
        ----
            uri: Database URI.
        """
        self._server = LanceDBServer(uri)

    async def __aenter__(self) -> LanceDBServer:
        """Enter context.

        Returns
        -------
            LanceDB server.
        """
        await self._server.start()
        return self._server

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit context."""
        await self._server.stop()
