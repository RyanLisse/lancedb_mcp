# Contributing

Thank you for your interest in contributing to `create-mcp-server`! This tool helps developers quickly scaffold new MCP (Model Context Protocol) servers.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/create-python-server.git`
3. Install dependencies: `uv sync --dev --all-extras`

## Development

- Make your changes in the `src` directory
- Test your changes by creating a new server: `uv run -m create_mcp_server test-server`
- Run type checking: `uv run pyright`
- Run linting: `uv run ruff check .`

## Pull Requests

1. Create a new branch for your changes
2. Make your changes
3. Ensure type checking and linting pass
4. Test server creation using your changes
5. Submit a pull request with a clear description of your changes

## Code of Conduct

This project follows our [Code of Conduct](CODE_OF_CONDUCT.md). Please review it before contributing.

## Reporting Issues

- Use the [GitHub issue tracker](https://github.com/modelcontextprotocol/create-python-server/issues)
- Provide clear reproduction steps
- Include relevant system information
- Specify the version you're using

## Security Issues

Please review our [Security Policy](SECURITY.md) for reporting security vulnerabilities.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
