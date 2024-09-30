# test/test_db_service.py

import pytest
from unittest.mock import MagicMock
from app.services.db_service import save_transaction_to_db
from app.utils.models import Transaction

@pytest.fixture
def mock_db_session():
    # Mock a SQLAlchemy session
    mock_session = MagicMock()

    # Mock the add, commit, and refresh methods
    mock_session.add = MagicMock()
    mock_session.commit = MagicMock()
    mock_session.refresh = MagicMock()

    return mock_session

def test_save_transaction_to_db(mock_db_session):
    # Dummy transaction data
    transaction_data = {
        'amount': 100,
        'location': 'New York',
        'user_id': 'user123',
        'time': '2024-09-22T12:34:56'
    }

    # Call the function with mock session and transaction data
    saved_transaction = save_transaction_to_db(transaction_data, False, db=mock_db_session)

    # Ensure that the transaction was added to the session and committed
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()
