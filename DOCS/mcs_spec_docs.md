*Note: This is llms-full.txt is not complete, please enter a Firecrawl API key to get the entire llms-full.txt at llmstxt.firecrawl.dev or you can access llms.txt via API with curl -X GET 'http://llmstxt.firecrawl.dev/https://spec.modelcontextprotocol.io/?FIRECRAWL_API_KEY=YOUR_API_KEY' or llms-full.txt via API with curl -X GET 'http://llmstxt.firecrawl.dev/https://spec.modelcontextprotocol.io//full?FIRECRAWL_API_KEY=YOUR_API_KEY'

# https://spec.modelcontextprotocol.io/ llms-full.txt

[Specification](/specification/)

[Revisions](/specification/revisions/)

2024-11-05 (Current)

# 2024-11-05 (Current)

This is the current version of the specification. This revision may continue to receive backwards compatible changes.[Specification](/specification/)

Server Features

# Server Features

ℹ️

**Protocol Revision**: 2024-11-05

Servers provide the fundamental building blocks for adding context to language models via MCP. These primitives enable rich interactions between clients, servers, and language models:

- **Prompts**: Pre-defined templates or instructions that guide language model interactions
- **Resources**: Structured data or content that provides additional context to the model
- **Tools**: Executable functions that allow models to perform actions or retrieve information

Each primitive can be summarized in the following control hierarchy:

| Primitive | Control | Description | Example |
| --- | --- | --- | --- |
| Prompts | User-controlled | Interactive templates invoked by user choice | Slash commands, menu options |
| Resources | Application-controlled | Contextual data attached and managed by the client | File contents, git history |
| Tools | Model-controlled | Functions exposed to the LLM to take actions | API POST requests, file writing |

Explore these key primitives in more detail below:

[Prompts](prompts) [Resources](resources) [Tools](tools)[Specification](/specification/)

Client Features

# Client Features

ℹ️

**Protocol Revision**: 2024-11-05

Clients can implement additional features to enrich connected MCP servers:

[Roots](roots) [Sampling](sampling)# Specification

ℹ️

**Protocol Revision**: 2024-11-05

