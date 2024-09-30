import pickle
import os

# Load the trained model and scaler
def load_fraud_model():
    """
    Loads the trained fraud detection model and its associated scaler.

    The model and scaler are stored as pickle files and are used to make predictions 
    and preprocess data during transaction analysis.

    Returns:
        tuple: A tuple containing the trained fraud detection model and the scaler.
        
    Raises:
        FileNotFoundError: If the model or scaler files are not found.
        pickle.UnpicklingError: If there is an error during loading of the model or scaler.
    """
    # Define the path to the trained fraud detection model
    model_path = os.path.join(os.path.dirname(__file__), '..', 'fraud_detection', 'fraud_detection_model.pkl')
    with open(model_path, 'rb') as model_file:
        # Load the trained model from the pickle file
        model = pickle.load(model_file)

    # Define the path to the scaler (used for feature scaling)
    scaler_path = os.path.join(os.path.dirname(__file__), '..', 'fraud_detection', 'scaler.pkl')
    with open(scaler_path, 'rb') as scaler_file:
        # Load the scaler from the pickle file
        scaler = pickle.load(scaler_file)

    # Return both the model and the scaler
    return model, scaler
