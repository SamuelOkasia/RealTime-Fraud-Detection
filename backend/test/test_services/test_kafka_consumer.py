# test/test_kafka_consumer.py

import pytest
from unittest.mock import patch, MagicMock
from app.consumers.kafka_consumer import consume_transactions
import asyncio

@pytest.mark.asyncio
@patch('app.consumers.kafka_consumer.AIOKafkaConsumer')
@patch('app.consumers.kafka_consumer.save_transaction_to_db')
@patch('app.consumers.kafka_consumer.fraud_model')
@patch('app.consumers.kafka_consumer.preprocess_transaction')
async def test_consume_transactions(
        mock_preprocess_transaction, mock_fraud_model, 
        mock_save_transaction, mock_kafka_consumer):

    # Mock Kafka consumer's async message stream
    mock_message = MagicMock()
    mock_message.value = {
        'amount': 100,
        'location': 'New York',
        'user_id': 'user123',
        'time': '2024-09-22T12:34:56'
    }

    # Mock the start method to return an awaitable
    async def mock_start():
        return None
    mock_kafka_consumer().start.side_effect = mock_start

    # Mock the stop method to return an awaitable
    async def mock_stop():
        return None
    mock_kafka_consumer().stop.side_effect = mock_stop

    # Mock the async for loop in Kafka consumer
    async def mock_aiter():
        yield mock_message
    mock_kafka_consumer().__aiter__.side_effect = mock_aiter

    # Mock the fraud detection and preprocessing functions
    mock_preprocess_transaction.return_value = [1, 2, 3]  # Dummy processed data
    mock_fraud_model.predict.return_value = [0]  # No fraud detected

    # Call the async function to be tested
    await consume_transactions()

    # Ensure the transaction is saved to the DB
    mock_save_transaction.assert_called_once_with(mock_message.value, False)
    mock_fraud_model.predict.assert_called_once()
