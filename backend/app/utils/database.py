from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import databases
from dotenv import load_dotenv
from app.utils.config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_DB

# Construct the PostgreSQL database URL using environment variables
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"

# Use the 'databases' package to handle asynchronous database connections
database = databases.Database(DATABASE_URL)

# SQLAlchemy engine to interface with the PostgreSQL database
engine = create_engine(DATABASE_URL)

# SessionLocal provides the session factory that creates new database sessions for requests
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models (all models will inherit from this)
Base = declarative_base()

# Function to create tables in the database based on the defined models
def create_db_and_tables():
    Base.metadata.create_all(bind=engine)
