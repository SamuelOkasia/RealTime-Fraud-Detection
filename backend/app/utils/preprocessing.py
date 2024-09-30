import os
import pickle
import numpy as np
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.utils.database import SessionLocal
from app.utils.models import Transaction
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta

# Load pre-fitted scaler
def load_scaler():
    """
    Loads the pre-trained and pre-fitted scaler from a file for use in scaling new transaction data.
    
    The scaler is used to normalize/scale numeric data (e.g., amount, transaction frequency) to the same scale as the 
    data that the machine learning model was trained on.
    
    Returns:
        scaler (StandardScaler): The pre-fitted scaler object used to transform new transaction data.
    """
    scaler_path = os.path.join(os.path.dirname(__file__), '..', 'fraud_detection', 'scaler.pkl')
    with open(scaler_path, 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)
    return scaler

# Function to fetch transaction frequency from the database
def get_transaction_frequency(user_id, current_time):
    """
    Fetches the number of transactions made by a user in the past 24 hours from the database.
    
    Args:
        user_id (str): The ID of the user whose transaction frequency is being checked.
        current_time (datetime): The time of the current transaction.

    Returns:
        int: The count of transactions made by the user in the past 24 hours.
    """
    db: Session = SessionLocal()
    try:
        # Define the time window for transaction history (e.g., last 24 hours)
        time_window = current_time - timedelta(hours=24)
        
        # Query to get the count of transactions in the last 24 hours for this user
        transaction_count = db.query(func.count(Transaction.id)) \
            .filter(Transaction.user_id == user_id) \
            .filter(Transaction.time >= time_window) \
            .scalar()
        
        return transaction_count
    finally:
        db.close()

# Function to preprocess the incoming transaction for prediction
def preprocess_transaction(transaction_data):
    """
    Preprocesses an incoming transaction for fraud prediction by the ML model.
    
    This includes:
    - Extracting time-based features such as transaction hour and transaction frequency.
    - Encoding categorical features such as transaction location.
    - Scaling numeric features using the pre-fitted scaler.

    Args:
        transaction_data (dict): The transaction data, typically in the following format:
            {
                'user_id': 'user_123',
                'amount': 150.00,
                'location': 'New York',
                'time': '2024-09-28T10:34:15'
            }
    
    Returns:
        np.ndarray: A scaled and preprocessed numpy array ready for input into the fraud detection model.
    """
    # Parse the transaction time
    transaction_time = datetime.strptime(transaction_data['time'], "%Y-%m-%dT%H:%M:%S")
    
    # Get real transaction frequency from the database
    transaction_frequency = get_transaction_frequency(transaction_data['user_id'], transaction_time)

    # Extract the hour of the transaction (for time-of-day feature)
    transaction_hour = transaction_time.hour

    # Create a dictionary for a single transaction with new features
    transaction = {
        'amount': [transaction_data['amount']],  # Transaction amount
        'transaction_frequency': [transaction_frequency],  # Number of transactions in last 24 hours
        'transaction_hour': [transaction_hour],  # Hour of the transaction
        'location_San Francisco': [1 if transaction_data['location'] == 'San Francisco' else 0],  # One-hot encode location
        'location_Los Angeles': [1 if transaction_data['location'] == 'Los Angeles' else 0],
        'location_Chicago': [1 if transaction_data['location'] == 'Chicago' else 0],
        'location_Houston': [1 if transaction_data['location'] == 'Houston' else 0],
    }
    
    # Convert to a numpy array for model input
    X = np.array(list(transaction.values())).reshape(1, -1)

    # Scale the amount and other features
    scaler = load_scaler()
    X_scaled = scaler.fit_transform(X)  # Use the pre-fitted scaler to transform the input features

    return X_scaled
