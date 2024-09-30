# test/test_kafka_producer.py
from unittest.mock import patch
from app.producers.kafka_producer import send_transaction_to_kafka

@patch('app.producers.kafka_producer.KafkaProducer')
def test_send_transaction_to_kafka(mock_kafka_producer):
    # Dummy transaction data
    transaction_data = {
        'amount': 100,
        'location': 'New York',
        'user_id': 'user123',
        'time': '2024-09-22T12:34:56'
    }

    # Call the function to be tested
    send_transaction_to_kafka(transaction_data)

    # Check if KafkaProducer's send method was called with correct arguments
    mock_kafka_producer().send.assert_called_with(
        'transactions',
        transaction_data
    )
