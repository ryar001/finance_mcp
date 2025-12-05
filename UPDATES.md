## Project Update Log: 2025-12-05

### What's New
- **`__version__.py`**:
  - Initial version file added (`__version__ = "0.0.1"`).
- **`src/components/const.py`**:
  - Added `YFinanceEnum` for specifying financial data frequencies (QUARTERLY, YEARLY).
- **`src/components/utils.py`**:
  - Introduced utility functions `camel_to_snake`, `yfinance_to_standard_mappings`, `map_balance_sheet`, `map_income_statement`, and `map_cash_flow_statement` for data mapping.
- **`src/main.py`**:
  - Implemented FastAPI `lifespan` context manager and mounted `/mcp` for the MCP server.
  - Changed root message to "Free Finance MCP".
- **`src/main_mcp.py`**:
  - Integrated `financial_tools` and `dev_tools` into `FastMCP` server initialization.
- **`src/models/balance_sheet.py`**:
  - Introduced a comprehensive `QuarterlyBalanceSheet` model with numerous financial metrics and set `__tablename__ = "quarterly_balance_sheets"`.
- **`src/models/base_model.py`**:
  - Created `BaseStatementsModel` as a common base for financial statements.
- **`src/models/cash_flow_statement.py`**:
  - Defined a detailed `QuarterlyCashFlowStatement` model with extensive cash flow metrics and set `__tablename__ = "quarterly_cash_flow_statements"`.
- **`src/models/income_statement.py`**:
  - Expanded `QuarterlyIncomeStatement` with numerous financial metrics and set `__tablename__ = "quarterly_income_statements"`.
- **`src/services/financial_data.py`**:
  - Added `get_cashflow_statement` function utilizing `yfinance`.
- **`src/tools/financial_tools.py`**:
  - New file introduced to house `get_income_statement_tool`, `get_balance_sheet_tool`, and `get_cashflow_statement_tool`.
- **`tests/test_mcp_tools.py`**:
  - New file added for testing the MCP tools, including income statement, balance sheet, and cash flow statement retrieval.
- **`pyproject.toml`**:
  - Added `pytest`, `yfinance`, and `tabulate` to project dependencies.
- **`uv.lock`**:
  - Updated lock file with new dependencies (`beautifulsoup4`, `curl-cffi`, `multitasking`, `numpy`, `pandas`, `peewee`, `pytz`, `ruff`, `soupsieve`, `tabulate`, `tzdata`, `yfinance`).

### Refactor
- **`src/components/init_config.py`**:
  - Minor adjustments to logging setup, likely due to file rebuild.
- **`src/components/logging_utils.py`**:
  - Internal refactoring for logging setup within the `build` directory, no functional change.
- **`src/components/rotateHandler.py`**:
  - Internal refactoring for logging setup within the `build` directory, no functional change.
- **`src/main.py`**:
  - Moved router inclusion and startup logic to `src/main_mcp.py`.
- **`src/models/balance_sheet.py`**:
  - Replaced older balance sheet models with a single comprehensive `QuarterlyBalanceSheet` inheriting from `BaseStatementsModel`. Removed `from_pulled_data` method.
- **`src/models/cash_flow_statement.py`**:
  - Replaced older cash flow models with a single comprehensive `QuarterlyCashFlowStatement` inheriting from `BaseStatementsModel`.
- **`src/models/income_statement.py`**:
  - Replaced older income statement models with a single comprehensive `QuarterlyIncomeStatement` inheriting from `BaseStatementsModel`. Removed `from_pulled_data` method.
- **`src/prompts/get_balance_sheet_agent.py`**:
  - Updated JSON schema reference and adjusted LLM prompt instructions.
- **`src/prompts/get_income_statement_agent.py`**:
  - Updated JSON schema reference and refined LLM prompt instructions for SEC filings.
- **`src/prompts/sources.py`**:
  - Simplified financial data sources.
- **`src/routers/income_statement.py`**:
  - Adapted to the new return type of `get_income_statement` and refined error handling.
- **`src/services/financial_data.py`**:
  - Switched from LLM-based web search for financial data extraction to `yfinance` library.
- **`src/services/firestore_helper.py`**:
  - Removed example usage of `get_income_statement_from_firestore`.
- **`src/services/utils.py`**:
  - Removed `calculate_annual_from_quarters`.
- **`src/tools/income_statement_tool.py`**:
  - Converted to a standalone async function and updated to new service function signature.
- **`tests/test_consistency.py`**:
  - Updated `test_get_income_statement_consistency` to match new service function return types.
- **`tests/test_live_financial_data.py`**:
  - Updated live tests to reflect `yfinance` integration and new model structures.
- **`tests/test_routers.py`**:
  - Adjusted test for `get_income_statement_route` to account for new return types and error handling.
- **`uv.lock`**:
  - Updated python version constraints.

### Bugfix
- **`src/components/init_config.py`**:
  - Fixed duplicated `print_output` assignment within `build` directory, indicating a proper rebuild.
- **`src/routers/income_statement.py`**:
  - Improved handling of cases where no income statement is found by returning a default, ensuring 200 OK responses.

### Deletions
- **`tests/test_balance_sheet_model.py`**:
  - Removed, likely superseded by new testing approach.
- **`tests/test_financial_data.py`**:
  - Removed, likely superseded by new testing approach.
- **`tests/test_income_statement.py`**:
  - Removed, likely superseded by new testing approach.
- **`tests/test_main_mcp.py`**:
  - Removed, likely superseded by `tests/test_mcp_tools.py`.
- **`tests/test_models.py`**:
  - Removed, likely superseded by new testing approach.
