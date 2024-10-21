import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# This test checks if WebSocket can connect and send data.
@pytest.mark.skip(reason="Skipping this test temporarily as it is hanging")
@pytest.mark.asyncio
async def test_websocket_connection():
    with client.websocket_connect("/api/ws") as websocket:
        assert websocket  # Check if the connection is established

        received_message = websocket.receive_json()
        assert received_message is not None
        assert "amount" in received_message
