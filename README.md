# Finance MCP Server

A Model Context Protocol (MCP) server that provides financial data for LLMs. This server specifically fetches financial statements (Income Statement, Balance Sheet, Cash Flow) for public companies.

## Features

- **Free to use**: No API keys required.
- **Structured Data**: Returns data in consistent Pydantic models (JSON schema).
- **Easy Integration**: Works with any MCP-compliant client (Claude Desktop, Cursor, etc.).

## Data Source

This package retrieves financial data from [Yahoo Finance](https://finance.yahoo.com/) using the `yfinance` library.
*Note: This tool is for educational and research purposes. Please respect Yahoo Finance's terms of service.*

## Installation & Usage

### Option 1: Quick Use with `uvx` (Recommended)

You can run this server directly without standard installation using `uv` (or `uvx`).

Add this to your MCP settings configuration (e.g., `~/.config/Claude/claude_desktop_config.json` or your IDE's MCP config):

```json
{
  "mcpServers": {
    "finance": {
      "command": "uvx",
      "args": [
        "finance-mcp-free"
      ]
    }
  }
}
```

### Option 2: Local Development (Git Clone)

If you want to modify the code or run it locally:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ryar001/finance_mcp.git
   cd finance_mcp
   ```

2. **Install dependencies**:
   ```bash
   # Using uv (recommended)
   uv venv
   source .venv/bin/activate
   uv sync
   
   # Or using pip
   pip install -e .
   ```

3. **Run the server**:
   ```bash
   # Run directly
   finance-mcp
   
   # Or via fastmcp dev for auto-reload
   fastmcp dev finance_mcp/main_mcp.py:mcp_server
   ```

## Data Models

The server returns data structured according to strict Pydantic models to ensure reliability for your LLM.

### Example Return Format

All financial statements return a dictionary where keys are dates and values are the statement object.

**Income Statement Example:**
```json
{
  "30/09/2023": {
    "ticker": "AAPL",
    "period": "30/09/2023",
    "total_revenue": 89498000000,
    "net_income": 22956000000,
    "cost_of_revenue": 49071000000,
    "gross_profit": 40427000000,
    "operating_expenses": 13458000000,
    "operating_income": 26969000000,
    ...
  }
}
```

The data is strictly typed to ensure your LLM can reliably query fields like `total_revenue`, `net_income`, etc.
