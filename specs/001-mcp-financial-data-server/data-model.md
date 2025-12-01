# Data Model: MCP Financial Data Server

## `EarningsStatement`

This model represents the earnings statement for a company for a specific period.

| Field | Type | Description |
|---|---|---|
| `income_statement` | str | The income statement for the company. |
| `balance_sheet` | str | The balance sheet for the company. |
| `cashflow_statement` | str | The cashflow statement for the company. |

### SQLModel Definition

```python
from typing import Optional
from sqlmodel import SQLModel, Field

class EarningsStatementBase(SQLModel, table=False):
    income_statement: str
    balance_sheet: str
    cashflow_statement: str

class EarningsStatement(EarningsStatementBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    company: str
    period: str

class EarningsStatementCreate(EarningsStatementBase):
    pass

class EarningsStatementRead(EarningsStatementBase):
    id: int
    company: str
    period: str
```
