
import sys
from pathlib import Path
from typing import Optional
import datetime # Moved from line 100

from sqlmodel import Field, SQLModel
from src.components.const import ExchangesEnum,FiscalQuarterEnum

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent))


class ToPullIncomeStatement(SQLModel):
    """SQLModel defining the raw financial data to be extracted by the LLM."""
    id: Optional[int] = Field(default=None, primary_key=True)
    company_name: str = Field(description="The official name of the company (e.g., 'Apple Inc.').")
    ticker: str = Field(description="The stock ticker symbol for the company (e.g., 'AAPL').",primary_key=True)
    exchange: ExchangesEnum = Field(description="The stock exchange where the company is listed (e.g., 'NASDAQ','NYSE').",primary_key=True)
    fiscal_year: int = Field(description="The fiscal year for the report (e.g., 2025).",primary_key=True)
    fiscal_quarter: FiscalQuarterEnum = Field(description="The fiscal quarter for the report as a string (e.g., 'Q1', 'Q4').",primary_key=True)
    last_earnings_date: Optional[str] = Field(
        default=None, description="The date of the last earnings report, in any common format (e.g., '2025-10-30')."
    )
    weighted_avg_shares_basic: Optional[int] = Field(
        default=None, description="Basic weighted average shares outstanding. Provide the full numerical value.", nullable=True
    )
    weighted_avg_shares_diluted: Optional[int] = Field(
        default=None, description="Diluted weighted average shares outstanding. Provide the full numerical value.", nullable=True
    )

    revenue: Optional[int] = Field(
        default=None,
        description="Total revenue for the quarter in USD. Provide the full numerical value, not millions or thousands.",
        nullable=True
    )
    cost_of_goods_sold: Optional[int] = Field(
        default=None,
        description="Cost of revenue (or cost of goods sold) for the quarter in USD. Provide the full numerical value.",
        nullable=True
    )
    selling_general_admin_expenses: Optional[int] = Field(
        default=None,
        description="Selling, General & Administrative (SG&A) expenses for the quarter in USD. Provide the full numerical value.",
        nullable=True
    )
    research_and_development_expense: Optional[int] = Field(
        default=None,
        description="Research & Development (R&D) expense for the quarter in USD. Provide the full numerical value.",
        nullable=True
    )
    depreciation_and_amortization: Optional[int] = Field(
        default=None,
        description="Depreciation and amortization expense for the quarter in USD. Provide the full numerical value.",
        nullable=True
    )
    interest_income: Optional[int] = Field(
        default=None, description="Interest income for the quarter in USD. Provide the full numerical value.", nullable=True
    )
    interest_expense: Optional[int] = Field(
        default=None, description="Interest expense for the quarter in USD. Provide the full numerical value.", nullable=True
    )
    non_operating_income: Optional[int] = Field(
        default=None,
        description="Other non-operating income or expense for the quarter in USD. Provide the full numerical value.",
        nullable=True
    )
    income_tax_expense: Optional[int] = Field(
        default=None, description="Income tax expense for the quarter in USD. Provide the full numerical value.", nullable=True
    )
    other_comprehensive_income: Optional[int] = Field(
        default=None,
        description="Other comprehensive income for the quarter in USD. Provide the full numerical value.",
        nullable=True
    )
    preferred_dividends: Optional[int] = Field(
        default=None,
        description="Dividends paid to preferred shareholders for the quarter in USD. Provide the full numerical value.",
        nullable=True
    )


