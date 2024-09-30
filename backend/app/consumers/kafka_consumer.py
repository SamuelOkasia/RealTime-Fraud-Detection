import logging
import json
from kafka import KafkaConsumer
from aiokafka import AIOKafkaConsumer

# Import necessary services and utilities
from app.services.db_service import save_transaction_to_db
from app.services.fraud_detection_service import load_fraud_model
from app.utils.preprocessing import preprocess_transaction
from app.utils.config import KAFKA_BROKER, POSTGRES_USER
from prometheus_client import Counter, Gauge, start_http_server
import time
import asyncio  # Import asyncio for async handling
from app.utils.websocket_manager import notify_clients  # WebSocket client notification utility
from app.utils.logging_config import setup_logging

# Initialize logging at the start of the application
setup_logging()
logger = logging.getLogger(__name__)

# Load the trained fraud detection model and scaler into memory
fraud_model, scaler = load_fraud_model()

# Start Prometheus metrics server on port 8001
start_http_server(8001)

# Define Prometheus metrics for monitoring transaction processing
transactions_processed = Counter('transactions_processed_total', 'Total number of transactions processed')
fraudulent_transactions = Counter('fraudulent_transactions_total', 'Total number of fraudulent transactions')
transaction_processing_time = Gauge('transaction_processing_time', 'Time taken to process a transaction')


def safe_json_deserializer(m):
    """
    Safely deserialize Kafka messages from JSON format.

    Args:
        m (bytes): The message in byte format.

    Returns:
        dict: Deserialized JSON message or None in case of error.
    """
    try:
        if m is None:
            return None
        return json.loads(m.decode('utf-8'))
    except (json.JSONDecodeError, AttributeError) as e:
        logger.error(f"Failed to deserialize message: {m}, Error: {e}")
        return None  # Return None for invalid or malformed messages


async def consume_transactions():
    """
    Consume transaction messages from a Kafka topic, process the data for fraud detection,
    and save the transactions to the database while notifying connected clients via WebSockets.
    """
    
    # Parse Kafka broker list from config (in case of multiple brokers)
    kafka_brokers_list = KAFKA_BROKER.split(",")

    logger.info("Initializing Kafka Consumer...")
    logger.info(f"Kafka broker URL Consumer: {KAFKA_BROKER}")

    # Create an asynchronous Kafka consumer
    consumer = AIOKafkaConsumer(
        'transactions',  # Kafka topic name
        bootstrap_servers=[KAFKA_BROKER],
        value_deserializer=safe_json_deserializer,  # Deserialization for message value
        group_id='transaction-consumers',  # Consumer group to ensure messages are consumed once per group
        auto_offset_reset='earliest',  # Start consuming from the earliest message
        session_timeout_ms=60000,  # Kafka session timeout settings
        heartbeat_interval_ms=10000,
        fetch_max_bytes=2000000000,
        max_partition_fetch_bytes=2000000000,
        request_timeout_ms=65000,
    )

    # Start the Kafka consumer
    await consumer.start()
    try:
        # Consume messages asynchronously
        async for message in consumer:
            try:
                # Track start time for transaction processing time metric
                start_time = time.time()

                # Extract and log the transaction data from the Kafka message
                transaction_data = message.value
                logger.info(f"Consumed transaction: {transaction_data}")

                # Preprocess the transaction for fraud detection model
                preprocessed_transaction = preprocess_transaction(transaction_data)

                # Run fraud detection model to predict if the transaction is fraudulent
                is_fraud = fraud_model.predict(preprocessed_transaction)[0]

                # Update Prometheus metrics
                transactions_processed.inc()  # Increment transaction counter
                if is_fraud:
                    fraudulent_transactions.inc()  # Increment fraud counter if detected

                # Calculate and update the time taken to process the transaction
                processing_duration = time.time() - start_time
                transaction_processing_time.set(processing_duration)

                # Save the transaction data to the database and retrieve the saved record
                saved_transaction = save_transaction_to_db(transaction_data, is_fraud)
                logger.info(f"Saved transaction to DB: {saved_transaction}")

                # Notify WebSocket clients of the transaction status
                await notify_clients({
                    "id": saved_transaction.id,
                    "amount": saved_transaction.amount,
                    "location": saved_transaction.location,
                    "user_id": saved_transaction.user_id,
                    "time": saved_transaction.time.isoformat(),  # Convert to ISO format for frontend compatibility
                    "is_fraud": saved_transaction.is_fraud
                })

            except Exception as e:
                # Log any errors during message consumption and processing
                logger.error(f"Error processing transaction: {e}", exc_info=True)
    finally:
        # Stop the Kafka consumer gracefully when finished
        await consumer.stop()
        logger.info("Kafka consumer stopped")

