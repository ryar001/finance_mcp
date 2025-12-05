import pytest
from src.models.income_statement import IncomeStatement

def test_income_statement_model():
    income_statement = IncomeStatement(
        company_name="Test Company",
        ticker="TEST",
        revenue=1000.0,
        cost_of_goods_sold=400.0,
        selling_general_admin_expenses=100.0,
        research_and_development_expense=50.0,
        depreciation_and_amortization=50.0,
        interest_income=10.0,
        interest_expense=20.0,
        non_operating_income=30.0,
        income_tax_expense=80.0,
        other_comprehensive_income=15.0,
        weighted_avg_shares_basic=100.0,
        weighted_avg_shares_diluted=110.0,
        preferred_dividends=5.0,
        last_earnings_date="30/10/23"
    )
    assert income_statement.revenue == 1000.0
    assert income_statement.cost_of_goods_sold == 400.0
    assert income_statement.selling_general_admin_expenses == 100.0
    assert income_statement.research_and_development_expense == 50.0
    assert income_statement.depreciation_and_amortization == 50.0
    assert income_statement.interest_income == 10.0
    assert income_statement.interest_expense == 20.0
    assert income_statement.non_operating_income == 30.0
    assert income_statement.income_tax_expense == 80.0
    assert income_statement.other_comprehensive_income == 15.0
    assert income_statement.weighted_avg_shares_basic == 100.0
    assert income_statement.weighted_avg_shares_diluted == 110.0
    assert income_statement.preferred_dividends == 5.0
    assert income_statement.last_earnings_date == "30/10/23"

    # Test derived fields
    assert income_statement.gross_profit == 600.0  # 1000 - 400
    assert income_statement.operating_expenses == 200.0  # 100 + 50 + 50
    assert income_statement.operating_income == 400.0  # 600 - 200
    assert income_statement.pre_tax_income == 420.0  # 400 + 10 - 20 + 30
    assert income_statement.net_income == 340.0  # 420 - 80
    assert income_statement.net_income_common == 335.0 # 340 - 5
    assert income_statement.ebitda == 450.0 # 400 + 50
    assert income_statement.comprehensive_income == 355.0 # 340 + 15
    assert income_statement.eps_basic == 3.40 # 340 / 100
    assert pytest.approx(income_statement.eps_diluted, 0.001) == 3.090909 # 340 / 110

def test_income_statement_model_minimal_fields():
    income_statement = IncomeStatement(
        company_name="Minimal Co.",
        ticker="MIN",
        revenue=500.0,
        cost_of_goods_sold=200.0,
        last_earnings_date="01/01/24"
    )
    assert income_statement.revenue == 500.0
    assert income_statement.cost_of_goods_sold == 200.0
    assert income_statement.last_earnings_date == "01/01/24"

    assert income_statement.gross_profit == 300.0
    assert income_statement.operating_expenses == 0.0 # All optional fields are None
    assert income_statement.operating_income == 300.0
    assert income_statement.pre_tax_income == 300.0
    assert income_statement.net_income == 300.0
    assert income_statement.net_income_common == 300.0
    assert income_statement.ebitda == 300.0
    assert income_statement.comprehensive_income == 300.0
    assert income_statement.eps_basic is None
    assert income_statement.eps_diluted is None