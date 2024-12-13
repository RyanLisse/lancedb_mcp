"""Main entry point for the LanceDB MCP server."""

import asyncio
import sys

from .server import LanceDBServer

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
    sys.exit(asyncio.run(main()))
