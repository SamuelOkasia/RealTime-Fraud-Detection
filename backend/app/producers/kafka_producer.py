from kafka import KafkaProducer
import json
from app.utils.config import KAFKA_BROKER, KAFKA_TOPIC
from datetime import datetime
from app.utils.logging_config import setup_logging
import logging

# Setup logging for this module
setup_logging()  # Initialize logging at the start of the application
logger = logging.getLogger(__name__)  # Create a logger instance for this module

def get_kafka_producer():
    """
    Create and return a KafkaProducer instance.

    This function initializes a KafkaProducer with the appropriate configuration
    for sending messages to the Kafka broker.

    Returns:
        KafkaProducer: A configured Kafka producer instance.
    """
    # Initialize Kafka producer
    return KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER],  # Set the Kafka broker URL
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),  # Serialize data as JSON
        api_version=(2, 6, 0),  # Set the Kafka API version to match the server
        max_request_size=2000000000  # Increase the maximum request size to handle large messages
    )

def send_transaction_to_kafka(transaction):
    """
    Send a transaction message to the Kafka topic.

    This function serializes the transaction data and sends it to the configured Kafka topic.
    It also handles logging and error handling in case the message fails to send.

    Args:
        transaction (dict): A dictionary containing the transaction data to send.
    """
    # Ensure the 'time' field is serialized as ISO format (if it exists as a datetime object)
    if isinstance(transaction.get('time'), datetime):
        transaction['time'] = transaction['time'].isoformat()

    try:
        # Get the Kafka producer instance
        producer = get_kafka_producer()

        # Send the serialized transaction data to the Kafka topic
        producer.send(KAFKA_TOPIC, transaction)

        # Flush to ensure all messages are sent before closing the producer
        producer.flush()

        # Log the successful send event
        logger.info(f"Successfully sent transaction to Kafka: {transaction}")

    except Exception as e:
        # Log any errors that occur during the send process
        logger.error(f"Failed to send transaction to Kafka: {e}", exc_info=True)

    finally:
        # Ensure the producer is closed to release resources
        producer.close()
