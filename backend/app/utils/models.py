from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean
from app.utils.database import Base

class Transaction(Base):
    """
    SQLAlchemy model representing a transaction in the system.

    This class defines the structure of the 'transactions' table in the PostgreSQL database. Each instance of the
    `Transaction` class corresponds to a row in the 'transactions' table, which stores data about individual transactions.

    Attributes:
        id (Integer): The primary key of the transaction (unique identifier).
        user_id (String): The ID of the user who made the transaction.
        amount (Float): The monetary amount of the transaction.
        location (String): The geographical location where the transaction occurred.
        time (DateTime): The timestamp of when the transaction occurred.
        is_fraud (Boolean): A boolean value indicating whether the transaction was classified as fraudulent.
    """

    __tablename__ = 'transactions'  # Name of the table in the database
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    amount = Column(Float, nullable=False)
    location = Column(String, nullable=False)
    time = Column(DateTime, nullable=False)
    is_fraud = Column(Boolean, default=False)  # Column to store whether the transaction is fraudulent
