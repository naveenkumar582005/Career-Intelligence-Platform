import os
import logging
from datetime import datetime

# Define central log directory and log file path inside backend/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "system_errors.log")

# Custom log format with timestamp, level, filename, line number, and function name
LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d - %(funcName)s()] %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Configure root logger
logger = logging.getLogger("CareerIntelligenceCentralLogger")
logger.setLevel(logging.INFO)

# Prevent duplicate handlers if module is re-imported
if not logger.handlers:
    # File Handler (Appends all errors to system_errors.log)
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Console Handler (Prints logs to terminal console)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)


def log_frontend_error(client_file, function_name, line_no, error_msg, url=""):
    """Special handler to log errors originating from the Frontend JavaScript client."""
    formatted_msg = (
        f"[FRONTEND_CLIENT] File: {client_file} | Line: {line_no} | Function: {function_name}() "
        f"| URL: {url} | Message: {error_msg}"
    )
    logger.error(formatted_msg)
