import pytest
from src.main_mcp import mcp
from fastmcp import FastMCP

def test_mcp_instance():
    """
    Tests if the mcp object is an instance of FastMCP.
    """
    assert isinstance(mcp, FastMCP)

def test_mcp_name():
    """
    Tests if the name of the mcp object is "Financial MCP".
    """
    assert mcp.name == "Financial MCP"

@pytest.mark.asyncio
async def test_mcp_tools():
    """
    Tests the tools registered with the FastMCP instance.
    """
    tools = await mcp.get_tools()
    assert "get_income_statement_route_api_v1_income_statement_get" in tools
