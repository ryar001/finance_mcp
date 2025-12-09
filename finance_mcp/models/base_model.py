from sqlmodel import SQLModel, Field
import datetime
from typing import Optional

class BaseStatementsModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    ticker: str = Field(description="The stock ticker symbol for the company (e.g., 'AAPL').", primary_key=True)  
    last_updated: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(tz=datetime.timezone.utc), nullable=False)
    last_earnings_date: Optional[str] = Field(
        default=None, description="The date of the last earnings report, in any common format (e.g., '2025-10-30')."
    )
