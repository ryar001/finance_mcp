from sqlmodel import SQLModel, Field
from typing import Optional

class CashFlowStatement(SQLModel, table=False):
    net_income: Optional[float] = Field(default=None, description="Net income")
    depreciation_and_amortization: Optional[float] = Field(default=None, description="Depreciation and amortization")
    cash_from_operations: Optional[float] = Field(default=None, description="Cash from operating activities")
    cash_from_investing: Optional[float] = Field(default=None, description="Cash from investing activities")
    cash_from_financing: Optional[float] = Field(default=None, description="Cash from financing activities")
    net_change_in_cash: Optional[float] = Field(default=None, description="Net change in cash")
