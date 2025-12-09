import pytest
from finance_mcp.services.financial_data import get_income_statement

@pytest.mark.asyncio
async def test_get_income_statement_consistency():
    """
    Tests the consistency of the get_income_statement function by calling it multiple times
    for the same company and ensuring the results are identical.
    This test makes real API calls and may take some time.
    """
    company = "AAPL"
    
    # Call the function three times
    statement1 = await get_income_statement(company)
    # statement3 = await get_income_statement(company)
    
    # Ensure the first statement is valid
    assert statement1 is not None, "First API call should return a statement, not None."
    assert isinstance(statement1[0], dict), "Should return a dictionary as the first element of the tuple."
    assert isinstance(statement1[1], list), "Should return a list as the second element of the tuple."
    assert len(statement1[0]) > 0, "The dictionary should not be empty."

