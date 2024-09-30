# backend/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.utils.database import Base

@pytest.fixture(scope='function')
def test_db():
    # Set up an in-memory SQLite database
    engine = create_engine('sqlite:///:memory:')
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create all the tables in the database
    Base.metadata.create_all(bind=engine)
    
    # Provide the test with a session
    db = TestingSessionLocal()
    try:
        yield db  # Testing happens here
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)  # Clean up the tables after test
import sys
import os

# Add the 'backend' directory (root) to the sys.path for module resolution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))