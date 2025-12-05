import pytest
from fastmcp import Client
from src.main_mcp import mcp_server
from src.models.income_statement import QuarterlyIncomeStatement
from src.models.balance_sheet import QuarterlyBalanceSheet
from src.models.cash_flow_statement import QuarterlyCashFlowStatement

@pytest.mark.asyncio
async def test_get_income_statement_tool():
    async with Client(mcp_server) as client:
        response = await client.call_tool(name="get_income_statement_tool", arguments={"company":"AAPL"})
        assert response is not None
        first_statement = next(iter(response.structured_content.values()))
        first_statement_model = QuarterlyIncomeStatement.model_validate(first_statement)
        assert first_statement_model.ticker == "AAPL"

@pytest.mark.asyncio
async def test_get_balance_sheet_tool():
    async with Client(mcp_server) as client:
        response = await client.call_tool(name="get_balance_sheet_tool", arguments={"company":"AAPL"})
        assert response is not None
        first_statement = next(iter(response.structured_content.values()))
        first_statement_model = QuarterlyBalanceSheet.model_validate(first_statement)
        assert isinstance(first_statement_model, QuarterlyBalanceSheet)
        assert first_statement_model.ticker == "AAPL"

@pytest.mark.asyncio
async def test_get_cashflow_statement_tool():
    async with Client(mcp_server) as client:
        response = await client.call_tool(name="get_cashflow_statement_tool", arguments={"company":"AAPL"})
        assert response is not None
        first_statement = next(iter(response.structured_content.values()))
        first_statement_model = QuarterlyCashFlowStatement.model_validate(first_statement)
        assert first_statement_model.ticker == "AAPL"
