"""Main entry point for LanceDB MCP."""

import asyncio

from .cli import cli


async def main():
    """Execute the main entry point."""
    cli(standalone_mode=False)


if __name__ == "__main__":
    asyncio.run(main())
