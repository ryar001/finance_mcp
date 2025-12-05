from yfinance import Ticker

from src.models.income_statement import QuarterlyIncomeStatement
from src.models.balance_sheet import QuarterlyBalanceSheet
from src.models.cash_flow_statement import QuarterlyCashFlowStatement
import json
from pydantic import ValidationError
from typing import Dict,Tuple

from src.components.const import YFinanceEnum
from src.components.init_config import logger
from src.components.utils import map_income_statement,map_balance_sheet, map_cash_flow_statement


async def get_income_statement(ticker: str, freq: YFinanceEnum.Freq = None,date_format: str = "%d/%m/%Y") -> Tuple[Dict[str, QuarterlyIncomeStatement],list[str]]:
    """
    Fetches the income statement for a given company using an LLM to perform a web search.
    Parses the result into an IncomeStatement Pydantic model.
    """
    try:
        response = Ticker(ticker.upper()).get_income_stmt(freq=freq or YFinanceEnum.Freq.QUARTERLY)
        final = {}
        missing_keys = []
        for col_name,series in response.items():
            date = col_name.strftime(date_format)
            final[date],missing_keys = map_income_statement(series,date,ticker)
        logger.debug(f"[{get_income_statement.__name__}] LLM Raw Output: {final}")
        
        return final,missing_keys

    except json.JSONDecodeError as e:
        logger.error(f"[{get_income_statement.__name__}] Error decoding JSON from Gemini: {e}")
        return None,[]
    except ValidationError as e:
        logger.error(f"[{get_income_statement.__name__}] Pydantic validation error: {e}")
        return None,[]
    except Exception as e:
        logger.exception(f"[{get_income_statement.__name__}] An unexpected error occurred during LLM call: {e}")
        return None,[]

async def get_balance_sheet(ticker: str, freq: YFinanceEnum.Freq = None,date_format: str = "%d/%m/%Y") -> Tuple[Dict[str, QuarterlyBalanceSheet],list[str]]:
    """
    Fetches the balance sheet for a given company using yfinance.
    Parses the result into a BalanceSheet Pydantic model.
    """

    try:
        # Fetch data
        response = Ticker(ticker.upper()).get_balance_sheet(freq=freq or YFinanceEnum.Freq.QUARTERLY)
        
        # We need to pick one quarter to return. Assuming latest.
        # response is a DataFrame where columns are Dates.
        if response.empty:
            logger.warning(f"[{get_balance_sheet.__name__}] No data found for {ticker}")
            return None,[]
        final = {}
        missing_keys = []
        for col_name,series in response.items():
            date = col_name.strftime(date_format)
            final[date],missing_keys = map_balance_sheet(series,date,ticker)
        logger.debug(f"[{get_balance_sheet.__name__}] LLM Raw Output: {final}")
        
        return final,missing_keys

    except Exception as e:
        logger.exception(f"[{get_balance_sheet.__name__}] An unexpected error occurred: {e}")
        return None,[]

async def get_cashflow_statement(ticker: str, freq: YFinanceEnum.Freq = None,date_format: str = "%d/%m/%Y") -> Tuple[Dict[str, QuarterlyCashFlowStatement],list[str]]:
    """
    Fetches the cash flow statement for a given company using yfinance.
    Parses the result into a CashFlowStatement Pydantic model.
    """

    try:
        # Fetch data
        response = Ticker(ticker.upper()).get_cash_flow(freq=freq or YFinanceEnum.Freq.QUARTERLY)
        
        # We need to pick one quarter to return. Assuming latest.
        # response is a DataFrame where columns are Dates.
        if response.empty:
            logger.warning(f"[{get_cashflow_statement.__name__}] No data found for {ticker}")
            return None,[]
        final = {}
        missing_keys = []
        for col_name,series in response.items():
            date = col_name.strftime(date_format)
            final[date],missing_keys = map_cash_flow_statement(series,date,ticker)
        logger.debug(f"[{get_cashflow_statement.__name__}] LLM Raw Output: {final}")
        
        return final,missing_keys

    except Exception as e:
        logger.exception(f"[{get_cashflow_statement.__name__}] An unexpected error occurred: {e}")
        return None,[]

# The rest of the service functions will be added in subsequent tasks
# Call list_available_models during development to check available models
# await list_available_models() # This line would be uncommented to run the list function.

# if __name__ == "__main__":
#     import asyncio
#     async def main():
#         list_of_models = await list_available_models()
#         print(list_of_models[0])

#         income_statement = await get_income_statement("Apple")
#         print(income_statement)

#         balance_sheet = await get_balance_sheet("Apple")
#         print(balance_sheet)

#     asyncio.run(main())