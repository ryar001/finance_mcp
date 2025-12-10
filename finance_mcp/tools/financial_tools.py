from typing import Dict
from finance_mcp.services.financial_data import get_income_statement, get_balance_sheet, get_cashflow_statement
from finance_mcp.models.balance_sheet import QuarterlyBalanceSheet
from finance_mcp.models.cash_flow_statement import QuarterlyCashFlowStatement
from finance_mcp.models.income_statement import QuarterlyIncomeStatement


async def get_income_statement_tool(company: str) -> Dict[str, QuarterlyIncomeStatement]:
    """
    Retrieve the income statement for a specified company.

    - **company**: The name of the company for which to retrieve the income statement.
    """
    statements, _ = await get_income_statement(company)
    return statements

async def get_balance_sheet_tool(company: str) -> Dict[str, QuarterlyBalanceSheet]:
    """
    Retrieve the balance sheet for a specified company.

    - **company**: The name of the company for which to retrieve the balance sheet.
    """
    statements, _ = await get_balance_sheet(company)
    return statements

async def get_cashflow_statement_tool(company: str) -> Dict[str, QuarterlyCashFlowStatement]:
    """
    Retrieve the cash flow statement for a specified company.

    - **company**: The name of the company for which to retrieve the cash flow statement.
    """
    statements, _ = await get_cashflow_statement(company)
    return statements
