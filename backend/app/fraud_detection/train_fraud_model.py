import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier  # New model
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import pickle

# Simulate some fake transaction data with advanced features
def generate_fake_data():
    """
    Generate a synthetic dataset of transaction data with fraud labels.

    Returns:
        pd.DataFrame: A DataFrame containing user transaction data.
    """
    np.random.seed(42)  # Set seed for reproducibility
    
    # Number of samples (transactions)
    num_samples = 1000

    # Simulate transaction features
    user_ids = [f"user_{i}" for i in range(num_samples)]
    amounts = np.random.uniform(1, 1000, size=num_samples)  # Random transaction amounts
    locations = np.random.choice(['New York', 'San Francisco', 'Los Angeles', 'Chicago', 'Houston'], num_samples)
    times = pd.date_range(start="2024-01-01", periods=num_samples, freq='min')  # Transaction timestamps
    
    # Additional features for model training
    transaction_frequency = np.random.randint(1, 20, size=num_samples)  # Transactions per hour
    transaction_hour = times.hour  # Hour of the transaction

    # Mark some transactions as fraudulent (10% fraud rate)
    is_fraud = np.random.choice([0, 1], size=num_samples, p=[0.9, 0.1])

    # Create a DataFrame to hold the transaction data
    data = pd.DataFrame({
        'user_id': user_ids,
        'amount': amounts,
        'location': locations,
        'time': times,
        'transaction_frequency': transaction_frequency,
        'transaction_hour': transaction_hour,
        'is_fraud': is_fraud  # Fraud label
    })

    return data


# Preprocessing data (scaling and encoding)
def preprocess_data(data):
    """
    Preprocess the dataset by encoding categorical features and scaling numerical features.

    Args:
        data (pd.DataFrame): The dataset containing transaction details.

    Returns:
        X_scaled (np.array): Scaled feature matrix.
        y (np.array): Target variable (fraud labels).
        scaler (StandardScaler): Fitted scaler to be saved for future use.
    """
    # One-hot encode categorical 'location'
    data = pd.get_dummies(data, columns=['location'], drop_first=True)
    
    # Separate features (X) and target (y)
    X = data.drop(columns=['user_id', 'time', 'is_fraud'])  # Drop unnecessary columns
    y = data['is_fraud']  # Target variable
    
    # Scale numerical features (amount, transaction_frequency, etc.)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, scaler


# Train the Random Forest model
def train_model():
    """
    Train a Random Forest classifier on the synthetic transaction data to detect fraud.
    
    Saves the trained model and the fitted scaler to files for future use.
    """
    # Generate synthetic transaction data
    data = generate_fake_data()
    
    # Preprocess the data (encode, scale)
    X, y, scaler = preprocess_data(data)  # Preprocessing and scaling

    # Split data into training and testing sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize and train the Random Forest model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Make predictions on the test set
    y_pred = model.predict(X_test)
    
    # Evaluate the model's performance
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model accuracy: {accuracy * 100:.2f}%")

    # Save the scaler for use during inference (feature scaling)
    with open('app/fraud_detection/scaler.pkl', 'wb') as scaler_file:
        pickle.dump(scaler, scaler_file)

    # Save the trained model to a file
    with open('app/fraud_detection/fraud_detection_model.pkl', 'wb') as model_file:
        pickle.dump(model, model_file)
    
    print("Model and scaler trained and saved successfully.")


if __name__ == "__main__":
    # Train the model when running this script directly
    train_model()
