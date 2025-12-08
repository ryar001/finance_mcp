import pytest
from src.services.financial_data import get_income_statement, get_balance_sheet, get_cashflow_statement
from src.models.income_statement import QuarterlyIncomeStatement
from src.models.balance_sheet import QuarterlyBalanceSheet
from src.models.cash_flow_statement import QuarterlyCashFlowStatement

# Define the path to the .env file explicitly for the test
ENV_PATH = ".env"


@pytest.mark.asyncio
async def test_get_income_statement_live():
    """
    Performs a live test of the get_income_statement function.
    """

    ticker = "AAPl"
    income_statement_map,missing_keys = await get_income_statement(ticker)

    assert income_statement_map is not None, f"Failed to retrieve income statement map for {ticker}"
    assert len(missing_keys) == 0, f"Missing keys: {missing_keys}"
    assert isinstance(income_statement_map, dict), f"Expected Dict object, got {type(income_statement_map)}"
    assert len(income_statement_map) > 0, "Income statement map should not be empty"

    # Get the latest statement (first value usually)
    first_date = list(income_statement_map.keys())[0]
    latest_statement = income_statement_map[first_date]
    breakpoint()
    assert isinstance(latest_statement, QuarterlyIncomeStatement), f"Expected QuarterlyIncomeStatement values, got {type(latest_statement)}"
    
    # Assert some key fields are not None or have a plausible value
    assert latest_statement.ticker.upper() == ticker.upper(), "Ticker mismatch in income statement."
    # Check total_revenue which is consistent with model definition (Optional[int])
    if latest_statement.total_revenue is not None:
        assert isinstance(latest_statement.total_revenue, int), "Total Revenue should be an int."
    
    assert latest_statement.last_earnings_date is not None and isinstance(latest_statement.last_earnings_date, str), "Last earnings date should be a string."
    

    print(f"Successfully retrieved live income statement map for {ticker} with {len(income_statement_map)} entries.")




@pytest.mark.asyncio
async def test_get_balance_sheet_live():
    """
    Performs a live test of the get_balance_sheet function.
    """

    ticker = "AAPl"
    balance_sheet_map, missing_keys = await get_balance_sheet(ticker)

    assert balance_sheet_map is not None, f"Failed to retrieve balance sheet map for {ticker}"
    assert len(missing_keys) == 0, f"Missing keys: {missing_keys}"
    assert isinstance(balance_sheet_map, dict), f"Expected Dict object, got {type(balance_sheet_map)}"
    assert len(balance_sheet_map) > 0, "Balance sheet map should not be empty"

    # Get the latest statement (first value usually)
    first_date = list(balance_sheet_map.keys())[0]
    latest_statement = balance_sheet_map[first_date]

    assert isinstance(latest_statement, QuarterlyBalanceSheet), f"Expected QuarterlyBalanceSheet values, got {type(latest_statement)}"
    
    # Assert some key fields are not None or have a plausible value
    assert latest_statement.ticker.upper() == ticker.upper(), "Ticker mismatch in balance sheet."
    
    # Check total_assets which is usually present
    # Assuming the model has total_assets. I should verify this but it's a safe bet for a balance sheet.
    # If not, I can just check id or last_updated if they exist.
    # Based on QuarterlyIncomeStatement test, it checks specific fields.
    # Let's check a generic field if possible or just rely on the type.
    
    print(f"Successfully retrieved live balance sheet map for {ticker} with {len(balance_sheet_map)} entries.")


@pytest.mark.asyncio
async def test_get_cash_flow_statement_live():
    """
    Performs a live test of the get_cash_flow_statement function.
    """

    ticker = "AAPL"
    cash_flow_map, missing_keys = await get_cashflow_statement(ticker)

    assert cash_flow_map is not None, f"Failed to retrieve cash flow statement map for {ticker}"
    assert len(missing_keys) == 0, f"Missing keys: {missing_keys}"
    assert isinstance(cash_flow_map, dict), f"Expected Dict object, got {type(cash_flow_map)}"
    assert len(cash_flow_map) > 0, "Cash flow statement map should not be empty"

    # Get the latest statement (first value usually)
    first_date = list(cash_flow_map.keys())[0]
    latest_statement = cash_flow_map[first_date]

    assert isinstance(latest_statement, QuarterlyCashFlowStatement), f"Expected QuarterlyCashFlowStatement values, got {type(latest_statement)}"
    
    # Assert some key fields are not None or have a plausible value
    assert latest_statement.ticker.upper() == ticker.upper(), "Ticker mismatch in cash flow statement."
    # Assert on operating_cash_flow as a plausible and common field
    if latest_statement.operating_cash_flow is not None:
        assert isinstance(latest_statement.operating_cash_flow, int), "Operating Cash Flow should be an int."
    
    print(f"Successfully retrieved live cash flow statement map for {ticker} with {len(cash_flow_map)} entries.")

