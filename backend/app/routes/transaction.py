from fastapi import APIRouter, WebSocket, Depends, HTTPException, WebSocketDisconnect
from app.producers.kafka_producer import send_transaction_to_kafka
from app.utils.database import SessionLocal
from app.utils.models import Transaction
from app.utils.schemas import TransactionSchema
from sqlalchemy.orm import Session
from app.utils.websocket_manager import websocket_endpoint, notify_clients, connected_clients
from app.utils.logging_config import setup_logging
import logging

# Initialize logging for the module
setup_logging()  
logger = logging.getLogger(__name__)

# Create an APIRouter instance to handle transaction-related routes
transaction_router = APIRouter()

# Dependency to get a database session
def get_db():
    """
    Dependency function to obtain a database session.

    This function is used as a FastAPI dependency to create and close the session for each request.

    Yields:
        Session: SQLAlchemy session instance.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint to process a new transaction (POST request)
@transaction_router.post("/api/transaction")
async def process_transaction(transaction: TransactionSchema, db: Session = Depends(get_db)):
    """
    Process a transaction by sending it to Kafka and optionally saving it to the database.

    This endpoint processes incoming transactions and sends them to Kafka for further processing.
    The transaction is also converted to a dictionary, and the 'time' field is serialized to ISO format.

    Args:
        transaction (TransactionSchema): The incoming transaction data in the request body.
        db (Session): SQLAlchemy session (injected dependency).

    Returns:
        dict: A response indicating that the transaction was successfully sent to Kafka.
    """
    try:    
        logger.info(f"Transaction received: {transaction}")
        
        # Convert the transaction to a dictionary and ensure 'time' is in ISO format
        transaction_data = transaction.dict()
        transaction_data['time'] = transaction_data['time'].isoformat()

        # Send transaction to Kafka
        send_transaction_to_kafka(transaction_data)

        return {"status": "transaction sent to Kafka", "transaction": transaction}
    
    except Exception as e:
        # Handle any error that occurs during transaction processing
        raise HTTPException(status_code=500, detail=f"Failed to process transaction: {e}")

# Endpoint to fetch the transaction history (GET request)
@transaction_router.get("/api/transactions")
def get_transactions(db: Session = Depends(get_db)):
    """
    Retrieve the history of all transactions stored in the database.

    Args:
        db (Session): SQLAlchemy session (injected dependency).

    Returns:
        List[Transaction]: A list of all transaction records.
    """
    transactions = db.query(Transaction).all()
    return transactions

# WebSocket endpoint to handle real-time transaction updates
@transaction_router.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    """
    Establishes a WebSocket connection to provide real-time transaction updates to connected clients.

    When a client connects via WebSocket, they will initially receive the full transaction history
    and continue to receive real-time updates as new transactions are processed.

    Args:
        websocket (WebSocket): The WebSocket connection instance.
        db (Session): SQLAlchemy session (injected dependency).
    """
    # Accept the WebSocket connection
    await websocket.accept()
    connected_clients.append(websocket)
    logger.info(f"WebSocket connection established. Total clients: {len(connected_clients)}")

    try:
        # Step 1: Send existing transactions from the database to the connected WebSocket client
        transactions = db.query(Transaction).all()
        for transaction in transactions:
            await websocket.send_json({
                "id": transaction.id,
                "amount": transaction.amount,
                "location": transaction.location,
                "user_id": transaction.user_id,
                "time": transaction.time.isoformat(),
                "is_fraud": transaction.is_fraud
            })

        # Step 2: Keep the WebSocket connection open to push real-time updates
        while True:
            await websocket.receive_text()  # Listen for incoming messages 

    except Exception as e:
        # Log any errors that occur during the WebSocket interaction
        logger.error(f"WebSocket error: {e}", exc_info=True)

    except WebSocketDisconnect:
        # Handle the WebSocket disconnection
        connected_clients.remove(websocket)
        logger.info(f"WebSocket client disconnected. Total clients: {len(connected_clients)}")
    
    finally:
        # Clean up WebSocket connection on disconnection or error
        if websocket in connected_clients:
            connected_clients.remove(websocket)
