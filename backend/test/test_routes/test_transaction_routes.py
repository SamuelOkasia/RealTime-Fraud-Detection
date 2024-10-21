import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_post_transaction():
    # Dummy transaction data
    transaction_data = {
        "amount": 200,
        "location": "Los Angeles",
        "user_id": "user456",
        "time": "2024-09-22T15:30:00"
    }

    # Send POST request to the transaction route
    response = client.post("/api/transaction", json=transaction_data)

    # Check if the response status code is 200 OK
    assert response.status_code == 200

    # Verify the response contains the expected status message
    response_data = response.json()
    assert response_data["status"] == "transaction sent to Kafka"
    assert response_data["transaction"]["amount"] == transaction_data["amount"]
