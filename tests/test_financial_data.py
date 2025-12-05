import pytest
from unittest.mock import MagicMock, patch, mock_open
import json
import os

# Set dummy environment variable before imports
os.environ['GEMINI_API_KEY'] = 'test_api_key'

# Mock settings.yml before importing the module that uses it
mock_settings = {
    'log_setting': {
        'log_file': 'test.log',
        'log_dir': './logs',
        'log_level': 'INFO',
        'print_output': False
    }
}

# The mock_open needs to provide the yaml content as a string
with patch('builtins.open', mock_open(read_data='log_setting:\n  log_file: test.log\n  log_dir: ./logs\n  log_level: INFO\n  print_output: false')):
    with patch('yaml.safe_load', return_value=mock_settings):
        # Import the functions to be tested AFTER mocking dependencies
        from src.services.financial_data import get_income_statement, get_balance_sheet, list_available_models, clean_json_output
        from src.models.income_statement import QuarterlyIncomeStatement
        from src.models.balance_sheet import QuarterlyBalanceSheet


@pytest.fixture
def mock_llm_generate_content():
    """Fixture to patch the LLM's generate_content method."""
    with patch('src.services.financial_data.llm.generate_content', new_callable=MagicMock) as mock_generate:
        yield mock_generate

class TestGetIncomeStatement:
    """Tests for the get_income_statement function."""

    @pytest.mark.asyncio
    async def test_successful_data_extraction(self, mock_llm_generate_content):
        """Test successful data extraction and processing."""
        # Arrange
        company = "Apple Inc."
        raw_llm_output = {
            "company_name": company,
            "ticker": "AAPL",
            "exchange": "NASDAQ",
            "fiscal_year": 2023,
            "fiscal_quarter": "Q4",
            "revenue": 394328000000,
            "cost_of_goods_sold": 223546000000,
            "operating_expenses": 55130000000,
            "research_and_development_expense": 5013000000,
            "selling_general_admin_expenses": 50117000000,
            "depreciation_and_amortization": 0,
            "interest_income": 0,
            "interest_expense": 2825000000,
            "non_operating_income": 0,
            "income_tax_expense": 19300000000,
            "weighted_avg_shares_basic": 16327000000,
            "weighted_avg_shares_diluted": 16427000000,
            "preferred_dividends": 0,
            "last_earnings_date": "28/10/23"
        }
        # Simulate the text output from the LLM, which might include markdown/json markers
        mock_response = MagicMock()
        mock_response.text = f"```json\n{json.dumps(raw_llm_output)}\n```"
        mock_llm_generate_content.return_value = mock_response

        # Act
        result = await get_income_statement(company)

        # Assert
        assert result is not None
        assert isinstance(result, QuarterlyIncomeStatement)
        assert result.company_name == company
        assert result.ticker == "AAPL"
        assert result.revenue == 394328000000
        
        # Verify derived metrics are calculated correctly
        assert result.gross_profit == 170782000000
        assert result.operating_income == 115652000000
        assert result.net_income == 93527000000
        assert pytest.approx(result.eps_diluted, 0.001) == 5.693

        # Verify LLM call
        mock_llm_generate_content.assert_called_once()
        _, kwargs = mock_llm_generate_content.call_args
        assert "income statement" in kwargs['contents']
        

    @pytest.mark.asyncio
    async def test_handles_json_decode_error(self, mock_llm_generate_content):
        """Test graceful handling of JSON decoding errors."""
        # Arrange
        company = "Invalid Co"
        mock_response = MagicMock()
        mock_response.text = "This is not valid JSON"
        mock_llm_generate_content.return_value = mock_response

        # Act
        result = await get_income_statement(company)

        # Assert
        assert result is None

    @pytest.mark.asyncio
    async def test_handles_validation_error(self, mock_llm_generate_content):
        """Test graceful handling of Pydantic validation errors for required fields."""
        # Arrange
        company = "Incomplete Data Inc."
        # LLM returns data missing a REQUIRED field (e.g., fiscal_year)
        invalid_data = {
            "company_name": company,
            "ticker": "INC",
            # "fiscal_year": 2023, # Missing required field
            "fiscal_quarter": "Q1",
            "revenue": 100000
        }
        mock_response = MagicMock()
        mock_response.text = json.dumps(invalid_data)
        mock_llm_generate_content.return_value = mock_response

        # Act
        result = await get_income_statement(company)

        # Assert
        assert result is None

    @pytest.mark.asyncio
    async def test_handles_unexpected_llm_exception(self, mock_llm_generate_content):
        """Test graceful handling of unexpected exceptions during the LLM call."""
        # Arrange
        company = "Error Corp"
        mock_llm_generate_content.side_effect = Exception("LLM is down")

        # Act
        result = await get_income_statement(company)

        # Assert
        assert result is None

    @pytest.mark.asyncio
    async def test_handles_none_for_missing_values(self, mock_llm_generate_content):
        """Test that missing optional values are correctly set to None."""
        # Arrange
        company = "New Venture LLC"
        llm_output = {
            "company_name": company,
            "ticker": "NVL",
            "exchange": "NASDAQ",
            "fiscal_year": 2024,
            "fiscal_quarter": "Q1",
            "revenue": 100000,
            "cost_of_goods_sold": 50000,
            "operating_expenses": 30000,
            "research_and_development_expense": 10000,
            "selling_general_admin_expenses": 20000,
            "depreciation_and_amortization": None, # Explicitly None
            "interest_income": 500,
            "interest_expense": 1000,
            "non_operating_income": 0,
            "income_tax_expense": 5000,
            "weighted_avg_shares_basic": 1000000,
            "weighted_avg_shares_diluted": 1000000,
            "preferred_dividends": 0,
            "last_earnings_date": None # Explicitly None
        }
        # The model might return null which becomes None after json.loads
        mock_response = MagicMock()
        mock_response.text = json.dumps(llm_output)
        mock_llm_generate_content.return_value = mock_response
        
        # Act
        result = await get_income_statement(company)

        # Assert
        assert result is not None
        # The model should keep None for optional fields if that's the input
        assert result.depreciation_and_amortization is None
        assert result.last_earnings_date is None

        # Also check that derived metrics were calculated correctly, treating Nones as 0
        # revenue=100k, cogs=50k -> gross_profit=50k
        # op_exp=30k
        # op_inc = 50k - 30k = 20k
        assert result.operating_income == 20000

