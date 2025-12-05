from src.prompts.prompt_base import BasePrompt
from src.models.income_statement import ToPullIncomeStatement
from src.prompts.sources import GET_INCOME_STATEMENT_SOURCES

class GetIncomeStatementAgent(BasePrompt):
    get_income_statement_sources = GET_INCOME_STATEMENT_SOURCES
    json_schema = ToPullIncomeStatement.model_json_schema()

    prompt = """
        You are an AI assistant specialized in financial data extraction.
        Perform a web search to find the latest quarterly income statement for {company}.
        
        From the income statement, extract all the necessary fields to populate the requested JSON schema.

        source the data from the web search.
        Prioritize the data from the following sources:
        {get_income_statement_sources}
        
        Output the result as a single, clean JSON object without any other text.
        Follow the JSON schema exactly as specified:
        {json_schema}
        """

    @classmethod
    def get_formatted_prompt(cls,company: str,get_income_statement_sources: list[str]=None, json_schema: str=None, **kwargs)-> str:
        if get_income_statement_sources is None:
            get_income_statement_sources = cls.get_income_statement_sources
        if json_schema is None:
            json_schema = cls.json_schema
        return cls.prompt.format(company=company,get_income_statement_sources=get_income_statement_sources,json_schema=json_schema,**kwargs)