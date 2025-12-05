import os
from dotenv import load_dotenv
# from google.genai.client import AsyncClient,Client
from google import genai
from src.models.income_statement import QuarterlyIncomeStatement,ToPullIncomeStatement
from src.models.balance_sheet import QuarterlyBalanceSheet, ToPullBalanceSheet
import json
from pydantic import ValidationError
from google.genai.types import GenerateContentConfig, Tool, GoogleSearch

from src.components.const import LlmModels
from src.components.init_config import logger
from src.services.utils import clean_json_output
from src.prompts.get_income_statement_agent import GetIncomeStatementAgent
from src.prompts.get_balance_sheet_agent import GetBalanceSheetAgent


# Load environment variables from .env file
load_dotenv()


# Configure the Gemini API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    # Changed print to logger.error
    logger.error("GEMINI_API_KEY not found in .env file")
    raise ValueError("GEMINI_API_KEY not found in .env file")
logger.debug(f"GEMINI_API_KEY loaded by genai.configure (masked): {api_key[:4]}...{api_key[-4:]}") # Debug print changed to logger.debug

client = genai.Client(api_key=api_key)
# client_api = client._get_api_client()
# async_client = AsyncClient(client_api)

# Create a GenerativeModel instance
llm = client.models

def get_config_with_search()-> GenerateContentConfig:
    grounding_tool = Tool(
        google_search=GoogleSearch()
    )

    config_with_search = GenerateContentConfig(
        tools=[grounding_tool],
    )
    
    return config_with_search


async def list_available_models():
    """Lists all available Gemini models and their capabilities."""
    logger.info("--- Available Gemini Models ---") # Changed print to logger.info
    for m in genai.list_models():
        logger.info(f"Name: {m.name}") # Changed print to logger.info
        logger.info(f"  Supported Generation Methods: {m.supported_generation_methods}") # Changed print to logger.info
        logger.info(f"  Description: {m.description}") # Changed print to logger.info
        logger.info("-" * 30) # Changed print to logger.info
    logger.info("------------------------------\n") # Changed print to logger.info

async def get_income_statement(company: str) -> QuarterlyIncomeStatement:
    """
    Fetches the income statement for a given company using an LLM to perform a web search.
    Parses the result into an IncomeStatement Pydantic model.
    """

    prompt = GetIncomeStatementAgent.get_formatted_prompt(company=company)
    try:
        response = llm.generate_content(
            model=LlmModels.GEMINI_2_5_FLASH,
            contents=prompt, 
            config=get_config_with_search()
        )
        
        gemini_output_text = response.text
        logger.info(f"LLM Raw Output: {gemini_output_text}")

        cleaned_text = clean_json_output(gemini_output_text)
        # Correctly parse and validate the JSON using the ToPullIncomeStatement model
        pulled_data = ToPullIncomeStatement.model_validate_json(cleaned_text)
        logger.debug(f"Parsed LLM Output: {pulled_data}")

        # Create the final statement with derived metrics
        final_statement = QuarterlyIncomeStatement.from_pulled_data(pulled_data)
        logger.debug(f"Final income statement data: {final_statement}")
        
        return final_statement

    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from Gemini: {e}")
        return None
    except ValidationError as e:
        logger.error(f"Pydantic validation error: {e}")
        return None
    except Exception as e:
        logger.exception(f"An unexpected error occurred during LLM call: {e}")
        return None

async def get_balance_sheet(company: str) -> QuarterlyBalanceSheet:
    """
    Fetches the balance sheet for a given company using an LLM to perform a web search.
    Parses the result into a BalanceSheet Pydantic model.
    """

    prompt = GetBalanceSheetAgent.get_formatted_prompt(company=company)
    try:
        response = llm.generate_content(
            model=LlmModels.GEMINI_2_5_FLASH,
            contents=prompt, 
            config=get_config_with_search()
        )
        
        gemini_output_text = response.text
        logger.info(f"LLM Raw Output: {gemini_output_text}")

        cleaned_text = clean_json_output(gemini_output_text)
        # Correctly parse and validate the JSON using the ToPullBalanceSheet model
        pulled_data = ToPullBalanceSheet.model_validate_json(cleaned_text)
        logger.debug(f"Parsed LLM Output: {pulled_data}")

        # Create the final statement with derived metrics
        final_statement = QuarterlyBalanceSheet.from_pulled_data(pulled_data)
        logger.debug(f"Final balance sheet data: {final_statement}")
        
        return final_statement

    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from Gemini: {e}")
        return None
    except ValidationError as e:
        logger.error(f"Pydantic validation error: {e}")
        return None
    except Exception as e:
        logger.exception(f"An unexpected error occurred during LLM call: {e}")
        return None

# The rest of the service functions will be added in subsequent tasks
# Call list_available_models during development to check available models
# await list_available_models() # This line would be uncommented to run the list function.