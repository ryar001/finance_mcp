import sys
from pathlib import Path
from typing import Optional
import datetime
from sqlmodel import Field
from finance_mcp.models.base_model import BaseStatementsModel

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent))


class QuarterlyIncomeStatement(BaseStatementsModel, table=True):
    """SQLModel for storing quarterly income statements in the database."""
    __tablename__ = "quarterly_income_statements"

    # Identity and Metadata
    id: Optional[int] = Field(default=None, primary_key=True)
    ticker: str = Field(description="The stock ticker symbol for the company (e.g., 'AAPL').", primary_key=True)  
    last_updated: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(tz=datetime.timezone.utc), nullable=False)
    
    last_earnings_date: Optional[str] = Field(
        default=None, description="The date of the last earnings report, in any common format (e.g., '2025-10-30')."
    )

    # Financial Metrics (Source: Single Complete Source)
    tax_effect_of_unusual_items: Optional[float] = Field(default=None, nullable=True)
    tax_rate_for_calcs: Optional[float] = Field(default=None, nullable=True)
    normalized_ebitda: Optional[int] = Field(default=None, nullable=True)
    total_unusual_items: Optional[int] = Field(default=None, nullable=True)
    total_unusual_items_excluding_goodwill: Optional[int] = Field(default=None, nullable=True)
    net_income_from_continuing_operation_net_minority_interest: Optional[int] = Field(default=None, nullable=True)
    reconciled_depreciation: Optional[int] = Field(default=None, nullable=True)
    reconciled_cost_of_revenue: Optional[int] = Field(default=None, nullable=True)
    ebitda: Optional[int] = Field(default=None, nullable=True)
    ebit: Optional[int] = Field(default=None, nullable=True)
    net_interest_income: Optional[int] = Field(default=None, nullable=True)
    interest_expense: Optional[int] = Field(default=None, nullable=True)
    interest_income: Optional[int] = Field(default=None, nullable=True)
    normalized_income: Optional[float] = Field(default=None, nullable=True)
    net_income_from_continuing_and_discontinued_operation: Optional[int] = Field(default=None, nullable=True)
    total_expenses: Optional[int] = Field(default=None, nullable=True)
    total_operating_income_as_reported: Optional[int] = Field(default=None, nullable=True)
    diluted_average_shares: Optional[int] = Field(default=None, nullable=True)
    basic_average_shares: Optional[int] = Field(default=None, nullable=True)
    diluted_eps: Optional[float] = Field(default=None, nullable=True)
    basic_eps: Optional[float] = Field(default=None, nullable=True)
    diluted_ni_availto_com_stockholders: Optional[int] = Field(default=None, nullable=True)
    net_income_common_stockholders: Optional[int] = Field(default=None, nullable=True)
    net_income: Optional[int] = Field(default=None, nullable=True)
    net_income_including_noncontrolling_interests: Optional[int] = Field(default=None, nullable=True)
    net_income_continuous_operations: Optional[int] = Field(default=None, nullable=True)
    tax_provision: Optional[int] = Field(default=None, nullable=True)
    pretax_income: Optional[int] = Field(default=None, nullable=True)
    other_income_expense: Optional[int] = Field(default=None, nullable=True)
    other_non_operating_income_expenses: Optional[int] = Field(default=None, nullable=True)
    special_income_charges: Optional[int] = Field(default=None, nullable=True)
    write_off: Optional[int] = Field(default=None, nullable=True)
    gain_on_sale_of_security: Optional[int] = Field(default=None, nullable=True)
    net_non_operating_interest_income_expense: Optional[int] = Field(default=None, nullable=True)
    interest_expense_non_operating: Optional[int] = Field(default=None, nullable=True)
    interest_income_non_operating: Optional[int] = Field(default=None, nullable=True)
    operating_income: Optional[int] = Field(default=None, nullable=True)
    operating_expense: Optional[int] = Field(default=None, nullable=True)
    research_and_development: Optional[int] = Field(default=None, nullable=True)
    selling_general_and_administration: Optional[int] = Field(default=None, nullable=True)
    selling_and_marketing_expense: Optional[int] = Field(default=None, nullable=True)
    general_and_administrative_expense: Optional[int] = Field(default=None, nullable=True)
    other_gand_a: Optional[int] = Field(default=None, nullable=True)
    gross_profit: Optional[int] = Field(default=None, nullable=True)
    cost_of_revenue: Optional[int] = Field(default=None, nullable=True)
    total_revenue: Optional[int] = Field(default=None, nullable=True)
    operating_revenue: Optional[int] = Field(default=None, nullable=True)


# --- Backward Compatibility ---
IncomeStatement = QuarterlyIncomeStatement
