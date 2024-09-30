import asyncio
from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect, APIRouter
from fastapi.responses import JSONResponse
from app.routes.transaction import transaction_router  # Import the transaction router for transaction-related API routes
from fastapi.middleware.cors import CORSMiddleware  # Middleware to handle Cross-Origin Resource Sharing (CORS)
from app.utils.websocket_manager import websocket_endpoint  # Import WebSocket handler to manage WebSocket connections
from app.consumers.kafka_consumer import consume_transactions  # Kafka consumer to process transaction messages
from app.utils.logging_config import setup_logging  # Custom logging configuration
import uvicorn  # ASGI server to run FastAPI applications
from app.utils.config import CORS_ORIGIN  # Load CORS origin from configuration (assumes config.py exists in utils)

# Set up application logging
setup_logging()  # Initialize logging at the start of the application

# Create the FastAPI application instance
app = FastAPI(
    title="Real-Time Fraud Detection API",
    description="This API allows you to submit transactions and check for fraud in real-time.",
    version="1.0.0",
    docs_url="/docs"  # Swagger documentation is enabled at /docs for easy API exploration
)

# Register the transaction routes
app.include_router(transaction_router)

# List of allowed origins for CORS (loaded from environment configuration)
origins = [CORS_ORIGIN]

# Add CORS middleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for CORS (can be restricted for production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all HTTP headers
)

@app.get("/api/")
def read_root():
    """
    Root API endpoint that provides a basic message.
    Returns a simple message indicating the API is running.
    """
    return {"message": "Real-Time Fraud Detection API"}

@app.get("/api/health")
async def health_check():
    """
    Health check endpoint to verify that the application is running properly.
    Returns a status message indicating the application's health.
    """
    return {"status": "healthy"}

# WebSocket route for real-time transaction updates
@app.websocket("/api/ws")
async def websocket_route(websocket: WebSocket):
    """
    WebSocket route to handle real-time transaction updates.
    It delegates the actual WebSocket handling to the `websocket_endpoint` function.
    
    Args:
        websocket (WebSocket): The WebSocket connection object from FastAPI.
    """
    await websocket_endpoint(websocket)

# FastAPI event that runs on application startup
@app.on_event("startup")
async def startup_event():
    """
    Event handler that is triggered when the FastAPI application starts.
    This function creates a background task to consume transactions from the Kafka broker.
    """
    asyncio.create_task(consume_transactions())  # Start the Kafka consumer in the background

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for unhandled exceptions in the application.
    It returns a 500 response with a generic error message.

    Args:
        request (Request): The incoming HTTP request that caused the error.
        exc (Exception): The exception that was raised.
    
    Returns:
        JSONResponse: A response containing the error message and 500 status code.
    """
    return JSONResponse(
        status_code=500,
        content={"message": f"An unexpected error occurred: {exc}"}
    )

# Main entry point when running the script directly
if __name__ == "__main__":
    """
    Run the FastAPI application using Uvicorn.
    This allows for the application to be started from the command line.
    """
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)