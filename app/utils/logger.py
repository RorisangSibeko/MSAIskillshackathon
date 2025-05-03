import logging
import os
from pathlib import Path

def setup_logger():
    """Set up the application logger."""
    # Create logs directory if it doesn't exist
    logs_dir = Path("app/data/logs")
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(logs_dir / "safewayai.log"),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger("safewayai")
