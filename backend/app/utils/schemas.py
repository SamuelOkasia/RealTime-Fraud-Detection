from pydantic import BaseModel, Field
from datetime import datetime

class TransactionSchema(BaseModel):
    """
    Pydantic model schema for transaction data.
    
    This schema is used to validate the incoming transaction data, ensuring that all required fields are present 
    and that the data adheres to the expected format.
    
    Attributes:
        amount (float): The transaction amount, which must be greater than 0.
        location (str): The location where the transaction occurred.
        user_id (str): The ID of the user associated with the transaction.
        time (datetime): The timestamp of the transaction in ISO 8601 format.
    """
    
    amount: float = Field(..., gt=0, description="The amount should be greater than 0")
    location: str
    user_id: str
    time: datetime

    class Config:
        """
        Configuration class for the Pydantic model.
        
        - json_schema_extra: Provides an example of the expected format for the transaction data.
        """
        json_schema_extra = {
            "example": {
                "amount": 100.50,
                "location": "New York",
                "user_id": "user123",
                "time": "2024-09-25T12:34:56"
            }
        }
