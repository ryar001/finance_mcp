
import pytest
from finance_mcp.main_mcp import mcp_server
from finance_mcp.tools.financial_tools import get_income_statement_tool

def test_mcp_server_configuration():
    """Test that the MCP server is configured correctly."""
    assert mcp_server.name == "Financial MCP Server"
    
    # FastMCP stores tools in different ways depending on version, 
    # but we can check if the functions are registered.
    # We can inspect the internal list of tools if available, or just trust the import
    # For many FastMCP implementations, list_tools() is an async method on the server or similar.
    # But since we have access to the object, we can check basic properties.
    pass

@pytest.mark.asyncio
async def test_get_income_statement_tool():
    """Test the get_income_statement_tool function directly."""
    # We use a real ticker, e.g., "AAPL" or "GOOG"
    company = "GOOG"
    result = await get_income_statement_tool(company)
    
    assert result is not None
    assert isinstance(result, dict)
    # Check if we got some data back (keys should be dates)
    assert len(result) > 0
    
    # Pick the first item
    first_key = list(result.keys())[0]
    statement = result[first_key]
    
    # Verify it has some expected fields
    # Note: result values are Pydantic models (QuarterlyIncomeStatement) based on financial_tools.py implementation?
    # financial_tools.py returns `statements` from `get_income_statement`.
    # `get_income_statement` returns Tuple[Dict[str, QuarterlyIncomeStatement], list[str]]
    # so `statements` is Dict[str, QuarterlyIncomeStatement].
    
    # Let's inspect one value
    assert hasattr(statement, "ticker")
    assert statement.ticker == "GOOG"

