from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_get_income_statement_success():
    # This test will initially fail because the endpoint is not yet implemented.
    # We will mock the service layer later to make this a true unit test for the router.
    response = client.get("/api/v1/income_statement?company=AAPL")
    assert response.status_code == 200
    assert response.json()["ticker"] == "AAPL"

def test_get_income_statement_not_found():
    # This test simulates a scenario where the company is not found.
    response = client.get("/api/v1/income_statement?company=NONEXISTENTCOMPANY")
    assert response.status_code == 200
    assert response.json()["ticker"] == "N/A"