[Model Context Protocol](https://modelcontextprotocol.io) (MCP) is an open protocol that enables seamless integration between LLM applications and external data sources and tools. Whether you’re building an AI-powered IDE, enhancing a chat interface, or creating custom AI workflows, MCP provides a standardized way to connect LLMs with the context they need.

This specification defines the authoritative protocol requirements, based on the TypeScript schema in [schema.ts](https://github.com/modelcontextprotocol/specification/blob/main/schema/schema.ts).

For implementation guides and examples, visit [modelcontextprotocol.io](https://modelcontextprotocol.io).

## Overview [Permalink for this section](\#overview)

MCP provides a standardized way for applications to:

- Share contextual information with language models
- Expose tools and capabilities to AI systems
- Build composable integrations and workflows

The protocol uses [JSON-RPC](https://www.jsonrpc.org/) 2.0 messages to establish communication between:

- **Hosts**: LLM applications that initiate connections
- **Clients**: Connectors within the host application
- **Servers**: Services that provide context and capabilities

MCP takes some inspiration from the [Language Server Protocol](https://microsoft.github.io/language-server-protocol/), which standardizes how to add support for programming languages across a whole ecosystem of development tools. In a similar way, MCP standardizes how to integrate additional context and tools into the ecosystem of AI applications.

## Key Details [Permalink for this section](\#key-details)

### Base Protocol [Permalink for this section](\#base-protocol)

- [JSON-RPC](https://www.jsonrpc.org/) message format
- Stateful connections
- Server and client capability negotiation

### Features [Permalink for this section](\#features)

Servers offer any of the following features to clients:

- **Resources**: Context and data, for the user or the AI model to use
- **Prompts**: Templated messages and workflows for users
- **Tools**: Functions for the AI model to execute

Clients may offer the following feature to servers:

- **Sampling**: Server-initiated agentic behaviors and recursive LLM interactions

### Additional Utilities [Permalink for this section](\#additional-utilities)

- Configuration
- Progress tracking
- Cancellation
- Error reporting
- Logging

## Security and Trust & Safety [Permalink for this section](\#security-and-trust--safety)

The Model Context Protocol enables powerful capabilities through arbitrary data access and code execution paths. With this power comes important security and trust considerations that all implementors must carefully address.

### Key Principles [Permalink for this section](\#key-principles)

1. **User Consent and Control**

   - Users must explicitly consent to and understand all data access and operations
   - Users must retain control over what data is shared and what actions are taken
   - Implementors should provide clear UIs for reviewing and authorizing activities
2. **Data Privacy**

   - Hosts must obtain explicit user consent before exposing user data to servers
   - Hosts must not transmit resource data elsewhere without user consent
   - User data should be protected with appropriate access controls
3. **Tool Safety**

   - Tools represent arbitrary code execution and must be treated with appropriate caution
   - Hosts must obtain explicit user consent before invoking any tool
   - Users should understand what each tool does before authorizing its use
4. **LLM Sampling Controls**

   - Users must explicitly approve any LLM sampling requests
   - Users should control:
     - Whether sampling occurs at all
     - The actual prompt that will be sent
     - What results the server can see
   - The protocol intentionally limits server visibility into prompts

### Implementation Guidelines [Permalink for this section](\#implementation-guidelines)

While MCP itself cannot enforce these security principles at the protocol level, implementors **SHOULD**:

1. Build robust consent and authorization flows into their applications
2. Provide clear documentation of security implications
3. Implement appropriate access controls and data protections
4. Follow security best practices in their integrations
5. Consider privacy implications in their feature designs

## Learn More [Permalink for this section](\#learn-more)

Explore the detailed specification for each protocol component:

[Architecture](architecture) [Base Protocol](basic) [Server Features](server) [Client Features](client) [Contributing](contributing)# Contributions

We welcome contributions from the community! Please review our [contributing guidelines](https://github.com/modelcontextprotocol/specification/blob/main/CONTRIBUTING.md) for details on how to submit changes.

All contributors must adhere to our [Code of Conduct](https://github.com/modelcontextprotocol/specification/blob/main/CODE_OF_CONDUCT.md).

For questions and discussions, please use [GitHub Discussions](https://github.com/modelcontextprotocol/specification/discussions).[Specification](/specification/)

Base Protocol

# Base Protocol

ℹ️

**Protocol Revision**: 2024-11-05

All messages between MCP clients and servers **MUST** follow the [JSON-RPC 2.0](https://www.jsonrpc.org/specification) specification. The protocol defines three fundamental types of messages:

| Type | Description | Requirements |
| --- | --- | --- |
| `Requests` | Messages sent to initiate an operation | Must include unique ID and method name |
| `Responses` | Messages sent in reply to requests | Must include same ID as request |
| `Notifications` | One-way messages with no reply | Must not include an ID |

**Responses** are further sub-categorized as either **successful results** or **errors**. Results can follow any JSON object structure, while errors must include an error code and message at minimum.

## Protocol Layers [Permalink for this section](\#protocol-layers)

The Model Context Protocol consists of several key components that work together:

- **Base Protocol**: Core JSON-RPC message types
- **Lifecycle Management**: Connection initialization, capability negotiation, and session control
- **Server Features**: Resources, prompts, and tools exposed by servers
- **Client Features**: Sampling and root directory lists provided by clients
- **Utilities**: Cross-cutting concerns like logging and argument completion

All implementations **MUST** support the base protocol and lifecycle management components. Other components **MAY** be implemented based on the specific needs of the application.

These protocol layers establish clear separation of concerns while enabling rich interactions between clients and servers. The modular design allows implementations to support exactly the features they need.

See the following pages for more details on the different components:

[Lifecycle](/specification/basic/lifecycle) [Resources](/specification/server/resources) [Prompts](/specification/server/prompts) [Tools](/specification/server/tools) [Logging](/specification/server/utilities/logging) [Sampling](/specification/client/sampling)

## Auth [Permalink for this section](\#auth)

Authentication and authorization are not currently part of the core MCP specification, but we are considering ways to introduce them in future. Join us in [GitHub Discussions](https://github.com/modelcontextprotocol/specification/discussions) to help shape the future of the protocol!

Clients and servers **MAY** negotiate their own custom authentication and authorization strategies.

## Schema [Permalink for this section](\#schema)

The full specification of the protocol is defined as a [TypeScript schema](http://github.com/modelcontextprotocol/specification/tree/main/schema/schema.ts). This is the source of truth for all protocol messages and structures.

There is also a [JSON Schema](http://github.com/modelcontextprotocol/specification/tree/main/schema/schema.json), which is automatically generated from the TypeScript source of truth, for use with various automated tooling.[Specification](/specification/)

[Server Features](/specification/server/)

Prompts

# Prompts

ℹ️

**Protocol Revision**: 2024-11-05

The Model Context Protocol (MCP) provides a standardized way for servers to expose prompt templates to clients. Prompts allow servers to provide structured messages and instructions for interacting with language models. Clients can discover available prompts, retrieve their contents, and provide arguments to customize them.

## User Interaction Model [Permalink for this section](\#user-interaction-model)

Prompts are designed to be **user-controlled**, meaning they are exposed from servers to clients with the intention of the user being able to explicitly select them for use.

Typically, prompts would be triggered through user-initiated commands in the user interface, which allows users to naturally discover and invoke available prompts.

For example, as slash commands:

![Example of prompt exposed as slash command](../slash-command.png)

However, implementors are free to expose prompts through any interface pattern that suits their needs—the protocol itself does not mandate any specific user interaction model.

## Capabilities [Permalink for this section](\#capabilities)

Servers that support prompts **MUST** declare the `prompts` capability during [initialization](https://spec.modelcontextprotocol.io/specification/basic/lifecycle/#initialization):

```json
{
  "capabilities": {
    "prompts": {
      "listChanged": true
    }
  }
}
```

`listChanged` indicates whether the server will emit notifications when the list of available prompts changes.

## Protocol Messages [Permalink for this section](\#protocol-messages)

### Listing Prompts [Permalink for this section](\#listing-prompts)

To retrieve available prompts, clients send a `prompts/list` request. This operation supports [pagination](https://spec.modelcontextprotocol.io/specification/server/utilities/pagination/).

**Request:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "prompts/list",
  "params": {
    "cursor": "optional-cursor-value"
  }
}
```

**Response:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "prompts": [\
      {\
        "name": "code_review",\
        "description": "Asks the LLM to analyze code quality and suggest improvements",\
        "arguments": [\
          {\
            "name": "code",\
            "description": "The code to review",\
            "required": true\
          }\
        ]\
      }\
    ],
    "nextCursor": "next-page-cursor"
  }
}
```

### Getting a Prompt [Permalink for this section](\#getting-a-prompt)

To retrieve a specific prompt, clients send a `prompts/get` request. Arguments may be auto-completed through [the completion API](https://spec.modelcontextprotocol.io/specification/server/utilities/completion/).

**Request:**

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "prompts/get",
  "params": {
    "name": "code_review",
    "arguments": {
      "code": "def hello():\n    print('world')"
    }
  }
}
```

**Response:**

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "description": "Code review prompt",
    "messages": [\
      {\
        "role": "user",\
        "content": {\
          "type": "text",\
          "text": "Please review this Python code:\ndef hello():\n    print('world')"\
        }\
      }\
    ]
  }
}
```

### List Changed Notification [Permalink for this section](\#list-changed-notification)

When the list of available prompts changes, servers that declared the `listChanged` capability **SHOULD** send a notification:

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/prompts/list_changed"
}
```

## Message Flow [Permalink for this section](\#message-flow)

```
ServerClientServerClientDiscoveryUsageChangesopt[listChanged]prompts/listList of promptsprompts/getPrompt contentprompts/list_changedprompts/listUpdated prompts
```

## Data Types [Permalink for this section](\#data-types)

### Prompt [Permalink for this section](\#prompt)

A prompt definition includes:

- `name`: Unique identifier for the prompt
- `description`: Optional human-readable description
- `arguments`: Optional list of arguments for customization

### PromptMessage [Permalink for this section](\#promptmessage)

Messages in a prompt can contain:

- `role`: Either “user” or “assistant” to indicate the speaker
- `content`: One of the following content types:

#### Text Content [Permalink for this section](\#text-content)

Text content represents plain text messages:

```json
{
  "type": "text",
  "text": "The text content of the message"
}
```

This is the most common content type used for natural language interactions.

#### Image Content [Permalink for this section](\#image-content)

Image content allows including visual information in messages:

```json
{
  "type": "image",
  "data": "base64-encoded-image-data",
  "mimeType": "image/png"
}
```

The image data MUST be base64-encoded and include a valid MIME type. This enables multi-modal interactions where visual context is important.

#### Embedded Resources [Permalink for this section](\#embedded-resources)

Embedded resources allow referencing server-side resources directly in messages:

```json
{
  "type": "resource",
  "resource": {
    "uri": "resource://example",
    "mimeType": "text/plain",
    "text": "Resource content"
  }
}
```

Resources can contain either text or binary (blob) data and MUST include:

- A valid resource URI
- The appropriate MIME type
- Either text content or base64-encoded blob data

Embedded resources enable prompts to seamlessly incorporate server-managed content like documentation, code samples, or other reference materials directly into the conversation flow.

## Error Handling [Permalink for this section](\#error-handling)

Servers SHOULD return standard JSON-RPC errors for common failure cases:

- Invalid prompt name: `-32602` (Invalid params)
- Missing required arguments: `-32602` (Invalid params)
- Internal errors: `-32603` (Internal error)

## Implementation Considerations [Permalink for this section](\#implementation-considerations)

1. Servers **SHOULD** validate prompt arguments before processing
2. Clients **SHOULD** handle pagination for large prompt lists
3. Both parties **SHOULD** respect capability negotiation

## Security [Permalink for this section](\#security)

Implementations **MUST** carefully validate all prompt inputs and outputs to prevent injection attacks or unauthorized access to resources.

[Resources](/specification/server/resources/ "Resources")[Specification](/specification/)

[Base Protocol](/specification/basic/)

[Utilities](/specification/basic/utilities/)

Cancellation

# Cancellation

ℹ️

**Protocol Revision**: 2024-11-05

The Model Context Protocol (MCP) supports optional cancellation of in-progress requests through notification messages. Either side can send a cancellation notification to indicate that a previously-issued request should be terminated.

## Cancellation Flow [Permalink for this section](\#cancellation-flow)

When a party wants to cancel an in-progress request, it sends a `notifications/cancelled` notification containing:

- The ID of the request to cancel
- An optional reason string that can be logged or displayed

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/cancelled",
  "params": {
    "requestId": "123",
    "reason": "User requested cancellation"
  }
}
```

## Behavior Requirements [Permalink for this section](\#behavior-requirements)

1. Cancellation notifications **MUST** only reference requests that:
   - Were previously issued in the same direction
   - Are believed to still be in-progress
2. The `initialize` request **MUST NOT** be cancelled by clients
3. Receivers of cancellation notifications **SHOULD**:
   - Stop processing the cancelled request
   - Free associated resources
   - Not send a response for the cancelled request
4. Receivers **MAY** ignore cancellation notifications if:
   - The referenced request is unknown
   - Processing has already completed
   - The request cannot be cancelled
5. The sender of the cancellation notification **SHOULD** ignore any response to the request that arrives afterward

## Timing Considerations [Permalink for this section](\#timing-considerations)

Due to network latency, cancellation notifications may arrive after request processing has completed, and potentially after a response has already been sent.

Both parties **MUST** handle these race conditions gracefully:

```
ServerClientServerClientProcessing startsProcessing may havecompleted beforecancellation arrivesStop processingalt​[If notcompleted]Request (ID: 123)notifications/cancelled (ID: 123)
```

## Implementation Notes [Permalink for this section](\#implementation-notes)

- Both parties **SHOULD** log cancellation reasons for debugging
- Application UIs **SHOULD** indicate when cancellation is requested

## Error Handling [Permalink for this section](\#error-handling)

Invalid cancellation notifications **SHOULD** be ignored:

- Unknown request IDs
- Already completed requests
- Malformed notifications

This maintains the “fire and forget” nature of notifications while allowing for race conditions in asynchronous communication.

[Ping](/specification/basic/utilities/ping/ "Ping") [Progress](/specification/basic/utilities/progress/ "Progress")[Specification](/specification/)

[Base Protocol](/specification/basic/)

[Utilities](/specification/basic/utilities/)

Ping

# Ping

ℹ️

**Protocol Revision**: 2024-11-05

The Model Context Protocol includes an optional ping mechanism that allows either party to verify that their counterpart is still responsive and the connection is alive.

## Overview [Permalink for this section](\#overview)

The ping functionality is implemented through a simple request/response pattern. Either the client or server can initiate a ping by sending a `ping` request.

## Message Format [Permalink for this section](\#message-format)

A ping request is a standard JSON-RPC request with no parameters:

```json
{
  "jsonrpc": "2.0",
  "id": "123",
  "method": "ping"
}
```

## Behavior Requirements [Permalink for this section](\#behavior-requirements)

1. The receiver **MUST** respond promptly with an empty response:

```json
{
  "jsonrpc": "2.0",
  "id": "123",
  "result": {}
}
```

2. If no response is received within a reasonable timeout period, the sender **MAY**:
   - Consider the connection stale
   - Terminate the connection
   - Attempt reconnection procedures

## Usage Patterns [Permalink for this section](\#usage-patterns)

```
ReceiverSenderReceiverSenderping requestempty response
```

## Implementation Considerations [Permalink for this section](\#implementation-considerations)

- Implementations **SHOULD** periodically issue pings to detect connection health
- The frequency of pings **SHOULD** be configurable
- Timeouts **SHOULD** be appropriate for the network environment
- Excessive pinging **SHOULD** be avoided to reduce network overhead

## Error Handling [Permalink for this section](\#error-handling)

- Timeouts **SHOULD** be treated as connection failures
- Multiple failed pings **MAY** trigger connection reset
- Implementations **SHOULD** log ping failures for diagnostics

[Cancellation](/specification/basic/utilities/cancellation/ "Cancellation")[Specification](/specification/)

Architecture

# Architecture

The Model Context Protocol (MCP) follows a client-host-server architecture where each host can run multiple client instances. This architecture enables users to integrate AI capabilities across applications while maintaining clear security boundaries and isolating concerns. Built on JSON-RPC, MCP provides a stateful session protocol focused on context exchange and sampling coordination between clients and servers.

## Core Components [Permalink for this section](\#core-components)

```

Internet
Local machine
Application Host Process

Server 3
External APIs
Remote
Resource C
Server 1
Files & Git
Server 2
Database
Local
Resource A
Local
Resource B
Host
Client 1
Client 2
Client 3
```

### Host [Permalink for this section](\#host)

The host process acts as the container and coordinator:

- Creates and manages multiple client instances
- Controls client connection permissions and lifecycle
- Enforces security policies and consent requirements
- Handles user authorization decisions
- Coordinates AI/LLM integration and sampling
- Manages context aggregation across clients

### Clients [Permalink for this section](\#clients)

Each client is created by the host and maintains an isolated server connection:

- Establishes one stateful session per server
- Handles protocol negotiation and capability exchange
- Routes protocol messages bidirectionally
- Manages subscriptions and notifications
- Maintains security boundaries between servers

A host application creates and manages multiple clients, with each client having a 1:1 relationship with a particular server.

### Servers [Permalink for this section](\#servers)

Servers provide specialized context and capabilities:

- Expose resources, tools and prompts via MCP primitives
- Operate independently with focused responsibilities
- Request sampling through client interfaces
- Must respect security constraints
- Can be local processes or remote services

## Design Principles [Permalink for this section](\#design-principles)

MCP is built on several key design principles that inform its architecture and implementation:

1. **Servers should be extremely easy to build**

   - Host applications handle complex orchestration responsibilities
   - Servers focus on specific, well-defined capabilities
   - Simple interfaces minimize implementation overhead
   - Clear separation enables maintainable code
2. **Servers should be highly composable**

   - Each server provides focused functionality in isolation
   - Multiple servers can be combined seamlessly
   - Shared protocol enables interoperability
   - Modular design supports extensibility
3. **Servers should not be able to read the whole conversation, nor “see into” other servers**

   - Servers receive only necessary contextual information
   - Full conversation history stays with the host
   - Each server connection maintains isolation
   - Cross-server interactions are controlled by the host
   - Host process enforces security boundaries
4. **Features can be added to servers and clients progressively**

   - Core protocol provides minimal required functionality
   - Additional capabilities can be negotiated as needed
   - Servers and clients evolve independently
   - Protocol designed for future extensibility
   - Backwards compatibility is maintained

## Message Types [Permalink for this section](\#message-types)

MCP defines three core message types based on [JSON-RPC 2.0](https://www.jsonrpc.org/specification):

- **Requests**: Bidirectional messages with method and parameters expecting a response
- **Responses**: Successful results or errors matching specific request IDs
- **Notifications**: One-way messages requiring no response

Each message type follows the JSON-RPC 2.0 specification for structure and delivery semantics.

## Capability Negotiation [Permalink for this section](\#capability-negotiation)

The Model Context Protocol uses a capability-based negotiation system where clients and servers explicitly declare their supported features during initialization. Capabilities determine which protocol features and primitives are available during a session.

- Servers declare capabilities like resource subscriptions, tool support, and prompt templates
- Clients declare capabilities like sampling support and notification handling
- Both parties must respect declared capabilities throughout the session
- Additional capabilities can be negotiated through extensions to the protocol

```
ServerClientHostServerClientHostActive Session with Negotiated Featuresloop[Client Requests]loop[Server Requests]loop[Notifications]Initialize clientInitialize session with capabilitiesRespond with supported capabilitiesUser- or model-initiated actionRequest (tools/resources)ResponseUpdate UI or respond to modelRequest (sampling)Forward to AIAI responseResponseResource updatesStatus changesTerminateEnd session
```

Each capability unlocks specific protocol features for use during the session. For example:

- Implemented [server features](https://spec.modelcontextprotocol.io/specification/server/) must be advertised in the server’s capabilities
- Emitting resource subscription notifications requires the server to declare subscription support
- Tool invocation requires the server to declare tool capabilities
- [Sampling](https://spec.modelcontextprotocol.io/specification/client/) requires the client to declare support in its capabilities

This capability negotiation ensures clients and servers have a clear understanding of supported functionality while maintaining protocol extensibility.

# LanceDB MCP Server Specification

## Overview

The LanceDB MCP Server implements the Model Context Protocol (MCP) for vector database operations. It provides a standardized interface for managing and querying vector embeddings using LanceDB.

## Server Implementation

### Core Components

1. **Server Class**: `LanceDBServer`
   - Extends the base MCP `Server` class
   - Manages database connections and operations
   - Handles vector table management

2. **Data Models**:
   - `VectorData`: Represents vector data with metadata
   - `DatabaseError`: Custom exception for database operations

### Server Capabilities

The server provides the following capabilities:

```python
{
    "tools": {
        "list": true,
        "get": true,
        "call": true
    },
    "resources": {
        "list": true,
        "get": true,
        "create": true,
        "update": true,
        "delete": true
    }
}
```

## API Reference

### Vector Operations

1. **Create Table**
   ```python
   async def create_table(table_name: str, dimension: int) -> CallToolResult
   ```
   - Creates a new vector table
   - Parameters:
     - `table_name`: Name of the table
     - `dimension`: Vector dimension size

2. **Add Vector**
   ```python
   async def add_vector(table_name: str, vector: List[float], metadata: Optional[Dict] = None) -> CallToolResult
   ```
   - Adds a vector to a table
   - Parameters:
     - `table_name`: Target table name
     - `vector`: Vector data as float list
     - `metadata`: Optional metadata dictionary

3. **Search Vectors**
   ```python
   async def search_vectors(table_name: str, query_vector: List[float], limit: int = 10) -> CallToolResult
   ```
   - Searches for similar vectors
   - Parameters:
     - `table_name`: Table to search in
     - `query_vector`: Query vector
     - `limit`: Maximum results to return

### Resource Management

1. **List Resources**
   ```python
   async def list_resources() -> List[Resource]
   ```
   - Lists all available tables
   - Returns list of Resource objects

2. **Get Table**
   ```python
   async def _get_table(table_name: str) -> Any
   ```
   - Retrieves a table by name
   - Internal method for table access

## Logging and Monitoring

The server implements comprehensive logging:

1. **Timestamp Generation**
   ```python
   def _get_timestamp() -> str
   ```
   - Generates UTC timestamps in ISO format

2. **Log Messages**
   ```python
   def _send_log(level: str, message: str)
   ```
   - Sends log messages to the client
   - Supports multiple log levels (info, error, etc.)

## Error Handling

The server implements robust error handling:

1. **Database Errors**
   - Custom `DatabaseError` class
   - Proper error propagation
   - Detailed error messages

2. **Operation Results**
   - Success/failure status
   - Error messages in `CallToolResult`
   - Proper cleanup on errors

## Testing

The server includes comprehensive tests:

1. **Unit Tests**
   - Server initialization
   - Vector operations
   - Error handling

2. **Integration Tests**
   - End-to-end workflows
   - Resource management
   - Vector operations

## Usage with MCP Inspector

1. **Starting the Server**
   ```bash
   python3 server.py
   ```

2. **Connecting Inspector**
   ```bash
   npx @modelcontextprotocol/inspector connect http://localhost:8000
   ```

3. **Available Operations**
   - View server capabilities
   - Create and manage tables
   - Add and search vectors
   - Monitor logs

## Best Practices

1. **Resource Management**
   - Always close database connections
   - Clean up temporary resources
   - Handle concurrent access

2. **Error Handling**
   - Validate inputs
   - Provide clear error messages
   - Implement proper rollbacks

3. **Performance**
   - Use appropriate vector dimensions
   - Implement batch operations
   - Monitor memory usage

## Dependencies

- `mcp`: Core MCP implementation
- `lancedb`: Vector database
- `numpy`: Numerical operations
- `pydantic`: Data validation
- `pyarrow`: Table schemas

## Configuration

The server can be configured through:

1. **Environment Variables**
   - Database URI
   - Log levels
   - Server settings

2. **Initialization Options**
   - Custom database path
   - Server name
   - Additional settings
