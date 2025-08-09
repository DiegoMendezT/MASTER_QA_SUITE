"""
Logging utility for MASTER QA SUITE v2.0
"""
import logging
import os
from datetime import datetime


def setup_logger(name=__name__, level=logging.INFO):
    """Setup logger with file and console handlers"""
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    logs_dir = os.path.join(os.path.dirname(__file__), '..', 'reports')
    os.makedirs(logs_dir, exist_ok=True)
    
    log_filename = f"test_execution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    log_filepath = os.path.join(logs_dir, log_filename)
    
    file_handler = logging.FileHandler(log_filepath)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger
