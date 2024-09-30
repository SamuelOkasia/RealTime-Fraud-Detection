import logging

def setup_logging():
    """
    Configures logging for the application.

    This function sets up basic logging to output logs to the console with a specific format.
    You can change the logging level to adjust verbosity. By default, the logging level is set to INFO.
    For more detailed logs, such as for debugging, you can set it to DEBUG.

    Logging Format:
    - `%(asctime)s`: The timestamp when the log entry was created.
    - `%(name)s`: The name of the logger (usually the module or file).
    - `%(levelname)s`: The log level (INFO, DEBUG, ERROR, etc.).
    - `%(message)s`: The actual log message.

    Example Output:
    ```
    2024-09-28 12:00:00 - app.module - INFO - Transaction processed successfully.
    ```

    Logging is configured to:
    - Log messages to the console using a `StreamHandler`.
    - The default log level is set to `INFO`, but you can modify it for more verbosity.
    """
    
    logging.basicConfig(
        level=logging.INFO,  # Set this to logging.DEBUG for more detailed logs
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()  # Outputs to console (standard output)
        ]
    )
