import sys
from pathlib import Path
from typing import Optional
from sqlmodel import Field
from src.models.base_model import BaseStatementsModel

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent))


class QuarterlyCashFlowStatement(BaseStatementsModel, table=True):
    """SQLModel for storing quarterly cash flow statements in the database."""
    __tablename__ = "quarterly_cash_flow_statements"

    # Financial Metrics (Source: Single Complete Source)
    free_cash_flow: Optional[int] = Field(default=None, nullable=True)
    repurchase_of_capital_stock: Optional[int] = Field(default=None, nullable=True)
    repayment_of_debt: Optional[int] = Field(default=None, nullable=True)
    issuance_of_debt: Optional[int] = Field(default=None, nullable=True)
    issuance_of_capital_stock: Optional[int] = Field(default=None, nullable=True)
    capital_expenditure: Optional[int] = Field(default=None, nullable=True)
    end_cash_position: Optional[int] = Field(default=None, nullable=True)
    beginning_cash_position: Optional[int] = Field(default=None, nullable=True)
    effect_of_exchange_rate_changes: Optional[int] = Field(default=None, nullable=True)
    changes_in_cash: Optional[int] = Field(default=None, nullable=True)
    financing_cash_flow: Optional[int] = Field(default=None, nullable=True)
    cash_flow_from_continuing_financing_activities: Optional[int] = Field(default=None, nullable=True)
    net_other_financing_charges: Optional[int] = Field(default=None, nullable=True)
    cash_dividends_paid: Optional[int] = Field(default=None, nullable=True)
    common_stock_dividend_paid: Optional[int] = Field(default=None, nullable=True)
    net_common_stock_issuance: Optional[int] = Field(default=None, nullable=True)
    common_stock_payments: Optional[int] = Field(default=None, nullable=True)
    common_stock_issuance: Optional[int] = Field(default=None, nullable=True)
    net_issuance_payments_of_debt: Optional[int] = Field(default=None, nullable=True)
    net_short_term_debt_issuance: Optional[int] = Field(default=None, nullable=True)
    short_term_debt_payments: Optional[int] = Field(default=None, nullable=True) # Added field
    net_long_term_debt_issuance: Optional[int] = Field(default=None, nullable=True)
    long_term_debt_payments: Optional[int] = Field(default=None, nullable=True)
    long_term_debt_issuance: Optional[int] = Field(default=None, nullable=True)
    investing_cash_flow: Optional[int] = Field(default=None, nullable=True)
    cash_flow_from_continuing_investing_activities: Optional[int] = Field(default=None, nullable=True)
    net_other_investing_changes: Optional[int] = Field(default=None, nullable=True)
    net_investment_purchase_and_sale: Optional[int] = Field(default=None, nullable=True)
    sale_of_investment: Optional[int] = Field(default=None, nullable=True)
    purchase_of_investment: Optional[int] = Field(default=None, nullable=True)
    net_business_purchase_and_sale: Optional[int] = Field(default=None, nullable=True)
    purchase_of_business: Optional[int] = Field(default=None, nullable=True)
    net_ppe_purchase_and_sale: Optional[int] = Field(default=None, nullable=True)
    purchase_of_ppe: Optional[int] = Field(default=None, nullable=True)
    operating_cash_flow: Optional[int] = Field(default=None, nullable=True)
    cash_flow_from_continuing_operating_activities: Optional[int] = Field(default=None, nullable=True)
    change_in_working_capital: Optional[int] = Field(default=None, nullable=True)
    change_in_other_working_capital: Optional[int] = Field(default=None, nullable=True)
    change_in_other_current_liabilities: Optional[int] = Field(default=None, nullable=True)
    change_in_other_current_assets: Optional[int] = Field(default=None, nullable=True)
    change_in_payables_and_accrued_expense: Optional[int] = Field(default=None, nullable=True)
    change_in_payable: Optional[int] = Field(default=None, nullable=True)
    change_in_account_payable: Optional[int] = Field(default=None, nullable=True)
    change_in_tax_payable: Optional[int] = Field(default=None, nullable=True)
    change_in_income_tax_payable: Optional[int] = Field(default=None, nullable=True)
    income_tax_paid_supplemental_data: Optional[int] = Field(default=None, nullable=True) # Added field
    other_non_cash_items: Optional[int] = Field(default=None, nullable=True) # Added field
    change_in_inventory: Optional[int] = Field(default=None, nullable=True)
    change_in_receivables: Optional[int] = Field(default=None, nullable=True)
    changes_in_account_receivables: Optional[int] = Field(default=None, nullable=True)
    stock_based_compensation: Optional[int] = Field(default=None, nullable=True)
    unrealized_gain_loss_on_investment_securities: Optional[int] = Field(default=None, nullable=True)
    asset_impairment_charge: Optional[int] = Field(default=None, nullable=True)
    deferred_tax: Optional[int] = Field(default=None, nullable=True)
    deferred_income_tax: Optional[int] = Field(default=None, nullable=True)
    depreciation_amortization_depletion: Optional[int] = Field(default=None, nullable=True)
    depreciation_and_amortization: Optional[int] = Field(default=None, nullable=True)
    depreciation: Optional[int] = Field(default=None, nullable=True)
    operating_gains_losses: Optional[int] = Field(default=None, nullable=True)
    gain_loss_on_investment_securities: Optional[int] = Field(default=None, nullable=True)
    net_income_from_continuing_operations: Optional[int] = Field(default=None, nullable=True)


# --- Backward Compatibility ---
CashFlowStatement = QuarterlyCashFlowStatement