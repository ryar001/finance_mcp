from fastmcp import FastMCP
from src.tools import financial_tools

mcp_server = FastMCP(
    "Financial MCP Server",
    tools=[
        financial_tools.get_income_statement_tool,
        financial_tools.get_balance_sheet_tool,
        financial_tools.get_cashflow_statement_tool,
    ],
)
