import re
import json
from typing import List
from finance_mcp.models.income_statement import QuarterlyIncomeStatement
from finance_mcp.components.const import ExchangesEnum,FiscalQuarterEnum

def clean_json_output(text: str):
    # remove outer single quotes
    if text.startswith("'") and text.endswith("'"):
        text = text[1:-1]

    # remove code fences: ```json or ```
    text = re.sub(r"^```[a-zA-Z]*\s*|\s*```$", "", text.strip(), flags=re.DOTALL)

    return text.strip()


def calculate_annual_from_quarters(quarterly_data: List[QuarterlyIncomeStatement]) -> dict:
    """
    Calculate the annual totals from a list of quarterly income statements.
    Assumes all quarters are for the same company and fiscal year.
    Only sums numeric fields; None is treated as 0.
    """
    fields_to_sum = [
        "revenue",
        "cost_of_goods_sold",
        "operating_expenses",
        "research_and_development_expense",
        "selling_general_admin_expenses",
        "depreciation_and_amortization",
        "interest_income",
        "interest_expense",
        "non_operating_income",
        "income_tax_expense",
        "other_comprehensive_income",
        "preferred_dividends",
        "net_income",
    ]

    annual_totals = {field: 0.0 for field in fields_to_sum}
    
    for q in quarterly_data:
        for field in fields_to_sum:
            value = getattr(q, field, 0.0)
            if value is not None:
                annual_totals[field] += value

    # Optionally, compute EPS
    if quarterly_data[0].weighted_avg_shares_diluted:
        total_net_income = annual_totals.get("net_income", 0.0)
        annual_totals["eps_diluted"] = total_net_income / quarterly_data[0].weighted_avg_shares_diluted
    if quarterly_data[0].weighted_avg_shares_basic:
        total_net_income = annual_totals.get("net_income", 0.0)
        annual_totals["eps_basic"] = total_net_income / quarterly_data[0].weighted_avg_shares_basic

    return annual_totals

def get_nosql_document_id(ticker: str, exchange: str|ExchangesEnum, fiscal_year: int, fiscal_quarter: str|FiscalQuarterEnum)-> str:
    '''
    Returns a document ID for a given ticker, exchange, fiscal year, and fiscal quarter.
    The document ID is in the format: Ticker_Exchange_FiscalYear_FiscalQuarter
    '''
    return f"{ticker}_{ExchangesEnum(exchange).value}_{fiscal_year}_{FiscalQuarterEnum(fiscal_quarter).value}".upper()

if __name__ == "__main__":
    gemini_output_text = """```json
{
  "company_name": "Apple Inc.",
  "ticker": "AAPL",
  "revenue": 416204000000,
  "cost_of_goods_sold": 232253000000,
  "selling_general_admin_expenses": 26177000000,
  "research_and_development_expense": 30076000000,
  "depreciation_and_amortization": null,
  "interest_income": null,
  "interest_expense": null,
  "non_operating_income": 3101000000,
  "income_tax_expense": 19927000000,
  "other_comprehensive_income": null,
  "weighted_avg_shares_basic": 14909471000,
  "weighted_avg_shares_diluted": 14942480000,
  "preferred_dividends": null,
  "last_earnings_date": "30/10/25"
}
```"""
    cleaned = clean_json_output(gemini_output_text)
    data = json.loads(cleaned)
    print(data)