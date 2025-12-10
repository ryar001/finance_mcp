Operational Logs:
- finance_server.log: Added log entries for FastMCP server startup.

2025-12-09
What's New:
- finance_mcp/components/const.py: Introduced new constants and enums for YFinance frequencies, LLM models, fiscal quarters, exchanges, and log types.
- finance_mcp/components/init_config.py: Added initialization for logging configuration, including dynamic log directory resolution and loading settings from `settings.yml`.
- finance_mcp/components/logging_utils.py: Implemented a new `LoggingUtils` class for structured logging with `structlog`, supporting JSON and plain-text formats, asynchronous file handlers, and context binding. Includes a comprehensive test suite.
- finance_mcp/components/rotateHandler.py: Added asynchronous file handlers (`AsyncTimedRotatingFileHandler`, `AsyncFileHandler`, `AsyncRotatingFileHandler`) to manage log file rotation without blocking the main thread.
- finance_mcp/components/settings.yml: Created a new YAML configuration file for logging settings (level, format, rotation, directory, file name).
- finance_mcp/components/utils.py: Introduced utility functions for converting camelCase to snake_case, mapping yfinance data to Pydantic models (income statement, balance sheet, cash flow statement), and handling data cleaning.
- finance_mcp/main.py: Set up the main FastAPI application, integrating the MCP server, defining a lifespan context, and including the income statement router.
- finance_mcp/models/balance_sheet.py: Defined the `QuarterlyBalanceSheet` SQLModel with fields for various balance sheet metrics, extending `BaseStatementsModel`.
- finance_mcp/models/base_model.py: Created a `BaseStatementsModel` for common fields across financial statements (id, ticker, last_updated, last_earnings_date).
- finance_mcp/models/cash_flow_statement.py: Defined the `QuarterlyCashFlowStatement` SQLModel with fields for various cash flow statement metrics, extending `BaseStatementsModel`. Added `short_term_debt_payments` and `income_tax_paid_supplemental_data`, `other_non_cash_items` fields.
- finance_mcp/models/income_statement.py: Defined the `QuarterlyIncomeStatement` SQLModel with fields for various income statement metrics, extending `BaseStatementsModel`.
- finance_mcp/prompts/get_balance_sheet_agent.py: Created a prompt template for an AI agent to extract balance sheet data.
- finance_mcp/prompts/get_income_statement_agent.py: Created a prompt template for an AI agent to extract income statement data, emphasizing official sources and strict JSON output.
- finance_mcp/prompts/prompt_base.py: Defined a base class for prompt templates.
- finance_mcp/prompts/sources.py: Defined common data sources for financial statements.
- finance_mcp/routers/income_statement.py: Established FastAPI routes for retrieving income statements, handling requests and exceptions.
- finance_mcp/services/financial_data.py: Implemented asynchronous functions to fetch income statement, balance sheet, and cash flow data using `yfinance` and map them to respective Pydantic models.
- finance_mcp/services/firestore_helper.py: Provided functions for uploading and retrieving financial documents from Google Firestore, including authentication guidance.
- finance_mcp/services/utils.py: Added utility functions for cleaning JSON output, calculating annual totals from quarterly data, and generating NoSQL document IDs.
- finance_mcp/tools/financial_tools.py: Defined asynchronous tools for retrieving income statements, balance sheets, and cash flow statements, leveraging the `financial_data` service.

What's New:
- finance_mcp/main_mcp.py: New file created to initialize the FastMCP server and register financial tools (get_income_statement_tool, get_balance_sheet_tool, get_cashflow_statement_tool).

What's New:
- `dev_mcp.py`: Introduced a new standalone MCP server for development tools, including `run_ai_tracker` for tracking changes, generating AI summaries, and committing.
- `finance_mcp_server.py`: Added a new entry point for the finance MCP server, including stderr redirection to `finance_server.log`.

Refactor:
- `pyproject.toml`: Updated project name to `finance-mcp-jokerssd` and added a `finance-mcp` script entry point. Configured `hatchling` for wheel builds to include the `finance_mcp` package.
- File Restructuring: Moved core source files from `src/` directly into the `finance_mcp/` package structure.
- Import Paths: Updated import statements in test files (`test_live_api.py`, `tests/test_consistency.py`, `tests/test_live_financial_data.py`, `tests/test_mcp_tools.py`, `tests/test_routers.py`) to reflect the new `finance_mcp` package structure.

Removed:
- `src/components/const.py`
- `src/components/init_config.py`
- `src/components/logging_utils.py`
- `src/components/rotateHandler.py`
- `src/components/settings.yml`
- `src/components/utils.py`
- `src/main.py`
- `src/main_mcp.py`
- `src/models/balance_sheet.py`
- `src/models/base_model.py`
- `src/models/cash_flow_statement.py`
- `src/models/income_statement.py`
- `src/prompts/get_balance_sheet_agent.py`
- `src/prompts/get_income_statement_agent.py`
- `src/prompts/prompt_base.py`
- `src/prompts/sources.py`
- `src/routers/income_statement.py`
- `src/services/financial_data.py`
- `src/services/firestore_helper.py`
- `src/services/utils.py`
- `src/tools/financial_tools.py`

Warnings:
- tests/test_live_financial_data.py

What's New:
- tests/test_live_financial_data.py:
    - Imported `get_cashflow_statement` and `QuarterlyCashFlowStatement`.
    - Added `test_get_cash_flow_statement_live` to verify cash flow statement retrieval.
- src/main_mcp.py:
    - Added import for `financial_tools`.
- src/models/cash_flow_statement.py:
    - Added `short_term_debt_payments`, `income_tax_paid_supplemental_data`, and `other_non_cash_items` fields to `QuarterlyCashFlowStatement`.

Refactor:
- src/components/init_config.py:
    - Modified log directory initialization to resolve relative paths from the project root.
- src/components/settings.yml:
    - Updated `log_dir` path to "Logs/General_logs".

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
