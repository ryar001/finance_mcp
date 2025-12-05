from fastmcp import tool, tool_block
from src.services.financial_data import get_income_statement
from src.models.income_statement import IncomeStatement
from src.components.logging_utils import setup_logging

logger = setup_logging()

@tool("get_income_statement_tool", "Retrieve an income statement for a company.")
class IncomeStatementTool:
    @tool_block("Retrieve income statement for a company.",
                "Returns a JSON object containing the income statement.")
    async def get_income_statement_by_company(
        self,
        company: str, # type: ignore
    ) -> IncomeStatement:
        """
        Retrieve the income statement for a specified company.

        Args:
            company: The name of the company (e.g., 'Apple', 'Microsoft').
        """
        try:
            income_statement = await get_income_statement(company)
            logger.debug(f"Tool received income statement: {income_statement}")
            if not income_statement:
                return IncomeStatement(
                    company_name=company,
                    ticker="N/A",
                    revenue=0.0,
                    cost_of_goods_sold=0.0,
                )
            return income_statement
        except Exception as e:
            logger.exception(f"Internal server error: {str(e)}")
            raise Exception(f"Internal server error: {str(e)}")
