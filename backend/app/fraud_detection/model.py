import pickle
import os

def load_model():
    """
    Load the fraud detection model from a pickle file.

    Returns:
        model (sklearn model): The loaded machine learning model.
    """
    # Path to the pre-trained fraud detection model (saved as a .pkl file)
    model_path = os.path.join(os.path.dirname(__file__), 'fraud_detection_model.pkl')

    # Load the model using pickle
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)

    return model


def predict_fraud(transaction_data):
    """
    Predict if a given transaction is fraudulent using the pre-loaded model.

    Args:
        transaction_data (dict): A dictionary containing transaction details. 
                                 Expected keys are 'amount' and 'location'.

    Returns:
        int: Fraud status, where 0 indicates not fraudulent and 1 indicates fraudulent.
    """
    # Load the fraud detection model
    model = load_model()

    # Prepare the transaction features for model input
    # Example assumes the model expects 'amount' and 'location' as features
    features = [[transaction_data['amount'], transaction_data['location']]]

    # Make the prediction using the loaded model
    fraud_prediction = model.predict(features)

    # Return the fraud status (0 for non-fraudulent, 1 for fraudulent)
    return fraud_prediction[0]
