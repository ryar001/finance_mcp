from src.prompts.prompt_base import BasePrompt
from src.models.balance_sheet import ToPullBalanceSheet
from src.prompts.sources import GET_BALANCE_SHEET_SOURCES

class GetBalanceSheetAgent(BasePrompt):
    get_balance_sheet_sources = GET_BALANCE_SHEET_SOURCES
    json_schema = ToPullBalanceSheet.model_json_schema()

    prompt = """
        You are an AI assistant specialized in financial data extraction.
        Perform a web search to find the latest quarterly balance sheet for {company}.
        
        From the balance sheet, extract all the necessary fields to populate the requested JSON schema.

        source the data from the web search.
        Prioritize the data from the following sources:
        {get_balance_sheet_sources}
        
        Output the result as a single, clean JSON object without any other text.
        Follow the JSON schema exactly as specified:
        {json_schema}
        """

    @classmethod
    def get_formatted_prompt(cls,company: str,get_balance_sheet_sources: list[str]=None, json_schema: str=None, **kwargs)-> str:
        if get_balance_sheet_sources is None:
            get_balance_sheet_sources = cls.get_balance_sheet_sources
        if json_schema is None:
            json_schema = cls.json_schema
        return cls.prompt.format(company=company,get_balance_sheet_sources=get_balance_sheet_sources,json_schema=json_schema,**kwargs)
