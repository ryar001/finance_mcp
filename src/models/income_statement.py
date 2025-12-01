from sqlmodel import SQLModel, Field
from typing import Optional

class IncomeStatement(SQLModel, table=False):
    revenue: Optional[float] = Field(default=None, description="Total revenue")
    cost_of_goods_sold: Optional[float] = Field(default=None, description="Cost of goods sold")
    gross_profit: Optional[float] = Field(default=None, description="Gross profit")
    operating_expenses: Optional[float] = Field(default=None, description="Operating expenses")
    operating_income: Optional[float] = Field(default=None, description="Operating income")
    net_income: Optional[float] = Field(default=None, description="Net income")
