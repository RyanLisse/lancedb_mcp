# LanceDB MCP Server

## Overview
A Model Context Protocol (MCP) server implementation for LanceDB vector database operations. This server enables efficient vector storage, similarity search, and management of vector embeddings with associated metadata.

## Components

### Resources
The server exposes vector database tables as resources:
- `table://{name}`: A vector database table that stores embeddings and metadata
  - Configurable vector dimensions
  - Text metadata support
  - Efficient similarity search capabilities

### API Endpoints

#### Table Management
- `POST /table`
   - Create a new vector table
   - Input:
     ```python
     {
       "name": "my_table",      # Table name
       "dimension": 768         # Vector dimension
     }
     ```

#### Vector Operations
- `POST /table/{table_name}/vector`
   - Add vector data to a table
   - Input:
     ```python
     {
       "vector": [0.1, 0.2, ...],  # Vector data
       "text": "associated text"    # Metadata
     }
     ```

- `POST /table/{table_name}/search`
   - Search for similar vectors
   - Input:
     ```python
     {
       "vector": [0.1, 0.2, ...],  # Query vector
       "limit": 10                  # Number of results
     }
     ```

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/lancedb_mcp.git
cd lancedb_mcp

# Install dependencies using uv
uv pip install -e .
```

## Usage with Claude Desktop

```bash
# Add the server to your claude_desktop_config.json
"mcpServers": {
  "lancedb": {
    "command": "uv",
    "args": [
      "run",
      "python",
      "-m",
      "lancedb_mcp",
      "--db-path",
      "~/.lancedb"
    ]
  }
}
```

## Development

```bash
# Install development dependencies
uv pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .
ruff .
```

## Environment Variables

- `LANCEDB_URI`: Path to LanceDB storage (default: ".lancedb")

## License

This project is licensed under the MIT License. See the LICENSE file for details.
