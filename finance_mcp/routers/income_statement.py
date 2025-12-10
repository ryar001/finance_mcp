from fastapi import APIRouter, HTTPException, Query
from finance_mcp.services.financial_data import get_income_statement
from finance_mcp.models.income_statement import IncomeStatement
from finance_mcp.components.init_config import logger

router = APIRouter()



@router.get(
    "/income_statement",
    response_model=IncomeStatement,
    summary="Retrieve an income statement for a company.",
    response_description="A JSON object containing the income statement."
)
async def get_income_statement_route(
    company: str = Query(..., description="Name of the company (e.g., 'Apple', 'Microsoft')")
):
    """
    Retrieve the income statement for a specified company.

    - **company**: The name of the company for which to retrieve the income statement.
    """
    try:
        statements, _ = await get_income_statement(company)
        logger.debug(f"Router received income statement: {statements}") 
        if not statements:
            return IncomeStatement(
                ticker="N/A",
            )
        return next(iter(statements.values()))
    except Exception as e:
        logger.exception(f"Internal server error: {str(e)}") # Replaced traceback.print_exc() with logger.exception
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")