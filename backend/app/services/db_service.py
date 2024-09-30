from sqlalchemy.orm import Session
from app.utils.database import SessionLocal
from app.utils.models import Transaction
from datetime import datetime

def save_transaction_to_db(transaction_data, is_fraud, db: Session = None):
    """
    Save a transaction to the database.

    This function takes in transaction data and a fraud status, then saves the transaction
    to the database. It also supports using an existing database session if provided.

    Args:
        transaction_data (dict): A dictionary containing the transaction details. 
            Required fields include 'user_id', 'amount', 'location', and 'time'.
        is_fraud (bool): A boolean indicating whether the transaction is fraudulent.
        db (Session, optional): SQLAlchemy session instance. If not provided, a new session is created.

    Returns:
        Transaction: The saved transaction object from the database.

    Raises:
        Exception: If there is any error during the saving process, the transaction is rolled back and the error is logged.
    """
    # Use the provided session (db) if available, otherwise create a new one
    db = db or SessionLocal()
    
    try:
        # Create a new Transaction object with the provided data
        transaction = Transaction(
            user_id=transaction_data['user_id'],
            amount=transaction_data['amount'],
            location=transaction_data['location'],
            time=datetime.strptime(transaction_data['time'], "%Y-%m-%dT%H:%M:%S"),  # Parse time into a datetime object
            is_fraud=is_fraud  # Set the fraud status
        )

        # Add and commit the new transaction to the database
        db.add(transaction)
        db.commit()
        
        # Refresh the session to ensure the latest data is returned
        db.refresh(transaction)
        
        print(f"Transaction saved: {transaction}")
        
        return transaction  # Return the saved transaction object

    except Exception as e:
        # Rollback the session in case of an error
        db.rollback()
        print(f"Error saving transaction to the database: {e}")
    
    finally:
        # Close the session after the transaction is processed
        db.close()
