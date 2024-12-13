# LanceDB MCP Server API Reference

## Overview

The LanceDB MCP Server implements the Model Control Protocol (MCP) specification, providing a standardized interface for vector database operations through LanceDB. This server enables vector operations including table creation, vector addition, and similarity search while adhering to MCP's principles of user consent, resource isolation, and secure data handling.

## Server Implementation

### Core Components

#### Database Connection
- Managed through LanceDB's Python client
- Supports both local and cloud storage backends
- Handles connection lifecycle and resource management

#### Table Management
- Creates and manages vector tables
- Maintains table references and state
- Handles table cleanup and optimization

#### Vector Operations
- Adds vectors with metadata
- Performs similarity search with configurable metrics
- Supports vector validation and dimension checking

#### Resource Management
- Tracks available tables and their states
- Implements MCP resource isolation
- Manages resource lifecycle

### MCP Protocol Implementation

#### Server Features
The server implements all required MCP features:

1. **Resources**
   - Vector tables as queryable resources
   - Resource isolation per connection
   - Resource state tracking

2. **Tools**
   - Table creation and management
   - Vector addition and search
   - Resource listing and status

3. **Capabilities**
   - Dynamic reporting of supported operations
   - Vector operation configurations
   - Resource management features

### API Reference

#### Server Methods

##### Lifecycle Management

```python
async def start(self):
    """Start the LanceDB server"""
    # Creates database directory
    # Establishes connection
    # Initializes state tracking
```

```python
async def stop(self):
    """Stop the LanceDB server"""
    # Cleans up resources
    # Closes connections
    # Performs garbage collection
```

##### Table Operations

```python
async def create_table(self, table_name: str, dimension: int) -> Dict[str, str]:
    """Create a new vector table"""
    # Creates table with specified dimension
    # Returns table metadata
```

```python
async def add_vector(self, table_name: str, vector: List[float], metadata: Optional[Dict] = None):
    """Add vector to table"""
    # Validates vector dimensions
    # Adds vector with optional metadata
```

```python
async def search_vectors(self, table_name: str, query_vector: List[float], limit: int = 10):
    """Search for similar vectors"""
    # Performs similarity search
    # Returns top-k results with scores
```

##### Resource Management

```python
async def list_resources(self) -> List[Resource]:
    """List available tables"""
    # Returns list of available tables
    # Includes table metadata
```

```python
async def get_implementation(self) -> Implementation:
    """Get server implementation details"""
    # Returns server name, version, vendor
```

```python
async def get_capabilities(self) -> ServerCapabilities:
    """Get server capabilities"""
    # Returns supported operations
    # Includes tool configurations
```

### Error Types

- `DatabaseError`: General database operation failures
  ```python
  class DatabaseError(Exception):
      """Raised when database operations fail"""
  ```

- `TableError`: Table-specific operation failures
  ```python
  class TableError(Exception):
      """Raised for table operation failures"""
  ```

- `VectorError`: Vector operation failures
  ```python
  class VectorError(Exception):
      """Raised for vector operation failures"""
  ```

### Configuration

#### Database URI
```python
server = LanceDBServer(
    db_uri="data/vectors",  # Database location
    read_consistency_interval=None  # Consistency check interval
)
```

#### Vector Operations
```python
# Vector dimension validation
vector_dim = 768  # Must match table dimension
vector = [0.1] * vector_dim

# Adding vectors with metadata
metadata = {
    "id": "doc1",
    "text": "Sample document",
    "timestamp": "2024-01-01"
}

# Search configuration
limit = 10  # Number of results
metric = "L2"  # Distance metric
```

### Best Practices

1. **Resource Management**
   - Clean up resources when no longer needed
   - Monitor table sizes and vector counts
   - Implement proper logging

2. **Vector Operations**
   - Validate vector dimensions before adding
   - Use appropriate metadata for tracking
   - Handle errors appropriately

3. **Performance Optimization**
   - Create indices for frequently searched tables
   - Use appropriate batch sizes for operations
   - Monitor and optimize resource usage

### Error Handling

The server implements comprehensive error handling:

1. **Database Errors**
   - Connection failures
   - Resource allocation issues
   - Storage backend errors

2. **Table Errors**
   - Creation failures
   - Access permission issues
   - Resource conflicts

3. **Vector Errors**
   - Dimension mismatches
   - Invalid data types
   - Search operation failures

### Logging and Monitoring

The server includes built-in logging for:
- Operation status and errors
- Resource usage and performance
- Security-related events

### Security Considerations

1. **Resource Isolation**
   - Tables are isolated per connection
   - Resource access requires explicit consent
   - State is maintained per session

2. **Data Validation**
   - Input validation for all operations
   - Secure handling of metadata
   - Protection against invalid operations

3. **Error Handling**
   - Secure error messages
   - No sensitive data in logs
   - Proper cleanup on failures

## Testing

The server includes comprehensive tests:

1. **Unit Tests**
   - Core functionality
   - Error handling
   - Edge cases

2. **Integration Tests**
   - End-to-end workflows
   - Resource management
   - Performance benchmarks

3. **Stress Tests**
   - Concurrent operations
   - Resource limits
   - Error recovery

## Contributing

1. **Development Setup**
   - Fork repository
   - Install dependencies
   - Set up development environment

2. **Making Changes**
   - Create feature branch
   - Follow coding standards
   - Add tests for new features

3. **Submitting Changes**
   - Create pull request
   - Pass all tests
   - Update documentation

## License

This project is licensed under the MIT License.
