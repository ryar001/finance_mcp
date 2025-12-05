import pandas as pd
import re
from typing import Tuple
from src.models.income_statement import QuarterlyIncomeStatement
from src.models.balance_sheet import QuarterlyBalanceSheet
from src.models.cash_flow_statement import QuarterlyCashFlowStatement
from src.components.init_config import logger

from typing import Dict, Any

def camel_to_snake(name: str) -> str:
    # Insert an underscore before capital letters, then lowercase everything
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    snake = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    return snake


def yfinance_to_standard_mappings(series: pd.Series, date_str: str, ticker: str,model: QuarterlyBalanceSheet|QuarterlyIncomeStatement|QuarterlyCashFlowStatement)-> [pd.Series, list[str]]:
    # Clean the data
    data_dict: Dict[str, Any] = {}
    missing_keys = []
    for metric_name, value in series.items():
        if pd.isna(value):
            value = None
            
        metric_str = str(metric_name)
        
        # Strategy 1: Lowercase and underscore (for "Total Assets" -> "total_assets")
        clean_key = camel_to_snake(metric_str.replace(" ", ""))
        
        # Strategy 2: CamelCase to snake_case (for "TotalAssets" or "OrdinarySharesNumber" -> "ordinary_shares_number")
        # If the key has no spaces, try splitting by capital letters


        # Map to model fields
        if clean_key in model.model_fields:
            data_dict[clean_key] = value
        else:
            logger.warning(f"[{yfinance_to_standard_mappings.__name__}] Unknown field: {clean_key}")
            missing_keys.append(clean_key)

    if missing_keys:
        logger.warning(f"[{yfinance_to_standard_mappings.__name__}] Missing keys: {missing_keys}")

    data_dict[ model.ticker.name] = ticker
    data_dict[ model.last_earnings_date.name] = date_str
    # 2. Use model_validate to create the instance and COERCE types
    # Since Pydantic V2, this is the standard way.
    instance = model.model_validate(data_dict)
    return instance,missing_keys
    
def map_balance_sheet(
    series: pd.Series,
    date_str: str,
    ticker: str,
) -> Tuple[QuarterlyBalanceSheet, list[str]]:
    """
    Maps a pandas Series (representing one quarter of balance sheet data)
    to a QuarterlyBalanceSheet Pydantic model.
    """
    return yfinance_to_standard_mappings(series, date_str, ticker, QuarterlyBalanceSheet)


def map_income_statement(
    series: pd.Series,
    date_str: str,
    ticker: str,
) -> Tuple[QuarterlyIncomeStatement, list[str]]:
    """
    Maps a pandas Series (representing one quarter of income statement data)
    to a QuarterlyIncomeStatement Pydantic model.
    """
    return yfinance_to_standard_mappings(series, date_str, ticker, QuarterlyIncomeStatement)

def map_cash_flow_statement(
    series: pd.Series,
    date_str: str,
    ticker: str,
) -> Tuple[QuarterlyCashFlowStatement, list[str]]:
    """
    Maps a pandas Series (representing one quarter of cash flow statement data)
    to a QuarterlyCashFlowStatement Pydantic model.
    """
    return yfinance_to_standard_mappings(series, date_str, ticker, QuarterlyCashFlowStatement)
