import os
from dotenv import load_dotenv
from pathlib import Path

from app.utils.logging_config import setup_logging
import logging

# Initialize logging configuration
setup_logging()  # Set up logging based on project-wide configuration
logger = logging.getLogger(__name__)  # Create a logger for this module

# Define the absolute path to the .env file (assuming .env is in the root directory of your project)
env_path = Path('/app/.env')

# Load the environment variables from the .env file
load_dotenv(dotenv_path=env_path)

# Kafka configurations
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")  # Default to 'kafka:9092' if not found in .env
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "transactions")  # Default to 'transactions' if not found in .env

# PostgreSQL configurations
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")  # The password for the PostgreSQL database (from .env)
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")  # Default to 'postgres' if not found in .env
POSTGRES_DB = os.getenv("POSTGRES_DB", "fraud_detection")  # Default to 'fraud_detection' if not found in .env
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")  # Default to 'localhost' if not found in .env
POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)  # Default to port 5432 if not found in .env

# CORS configuration for Frontend access
CORS_ORIGIN = os.getenv("CORS_ORIGIN", "http://localhost:3001")  # Default to 'http://localhost:3001' if not found in .env