class TestGetBalanceSheet:
    """Tests for the get_balance_sheet function."""

    @pytest.mark.asyncio
    async def test_successful_data_extraction(self, mock_llm_generate_content):
        """Test successful balance sheet data extraction and processing."""
        # Arrange
        company = "TestCorp"
        raw_llm_output = {
            "company_name": company,
            "ticker": "TC",
            "exchange": "NASDAQ",
            "fiscal_year": 2025,
            "fiscal_quarter": "Q4",
            "last_earnings_date": "01/12/25",
            "cash": 100,
            "accounts_receivable": 200,
            "inventory": 300,
            "property_plant_equipment": 1000,
            "accounts_payable": 150,
            "debt": 500,
            "shareholders_equity": 950,
        }
        mock_response = MagicMock()
        mock_response.text = f"```json\n{json.dumps(raw_llm_output)}\n```"
        mock_llm_generate_content.return_value = mock_response

        # Act
        result = await get_balance_sheet(company)

        # Assert
        assert result is not None
        assert isinstance(result, QuarterlyBalanceSheet)
        assert result.company_name == company
        assert result.ticker == "TC"
        assert result.cash == 100
        
        # Verify derived metrics are calculated correctly
        assert result.total_current_assets == 600
        assert result.total_assets == 1600
        assert result.total_liabilities == 650
        assert result.total_liabilities_and_equity == 1600

        # Verify LLM call
        mock_llm_generate_content.assert_called_once()
        _, kwargs = mock_llm_generate_content.call_args
        assert "balance sheet" in kwargs['contents']

    @pytest.mark.asyncio
    async def test_handles_json_decode_error(self, mock_llm_generate_content):
        """Test graceful handling of JSON decoding errors for balance sheet."""
        # Arrange
        company = "Invalid BS Co"
        mock_response = MagicMock()
        mock_response.text = "This is not valid JSON"
        mock_llm_generate_content.return_value = mock_response

        # Act
        result = await get_balance_sheet(company)

        # Assert
        assert result is None

    @pytest.mark.asyncio
    async def test_handles_validation_error(self, mock_llm_generate_content):
        """Test graceful handling of Pydantic validation errors for balance sheet."""
        # Arrange
        company = "Incomplete BS Inc."
        invalid_data = {
            "company_name": company,
            "ticker": "INCBS",
            # "fiscal_year": 2025, # Missing required field
            "fiscal_quarter": "Q1",
            "cash": 1000
        }
        mock_response = MagicMock()
        mock_response.text = json.dumps(invalid_data)
        mock_llm_generate_content.return_value = mock_response

        # Act
        result = await get_balance_sheet(company)

        # Assert
        assert result is None

    @pytest.mark.asyncio
    async def test_handles_unexpected_llm_exception(self, mock_llm_generate_content):
        """Test graceful handling of unexpected exceptions for balance sheet."""
        # Arrange
        company = "Error BS Corp"
        mock_llm_generate_content.side_effect = Exception("LLM is down")

        # Act
        result = await get_balance_sheet(company)

        # Assert
        assert result is None

class TestCleanJsonOutput:
    """Tests for the clean_json_output utility function."""

    def test_removes_markdown_and_backticks(self):
        """Test that it correctly strips common LLM JSON formatting."""
        raw_text = "```json\n{\"key\": \"value\"}\n```"
        cleaned = clean_json_output(raw_text)
        assert cleaned == "{\"key\": \"value\"}"

    def test_handles_text_with_no_markdown(self):
        """Test that it returns the original string if no markdown is present."""
        raw_text = "{\"key\": \"value\"}"
        cleaned = clean_json_output(raw_text)
        assert cleaned == raw_text

    def test_handles_empty_string(self):
        """Test that it handles empty strings without error."""
        raw_text = ""
        cleaned = clean_json_output(raw_text)
        assert cleaned == ""

class TestListAvailableModels:
    """Tests for the list_available_models function."""

    @pytest.mark.asyncio
    async def test_executes_without_errors(self):
        """Test that list_available_models executes without errors."""
        # This test primarily ensures the function can be called without crashing.
        # It relies on the actual `genai.list_models()` call, but we can mock it
        # to avoid network dependency and speed up tests.
        with patch('src.services.financial_data.genai.list_models') as mock_list:
            mock_model = MagicMock()
            mock_model.name = "models/gemini-pro"
            mock_model.supported_generation_methods = ['generateContent']
            mock_model.description = "A powerful model."
            mock_list.return_value = [mock_model]
            
            # Act & Assert
            try:
                await list_available_models()
            except Exception as e:
                pytest.fail(f"list_available_models raised an exception: {e}")