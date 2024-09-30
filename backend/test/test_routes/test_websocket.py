import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# This test checks if WebSocket can connect and send data.
@pytest.mark.asyncio
async def test_websocket_connection():
    with client.websocket_connect("/ws") as websocket:
        assert websocket  # Check if the connection is established

        # Optional: You can simulate sending a message and receiving one.
        # Here, you can check if the initial transaction data is sent to the frontend.
        received_message = websocket.receive_json()
        assert received_message is not None
        assert "amount" in received_message
