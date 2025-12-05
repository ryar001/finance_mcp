from src.prompts.prompt_base import BasePrompt
from src.models.income_statement import QuarterlyIncomeStatement
from src.prompts.sources import GET_INCOME_STATEMENT_SOURCES

class GetIncomeStatementAgent(BasePrompt):
    get_income_statement_sources = GET_INCOME_STATEMENT_SOURCES
    json_schema = QuarterlyIncomeStatement.model_json_schema()

    prompt = """
        You are an AI assistant specialized in financial data extraction. Your task is to retrieve the latest quarterly income statement for {company}.

        1. Use official sources first, in this order of priority:
        - use search tool to find The company's SEC filings (10-Q or 10-K for the relevant quarter)
 
        From the income statement, extract all fields necessary to populate the provided JSON schema ({json_schema}). 
        Do not use any other sources or hallucinate data.

        - Provide all numerical values in full USD (do not round, do not use millions/thousands notation). 
        - If a field is missing in official sources, return `null`.

        Output only a single, valid JSON object following the provided schema exactly. Do not add explanations, comments, or extra text.
        """

    @classmethod
    def get_formatted_prompt(cls,company: str,get_income_statement_sources: list[str]=None, json_schema: str=None, **kwargs)-> str:
        if get_income_statement_sources is None:
            get_income_statement_sources = cls.get_income_statement_sources
        if json_schema is None:
            json_schema = cls.json_schema
        return cls.prompt.format(company=company,get_income_statement_sources=get_income_statement_sources,json_schema=json_schema,**kwargs)