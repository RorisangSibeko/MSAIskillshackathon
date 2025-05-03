import flet as ft
import os
import sys
import logging
from ui.app import SafeWayAIApp

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """
    Main entry point for the SafeWayAI application.

    This function initializes the Flet app with the SafeWayAIApp class.
    For mobile deployment, it uses the FLET_VIEW environment variable
    to determine the view type.
    """
    print("Starting SafeWayAI application...")
    logger.info("Starting SafeWayAI application...")

    # Determine view type based on environment or platform
    view = os.environ.get("FLET_VIEW", ft.WEB_BROWSER)
    print(f"Using view type: {view}")

    # Launch the Flet app
    print("Launching Flet app...")
    ft.app(
        target=SafeWayAIApp,
        view=view,
        assets_dir="assets",
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
        
