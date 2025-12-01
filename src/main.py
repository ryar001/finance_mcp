from fastapi import FastAPI, Depends
from services.financial_data import FinancialDataService
from models.income_statement import IncomeStatement
from models.balance_sheet import BalanceSheet
from models.cash_flow_statement import CashFlowStatement
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI()

def get_financial_data_service():
    return FinancialDataService()

@app.get("/income_statement/{company}", response_model=IncomeStatement)
def get_income_statement(
    company: str,
    service: FinancialDataService = Depends(get_financial_data_service)
):
    """
    MCP function to get the income statement for a company.
    """
    income_statement = service.get_income_statement(company)
    return income_statement

@app.get("/balance_sheet/{company}", response_model=BalanceSheet)
def get_balance_sheet(
    company: str,
    service: FinancialDataService = Depends(get_financial_data_service)
):
    """
    MCP function to get the balance sheet for a company.
    """
    balance_sheet = service.get_balance_sheet(company)
    return balance_sheet

@app.get("/cash_flow_statement/{company}", response_model=CashFlowStatement)
def get_cash_flow_statement(
    company: str,
    service: FinancialDataService = Depends(get_financial_data_service)
):
    """
    MCP function to get the cash flow statement for a company.
    """
    cash_flow_statement = service.get_cash_flow_statement(company)
    return cash_flow_statement

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)