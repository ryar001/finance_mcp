from sqlmodel import SQLModel, Field
from typing import Optional

class BalanceSheet(SQLModel, table=False):
    cash: Optional[float] = Field(default=None, description="Cash and cash equivalents")
    accounts_receivable: Optional[float] = Field(default=None, description="Accounts receivable")
    inventory: Optional[float] = Field(default=None, description="Inventory")
    total_current_assets: Optional[float] = Field(default=None, description="Total current assets")
    property_plant_equipment: Optional[float] = Field(default=None, description="Property, plant, and equipment")
    total_assets: Optional[float] = Field(default=None, description="Total assets")
    accounts_payable: Optional[float] = Field(default=None, description="Accounts payable")
    debt: Optional[float] = Field(default=None, description="Short and long-term debt")
    total_liabilities: Optional[float] = Field(default=None, description="Total liabilities")
    shareholders_equity: Optional[float] = Field(default=None, description="Shareholder's equity")
    total_liabilities_and_equity: Optional[float] = Field(default=None, description="Total liabilities and shareholder's equity")
