from __future__ import annotations
from sqlmodel import SQLModel, Field
from typing import Optional
from src.components.const import ExchangesEnum

class BalanceSheetBase(SQLModel):
    cash: Optional[int] = Field(default=None, description="Cash and cash equivalents")
    accounts_receivable: Optional[int] = Field(default=None, description="Accounts receivable")
    inventory: Optional[int] = Field(default=None, description="Inventory")
    property_plant_equipment: Optional[int] = Field(default=None, description="Property, plant, and equipment")
    accounts_payable: Optional[int] = Field(default=None, description="Accounts payable")
    debt: Optional[int] = Field(default=None, description="Short and long-term debt")
    shareholders_equity: Optional[int] = Field(default=None, description="Shareholder's equity")

class ToPullBalanceSheet(BalanceSheetBase):
    """
    Represents the fields that must be pulled from the
    LLM for a balance sheet.
    """
    company_name: str = Field(description="The official name of the company (e.g., 'Apple Inc.').")
    ticker: str = Field(description="The stock ticker symbol for the company (e.g., 'AAPL').")
    exchange: ExchangesEnum = Field(description="The stock exchange where the company is listed (e.g., 'NASDAQ','NYSE').")
    fiscal_year: int = Field(description="The fiscal year for the report (e.g., 2025).")
    fiscal_quarter: str = Field(description="The fiscal quarter for the report as a string (e.g., 'Q1', 'Q4').")
    last_earnings_date: Optional[str] = Field(
        default=None, description="The date of the last earnings report, in any common format (e.g., '2025-10-30')."
    )

class QuarterlyBalanceSheet(BalanceSheetBase, table=True):
    """
    Represents a quarterly balance sheet, including derived metrics.
    """
    # Primary Key
    company_name: str = Field(description="The official name of the company (e.g., 'Apple Inc.').")
    ticker: str = Field(description="The stock ticker symbol for the company (e.g., 'AAPL').", primary_key=True)
    exchange: ExchangesEnum = Field(description="The stock exchange where the company is listed (e.g., 'NASDAQ','NYSE').", primary_key=True)
    fiscal_year: int = Field(description="The fiscal year for the report (e.g., 2025).", primary_key=True)
    fiscal_quarter: str = Field(description="The fiscal quarter for the report as a string (e.g., 'Q1', 'Q4').", primary_key=True)
    last_earnings_date: Optional[str] = Field(
        default=None, description="The date of the last earnings report, in any common format (e.g., '2025-10-30')."
    )

    # Derived Metrics
    total_current_assets: Optional[int] = Field(default=None, description="Total current assets")
    total_assets: Optional[int] = Field(default=None, description="Total assets")
    total_liabilities: Optional[int] = Field(default=None, description="Total liabilities")
    total_liabilities_and_equity: Optional[int] = Field(default=None, description="Total liabilities and shareholder's equity")

    @classmethod
    def from_pulled_data(cls, pulled_data: ToPullBalanceSheet) -> "QuarterlyBalanceSheet":
        """
        Creates a QuarterlyBalanceSheet instance from raw pulled data,
        calculating the derived financial metrics.
        """
        # --- Calculate Derived Metrics ---
        total_current_assets = (pulled_data.cash or 0) + \
                               (pulled_data.accounts_receivable or 0) + \
                               (pulled_data.inventory or 0)

        total_assets = total_current_assets + (pulled_data.property_plant_equipment or 0)

        total_liabilities = (pulled_data.accounts_payable or 0) + (pulled_data.debt or 0)
        
        total_liabilities_and_equity = total_liabilities + (pulled_data.shareholders_equity or 0)


        return cls(
            # Pass all fields from pulled_data
            **pulled_data.model_dump(),
            # Overwrite with calculated derived metrics
            total_current_assets=total_current_assets,
            total_assets=total_assets,
            total_liabilities=total_liabilities,
            total_liabilities_and_equity=total_liabilities_and_equity
        )