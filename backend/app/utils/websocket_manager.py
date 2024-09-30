from fastapi import WebSocket, WebSocketDisconnect
from app.utils.logging_config import setup_logging
import logging

# Initialize logging for this module
setup_logging()  # Set up logging configuration
logger = logging.getLogger(__name__)  # Create a logger for this module

# List to keep track of connected WebSocket clients
connected_clients = []

async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint to handle real-time connections from clients.
    
    This function accepts a WebSocket connection from a client, adds it to the list of connected clients, 
    and continuously listens for messages to keep the connection alive. When the client disconnects, 
    the connection is removed from the list.
    
    Args:
        websocket (WebSocket): The WebSocket object representing the client's connection.
    
    Workflow:
    1. Accept the WebSocket connection.
    2. Add the client to the `connected_clients` list.
    3. Keep the connection alive by listening for any message from the client.
    4. Handle disconnection gracefully by removing the client from the `connected_clients` list.
    """
    await websocket.accept()  # Accept the WebSocket connection
    connected_clients.append(websocket)  # Add the connected client to the list
    logger.info(f'Client connected. Total clients: {len(connected_clients)}')  # Log the number of clients connected
    
    try:
        # Keep the connection alive by receiving text (this could be a heartbeat or any other data)
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        # Handle WebSocket disconnection and remove the client from the list
        connected_clients.remove(websocket)
        logger.error(f'Client disconnected. Total clients: {len(connected_clients)}')
        await websocket.close()  # Close the WebSocket connection


async def notify_clients(transaction_data: dict):
    """
    Notify all connected WebSocket clients with the given transaction data.
    
    This function loops through the list of connected WebSocket clients and sends the provided transaction 
    data in JSON format. If any client cannot be reached, it is removed from the list.
    
    Args:
        transaction_data (dict): The transaction data to be sent to the clients in JSON format.
    
    Workflow:
    1. Loop through all connected clients.
    2. Attempt to send the transaction data to each client.
    3. If a client cannot be notified (e.g., due to a disconnection), remove the client from the list.
    """
    logger.info(f'Notifying {len(connected_clients)} clients')  # Log the number of clients to notify
    
    for client in connected_clients:
        try:
            logger.info(f'Sending data to client: {transaction_data}')  # Log the data being sent
            await client.send_json(transaction_data)  # Send the transaction data in JSON format
        except Exception as e:
            # Log the error and remove the client from the list if an exception occurs
            logger.error(f"Error notifying client: {e}")
            connected_clients.remove(client)  # Remove the client from the list