class DerivedIncomeStatement(SQLModel):
    """SQLModel defining the derived financial metrics."""
    gross_profit: Optional[float] = Field(default=None, description="Calculated as Revenue - Cost of Goods Sold.")
    operating_expenses: Optional[float] = Field(default=None, description="Calculated as SG&A + R&D + Depreciation & Amortization.")
    operating_income: Optional[float] = Field(default=None, description="Calculated as Gross Profit - Operating Expenses.")
    pre_tax_income: Optional[float] = Field(default=None, description="Calculated as Operating Income + Interest Income - Interest Expense + Non-Operating Income.")
    net_income: Optional[float] = Field(default=None, description="Calculated as Pre-Tax Income - Income Tax Expense.")
    net_income_common: Optional[float] = Field(default=None, description="Calculated as Net Income - Preferred Dividends.")
    ebitda: Optional[float] = Field(default=None, description="Calculated as Operating Income + Depreciation & Amortization.")
    comprehensive_income: Optional[float] = Field(default=None, description="Calculated as Net Income + Other Comprehensive Income.")
    eps_basic: Optional[float] = Field(default=None, description="Calculated as Net Income for Common Shareholders / Weighted Average Basic Shares.")
    eps_diluted: Optional[float] = Field(default=None, description="Calculated as Net Income for Common Shareholders / Weighted Average Diluted Shares.")


class IncomeStatementBase(ToPullIncomeStatement, DerivedIncomeStatement):
    """Composed base model for the complete income statement."""



class QuarterlyIncomeStatement(IncomeStatementBase, table=True):
    """SQLModel for storing quarterly income statements in the database."""
    __tablename__ = "quarterly_income_statements"
    last_updated: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(tz=datetime.timezone.utc), nullable=False)
    last_earnings_date: Optional[str] = Field(default=None, nullable=True)

    @classmethod
    def from_pulled_data(cls, pulled_data: 'ToPullIncomeStatement') -> 'QuarterlyIncomeStatement':
        """
        Creates a QuarterlyIncomeStatement instance from raw pulled data
        and calculates all derived financial metrics.
        """
        # Coalesce None values to 0.0 for calculation, accessing attributes directly
        revenue = pulled_data.revenue or 0.0
        cogs = pulled_data.cost_of_goods_sold or 0.0
        sga = pulled_data.selling_general_admin_expenses or 0.0
        rd = pulled_data.research_and_development_expense or 0.0
        da = pulled_data.depreciation_and_amortization or 0.0
        interest_income = pulled_data.interest_income or 0.0
        interest_expense = pulled_data.interest_expense or 0.0
        non_op_income = pulled_data.non_operating_income or 0.0
        tax = pulled_data.income_tax_expense or 0.0
        pref_dividends = pulled_data.preferred_dividends or 0.0
        oci = pulled_data.other_comprehensive_income or 0.0

        # Calculate derived metrics
        gross_profit = revenue - cogs
        operating_expenses = sga + rd + da
        operating_income = gross_profit - operating_expenses
        pre_tax_income = operating_income + interest_income - interest_expense + non_op_income
        net_income = pre_tax_income - tax
        net_income_common = net_income - pref_dividends
        ebitda = operating_income + da
        comprehensive_income = net_income + oci

        if pulled_data.weighted_avg_shares_basic and pulled_data.weighted_avg_shares_basic > 0:
            eps_basic = net_income_common / pulled_data.weighted_avg_shares_basic
        else:
            eps_basic = 0.0

        if pulled_data.weighted_avg_shares_diluted and pulled_data.weighted_avg_shares_diluted > 0:
            eps_diluted = net_income_common / pulled_data.weighted_avg_shares_diluted
        else:
            eps_diluted = 0.0

        # Add derived metrics to the raw data for final model instantiation
        derived_metrics = {
            "gross_profit": gross_profit,
            "operating_expenses": operating_expenses,
            "operating_income": operating_income,
            "pre_tax_income": pre_tax_income,
            "net_income": net_income,
            "net_income_common": net_income_common,
            "ebitda": ebitda,
            "comprehensive_income": comprehensive_income,
            "eps_basic": eps_basic,
            "eps_diluted": eps_diluted
        }

        return cls(**pulled_data.model_dump(), **derived_metrics)


# --- Backward Compatibility ---
# Alias for other parts of the codebase that might still use the old name.
IncomeStatement = QuarterlyIncomeStatement
