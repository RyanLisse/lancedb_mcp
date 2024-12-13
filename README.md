# LanceDB MCP Server

A Model Control Protocol (MCP) server implementation for LanceDB vector database operations. This server provides a standardized interface for vector storage and similarity search operations through the MCP protocol.

## Features

- Vector storage and retrieval
- Similarity search
- Metadata management
- Resource listing and querying
- Efficient vector operations

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/lancedb-mcp.git
cd lancedb-mcp

# Create and activate virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .
```

## Usage

### Starting the Server

```bash
lancedb-mcp
```

### Available Operations

1. **List Resources**
   - Lists all available vectors in the database
   - Returns vector IDs and associated metadata

2. **Read Resource**
   - Retrieves a specific vector by ID
   - Returns vector data and metadata

3. **Add Vector**
   - Adds a new vector to the database
   - Requires vector data and optional metadata

4. **Search Vectors**
   - Performs similarity search
   - Returns nearest neighbors with similarity scores

## API Reference

### Vector Data Model

```python
{
    "id": "string",           # Unique identifier
    "vector": [float],        # Vector data
    "metadata": {             # Optional metadata
        "key": "value"
    }
}
```

### Tools

1. **add_vector**
   ```python
   {
       "id": "vec1",
       "vector": [0.1, 0.2, 0.3],
       "metadata": {"category": "example"}
   }
   ```

2. **search_vectors**
   ```python
   {
       "query_vector": [0.1, 0.2, 0.3],
       "limit": 10
   }
   ```

## Development

### Testing

```bash
pytest
```

### Code Style

This project follows:
- PEP 8 style guide
- Black code formatting
- Type hints
- Comprehensive docstrings

## License

MIT License - see LICENSE file for details
