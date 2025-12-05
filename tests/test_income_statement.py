"""
Tests for the income statement models and their data transformation logic.
"""
import pytest
from src.models.income_statement import ToPullIncomeStatement, QuarterlyIncomeStatement

@pytest.fixture
def sample_pulled_data():
    """Provides a sample ToPullIncomeStatement with complete data."""
    return ToPullIncomeStatement(
        company_name="TestCorp",
        ticker="TC",
        fiscal_year=2025,
        fiscal_quarter="Q4",
        last_earnings_date="01/12/25",
        revenue=1000.0,
        cost_of_goods_sold=400.0,
        operating_expenses=300.0,
        research_and_development_expense=120.0,
        selling_general_admin_expenses=180.0,
        depreciation_and_amortization=50.0,
        interest_income=10.0,
        interest_expense=20.0,
        non_operating_income=5.0,
        income_tax_expense=75.0,
        weighted_avg_shares_basic=100.0,
        weighted_avg_shares_diluted=110.0,
        preferred_dividends=10.0,
    )

def test_from_pulled_data_full_data(sample_pulled_data):
    """
    Tests that all derived fields are correctly calculated when full source data is provided.
    """
    # Act
    statement = QuarterlyIncomeStatement.from_pulled_data(sample_pulled_data)

    # --- Assert Derived Fields ---
    # Gross Profit = Revenue - COGS = 1000 - 400 = 600
    assert statement.gross_profit == pytest.approx(600.0)

    # Operating Income = Gross Profit - Operating Expenses = 600 - 300 = 300
    assert statement.operating_income == pytest.approx(300.0)
    
    # EBT = Op Income + Interest Income - Interest Expense + Non-Op Income
    #     = 300 + 10 - 20 + 5 = 295
    assert statement.earnings_before_tax == pytest.approx(295.0)
    
    # Net Income = EBT - Tax = 295 - 75 = 220
    assert statement.net_income == pytest.approx(220.0)

    # EPS Basic = (Net Income - Preferred Dividends) / Basic Shares
    #           = (220 - 10) / 100 = 2.10
    assert statement.earnings_per_share_basic == pytest.approx(2.1)

    # --- Assert Inherited Fields ---
    assert statement.revenue == 1000.0
    assert statement.operating_expenses == 300.0
    assert statement.company_name == "TestCorp"

def test_from_pulled_data_calculated_opex():
    """
    Tests that Operating Expenses are correctly summed from R&D and SG&A
    if the main `operating_expenses` field is not provided.
    """
    # Arrange: Create data without `operating_expenses` but with its components
    pulled_data = ToPullIncomeStatement(
        company_name="TestCorp",
        ticker="TC",
        fiscal_year=2025,
        fiscal_quarter="Q4",
        last_earnings_date="01/12/25",
        revenue=1000.0,
        cost_of_goods_sold=400.0,
        operating_expenses=None,  # This is the key part of the test
        research_and_development_expense=120.0,
        selling_general_admin_expenses=180.0,
        income_tax_expense=75.0,
        weighted_avg_shares_basic=100.0,
    )
    
    # Act
    statement = QuarterlyIncomeStatement.from_pulled_data(pulled_data)

    # --- Assert Derived Fields ---
    # Calculated OpEx = R&D + SG&A = 120 + 180 = 300
    assert statement.operating_expenses == pytest.approx(300.0)

    # Gross Profit = 1000 - 400 = 600
    assert statement.gross_profit == pytest.approx(600.0)

    # Operating Income = Gross Profit - Calculated OpEx = 600 - 300 = 300
    assert statement.operating_income == pytest.approx(300.0)
    
    # EBT = 300 (no other non-op items)
    assert statement.earnings_before_tax == pytest.approx(300.0)

    # Net Income = EBT - Tax = 300 - 75 = 225
    assert statement.net_income == pytest.approx(225.0)

    # EPS Basic = (225 - 0) / 100 = 2.25
    assert statement.earnings_per_share_basic == pytest.approx(2.25)

def test_from_pulled_data_missing_optionals():
    """
    Tests that calculations proceed correctly and gracefully when optional
    financial data (like COGS, interest, etc.) is missing.
    """
    # Arrange: Data with only the bare minimum required fields
    pulled_data = ToPullIncomeStatement(
        company_name="MinimalCorp",
        ticker="MC",
        fiscal_year=2025,
        fiscal_quarter="Q1",
        last_earnings_date="01/03/25",
        revenue=500.0,
        operating_expenses=200.0,
        # All other financial numbers are None
    )

    # Act
    statement = QuarterlyIncomeStatement.from_pulled_data(pulled_data)

    # Assert: Check that derived fields are None or calculated with defaults
    # Gross Profit requires COGS, which is None
    assert statement.gross_profit is None
    
    # Operating Income requires Gross Profit, which is None
    assert statement.operating_income is None
    
    # EBT requires Operating Income, which is None
    assert statement.earnings_before_tax is None

    # Net Income requires EBT, which is None
    assert statement.net_income is None

    # EPS requires Net Income, which is None
    assert statement.earnings_per_share_basic is None
    
    # Check that key data is still present
    assert statement.revenue == 500.0
    assert statement.operating_expenses == 200.0

def test_from_pulled_data_no_shares():
    """
    Tests that EPS is None if share count is missing or zero.
    """
    # Arrange: Data is complete except for share count
    pulled_data_no_shares = ToPullIncomeStatement(
        company_name="TestCorp", ticker="TC", fiscal_year=2025, fiscal_quarter="Q4",
        last_earnings_date="01/12/25", revenue=1000.0, cost_of_goods_sold=400.0,
        operating_expenses=300.0, income_tax_expense=75.0, 
        weighted_avg_shares_basic=None # No shares
    )

    pulled_data_zero_shares = ToPullIncomeStatement(
        company_name="TestCorp", ticker="TC", fiscal_year=2025, fiscal_quarter="Q4",
        last_earnings_date="01/12/25", revenue=1000.0, cost_of_goods_sold=400.0,
        operating_expenses=300.0, income_tax_expense=75.0,
        weighted_avg_shares_basic=0 # Zero shares
    )

    # Act
    statement_no_shares = QuarterlyIncomeStatement.from_pulled_data(pulled_data_no_shares)
    statement_zero_shares = QuarterlyIncomeStatement.from_pulled_data(pulled_data_zero_shares)

    # Assert
    # Net income should be calculable, but EPS should not be
    assert statement_no_shares.net_income is not None
    assert statement_no_shares.earnings_per_share_basic is None

    assert statement_zero_shares.net_income is not None
    assert statement_zero_shares.earnings_per_share_basic is None
