
from dotenv import load_dotenv
import logging

from google.cloud import firestore
from google.cloud.firestore import DocumentSnapshot

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


