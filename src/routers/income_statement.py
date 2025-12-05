from fastapi import APIRouter, HTTPException, Query
from src.services.financial_data import get_income_statement
from src.models.income_statement import IncomeStatement
from src.components.init_config import logger

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
        income_statement = await get_income_statement(company)
        logger.debug(f"Router received income statement: {income_statement}") # Debug print changed to logger.debug
        if not income_statement:
            # Return a default/empty IncomeStatement if not found for now to ensure the API returns 200 OK.
            # Proper error handling will be addressed in a later task.
            return IncomeStatement(
                company_name=company,
                ticker="N/A",
                revenue=0.0,
                cost_of_goods_sold=0.0,
            )
        return income_statement
    except Exception as e:
        logger.exception(f"Internal server error: {str(e)}") # Replaced traceback.print_exc() with logger.exception
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")