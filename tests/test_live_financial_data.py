import os
import pytest
from dotenv import load_dotenv
from src.services.financial_data import get_income_statement # Import get_income_statement
from src.models.income_statement import QuarterlyIncomeStatement # Import IncomeStatement

# Define the path to the .env file explicitly for the test
ENV_PATH = ".env"

def test_gemini_api_key_loading():
    """
    Tests if the GEMINI_API_KEY can be loaded from the .env file.
    """
    load_dotenv(dotenv_path=ENV_PATH)
    
    gemini_api_key = os.getenv("GEMINI_API_KEY")

    if gemini_api_key is None:
        pytest.fail(f"GEMINI_API_KEY not found. Please ensure it's set in the {ENV_PATH} file.")
    
    assert gemini_api_key != "", "GEMINI_API_KEY is found but is empty."
    print(f"GEMINI_API_KEY successfully loaded from {ENV_PATH}.")

@pytest.mark.asyncio
async def test_get_income_statement_live():
    """
    Performs a live test of the get_income_statement function.
    """
    load_dotenv(dotenv_path=ENV_PATH)
    if not os.getenv("GEMINI_API_KEY"):
        pytest.skip(f"GEMINI_API_KEY not found in {ENV_PATH}, skipping live test.")

    ticker = "AAPl"
    income_statement = await get_income_statement(ticker)

    assert income_statement is not None, f"Failed to retrieve income statement for {ticker}"
    assert isinstance(income_statement, QuarterlyIncomeStatement), f"Expected QuarterlyIncomeStatement object, got {type(income_statement)}"
    breakpoint()
    # Assert some key fields are not None or have a plausible value
    assert income_statement.ticker == ticker.upper(), "Ticker mismatch in income statement."
    assert income_statement.revenue is not None and isinstance(income_statement.revenue, int), "Revenue should be a float."
    assert income_statement.net_income is not None and isinstance(income_statement.net_income, float), "Net income should be a float."
    assert income_statement.last_earnings_date is not None and isinstance(income_statement.last_earnings_date, str) and income_statement.last_earnings_date != "", "Last earnings date should be a non-empty string."
    
    print(f"Successfully retrieved live income statement for {ticker}:")
    print(income_statement.model_dump_json(indent=2))
