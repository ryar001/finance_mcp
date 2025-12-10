# Quickstart: Financial MCP Server

This document provides a quick overview of how to get started with the Financial MCP Server.

## Prerequisites

- Python 3.11
- `uv` package manager

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/example/finance_mcp.git
    ```
2.  Navigate to the project directory:
    ```bash
    cd finance_mcp
    ```
3.  Install the dependencies:
    ```bash
    uv add -r requirements.txt
    ```
4.  Create a `.env` file in the root of the project and add your Gemini API key:
    ```
    GEMINI_API_KEY=YOUR_API_KEY
    ```

## Running the Server

To run the server, use the following command:

```bash
uvicorn src.main:app --reload
```

## Usage

The server exposes three GET endpoints:

-   `/income_statement`
-   `/balance_sheet`
-   `/cash_flow_statement`

Each endpoint accepts a `company` query parameter.

### Example

```bash
curl "http://localhost:8000/income_statement?company=Apple"
```
