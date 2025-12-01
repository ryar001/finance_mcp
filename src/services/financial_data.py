import instructor
from dotenv import load_dotenv
import os
import google.generativeai as genai
from models.income_statement import IncomeStatement
from models.balance_sheet import BalanceSheet
from models.cash_flow_statement import CashFlowStatement
from .const import LlmModels

load_dotenv()

MODEL_NAME = LlmModels.GEMINI_2_5_FLASH.value

# Configure the Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create a client with instructor
client = instructor.from_provider(
    MODEL_NAME, 
    mode=instructor.Mode.GENAI_STRUCTURED_OUTPUTS
)

class FinancialDataService:
    def get_income_statement(self, company: str) -> IncomeStatement:
        return client.generate_content(
            model=MODEL_NAME,
            response_model=IncomeStatement,
            messages=[
                {"role": "user", "parts": [f"Get the income statement for {company} for the latest fiscal year."]}
            ]
        )

    def get_balance_sheet(self, company: str) -> BalanceSheet:
        return client.generate_content(
            model=MODEL_NAME,
            response_model=BalanceSheet,
            messages=[
                {"role": "user", "parts": [f"Get the balance sheet for {company} for the latest fiscal year."]}
            ]
        )

    def get_cash_flow_statement(self, company: str) -> CashFlowStatement:
        return client.generate_content(
            model=MODEL_NAME,
            response_model=CashFlowStatement,
            messages=[
                {"role": "user", "parts": [f"Get the cash flow statement for {company} for the latest fiscal year."]}
            ]
        )
