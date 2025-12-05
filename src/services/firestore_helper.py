
from dotenv import load_dotenv
import logging

from google.cloud import firestore
from google.cloud.firestore import DocumentSnapshot
from src.models.income_statement import QuarterlyIncomeStatement, ToPullIncomeStatement
from src.components.const import QUARTERLY_INCOME_STATEMENT_COLLECTION, FIRESTORE_DATABASE,ExchangesEnum
from src.services.utils import get_nosql_document_id

load_dotenv()

logger = logging.getLogger(__name__)

def upload_income_statement_to_firestore(json_data: dict,document_id: str,db: firestore.Client = None,collection: str = None):
    """
    Uploads a QuarterlyIncomeStatement object to Google Firestore.

    Args:
        json_data: A dictionary containing the data to upload.
        document_id: The ID of the document to upload.
        db: The Firestore client to use. If None, a new client will be created.
        collection: The collection to upload the document to. If None, the default collection will be used.
    """
    # --- Firestore Authentication ---
    # When running on a Google Cloud service (like Cloud Run, Cloud Functions, or Compute Engine),
    # the client library automatically detects the environment's service account and authenticates.
    # No extra configuration is needed besides ensuring that the service account has the
    # necessary IAM permissions for Firestore (e.g., "Cloud Datastore User" role).
    #
    # For local development, you must authenticate by setting up Application Default Credentials.
    # 1. Create a service account and download its JSON key file from the Google Cloud Console.
    # 2. Set the GOOGLE_APPLICATION_CREDENTIALS environment variable to the path of this file.
    #    - On macOS/Linux: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/key.json"
    #    - On Windows:      set GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\your\key.json"
    #

    # Get a reference to the document and upload the data.
    # Using .set() will create the document if it doesn't exist or overwrite it if it does.
    doc_ref = db.collection(collection).document(document_id)
    doc_ref.set(json_data)

    logger.info(f"[{__name__}::{upload_income_statement_to_firestore.__name__}] Successfully uploaded income statement to Firestore with document ID: {document_id}")

    return document_id


def get_document_from_firestore(document_id: str,db: firestore.Client = None,collection: str = None)->DocumentSnapshot|None:
    '''
    Get a document from Firestore.
    Args:
        document_id: The ID of the document to get.
        db: The Firestore client to use. If None, a new client will be created.
        collection: The collection to get the document from. If None, the default collection will be used.
    Returns:
        The document as a QuarterlyIncomeStatement object.
    '''
    doc_ref = db.collection(collection).document(document_id)
    doc = doc_ref.get()
    return doc



if __name__ == '__main__':
    # --- Example Usage ---

    # 1. Create a sample ToPullIncomeStatement object with raw data.
    raw_data = ToPullIncomeStatement(
        company_name="Apple Inc.",
        ticker="AAPL",
        exchange=ExchangesEnum.NASDAQ,
        fiscal_year=2025,
        fiscal_quarter="Q1",
        last_earnings_date="2025-01-30",
        revenue=90000000000,
        cost_of_goods_sold=50000000000,
        selling_general_admin_expenses=10000000000,
        research_and_development_expense=7000000000,
        depreciation_and_amortization=3000000000,
        interest_income=1000000000,
        interest_expense=500000000,
        income_tax_expense=5000000000,
        weighted_avg_shares_diluted=16000000000
    )
    # 2. Create a QuarterlyIncomeStatement from the raw data.
    # This will also calculate the derived financial metrics.
    quarterly_statement = QuarterlyIncomeStatement.from_pulled_data(raw_data)
    json_data = quarterly_statement.model_dump(mode='json')
    collection = QUARTERLY_INCOME_STATEMENT_COLLECTION
    db = firestore.Client(database=FIRESTORE_DATABASE)
    document_id = get_nosql_document_id(quarterly_statement.ticker, quarterly_statement.exchange, quarterly_statement.fiscal_year, quarterly_statement.fiscal_quarter)
    # 3. Upload the final statement to Firestore.
    upload_income_statement_to_firestore(json_data,document_id,db,collection)

    # 4. Get the statement from Firestore.
    doc = get_document_from_firestore(document_id, db, collection)
    if doc.exists:
        statement_dict = doc.to_dict()
        statement = QuarterlyIncomeStatement(**statement_dict)
        print(statement)
    else:
        print(f"Document with ID {document_id} not found.")
