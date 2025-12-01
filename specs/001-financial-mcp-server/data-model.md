# Data Model: Financial MCP Server

## IncomeStatement

Represents the financial data for an income statement.

### Fields

- **revenue**: `float`
- **cost_of_goods_sold**: `float`
- **gross_profit**: `float`
- **operating_expenses**: `float`
- **operating_income**: `float`
- **non_operating_income**: `float`
- **pre_tax_income**: `float`
- **income_tax_expense**: `float`
- **net_income**: `float`

## BalanceSheet

Represents the financial data for a balance sheet.

### Fields

- **assets**:
    - **current_assets**:
        - **cash_and_cash_equivalents**: `float`
        - **accounts_receivable**: `float`
        - **inventory**: `float`
    - **non_current_assets**:
        - **property_plant_and_equipment**: `float`
        - **goodwill**: `float`
        - **intangible_assets**: `float`
- **liabilities**:
    - **current_liabilities**:
        - **accounts_payable**: `float`
        - **short_term_debt**: `float`
    - **non_current_liabilities**:
        - **long_term_debt**: `float`
- **equity**:
    - **common_stock**: `float`
    - **retained_earnings**: `float`

## CashFlowStatement

Represents the financial data for a cash flow statement.

### Fields

- **operating_activities**:
    - **net_income**: `float`
    - **depreciation_and_amortization**: `float`
    - **change_in_working_capital**: `float`
- **investing_activities**:
    - **capital_expenditures**: `float`
    - **acquisitions**: `float`
- **financing_activities**:
    - **issuance_of_stock**: `float`
    - **issuance_of_debt**: `float`
    - **payment_of_dividends**: `float`
