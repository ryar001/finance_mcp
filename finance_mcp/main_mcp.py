from fastmcp import FastMCP
from finance_mcp.tools import financial_tools

mcp_server = FastMCP(
    "Financial MCP Server",
    tools=[
        financial_tools.get_income_statement_tool,
        financial_tools.get_balance_sheet_tool,
        financial_tools.get_cashflow_statement_tool,
    ],
)

def main():
    mcp_server.run()

if __name__ == "__main__":
    main()
