import flet as ft
import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add the current directory to the path to ensure imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the app class
from app.main import SafeWayAIApp

def main():
    """
    Main entry point for the SafeWayAI application.
    """
    print("Starting SafeWayAI application...")
    logger.info("Starting SafeWayAI application...")

    # Launch the Flet app
    print("Launching Flet app...")
    ft.app(
        target=SafeWayAIApp,
        assets_dir="app/assets",
        port=8080,
        route_url_strategy="path",
    )
    print("Flet app closed.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error in main: {e}")
        logger.exception("Error in main")
