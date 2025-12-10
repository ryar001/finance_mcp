#!/bin/bash
# Test script to verify the finance-mcp-jokerssd package from TestPyPI.

echo "Cleaning uv cache..."
uv cache clean

echo "Running finance-mcp-jokerssd from TestPyPI..."
echo "Note: This will download dependencies and start the MCP server. It may block waiting for input."
echo "Use Ctrl+C to exit."

# We need --extra-index-url for dependencies that are not on TestPyPI (like fastmcp, pandas, etc.)
uvx --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple finance-mcp-jokerssd
