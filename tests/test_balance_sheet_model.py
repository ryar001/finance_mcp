"""
Tests for the balance sheet models and their data transformation logic.
"""
import pytest
from src.models.balance_sheet import ToPullBalanceSheet, QuarterlyBalanceSheet
from src.components.const import ExchangesEnum

@pytest.fixture
def sample_pulled_balance_sheet_data():
    """Provides a sample ToPullBalanceSheet with complete data."""
    return ToPullBalanceSheet(
        company_name="TestCorp",
        ticker="TC",
        exchange=ExchangesEnum.NASDAQ,
        fiscal_year=2025,
        fiscal_quarter="Q4",
        last_earnings_date="01/12/25",
        cash=100,
        accounts_receivable=200,
        inventory=300,
        property_plant_equipment=1000,
        accounts_payable=150,
        debt=500,
        shareholders_equity=950,
    )

def test_from_pulled_data_full_data(sample_pulled_balance_sheet_data):
    """
    Tests that all derived fields are correctly calculated when full source data is provided.
    """
    # Act
    statement = QuarterlyBalanceSheet.from_pulled_data(sample_pulled_balance_sheet_data)

    # --- Assert Derived Fields ---
    # total_current_assets = cash + accounts_receivable + inventory = 100 + 200 + 300 = 600
    assert statement.total_current_assets == 600

    # total_assets = total_current_assets + property_plant_equipment = 600 + 1000 = 1600
    assert statement.total_assets == 1600
    
    # total_liabilities = accounts_payable + debt = 150 + 500 = 650
    assert statement.total_liabilities == 650
    
    # total_liabilities_and_equity = total_liabilities + shareholders_equity = 650 + 950 = 1600
    assert statement.total_liabilities_and_equity == 1600

    # --- Assert Inherited Fields ---
    assert statement.cash == 100
    assert statement.shareholders_equity == 950
    assert statement.company_name == "TestCorp"

def test_from_pulled_data_missing_optionals():
    """
    Tests that calculations proceed correctly and gracefully when optional
    financial data is missing.
    """
    # Arrange: Data with only the bare minimum required fields
    pulled_data = ToPullBalanceSheet(
        company_name="MinimalCorp",
        ticker="MC",
        exchange=ExchangesEnum.NYSE,
        fiscal_year=2025,
        fiscal_quarter="Q1",
        last_earnings_date="01/03/25",
        # All other financial numbers are None
    )

    # Act
    statement = QuarterlyBalanceSheet.from_pulled_data(pulled_data)

    # Assert: Check that derived fields are calculated with defaults (0)
    assert statement.total_current_assets == 0
    assert statement.total_assets == 0
    assert statement.total_liabilities == 0
    assert statement.total_liabilities_and_equity == 0
    
    # Check that key data is still present
    assert statement.company_name == "MinimalCorp"
    assert statement.cash is None
