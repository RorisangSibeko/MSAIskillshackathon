"""
Azure configuration for SafeWayAI application.
This module contains the configuration for Azure services used by the application.
Sensitive credentials are stored in a secure vault.
"""

import os
import json
import logging
from pathlib import Path
from dotenv import load_dotenv
from app.utils.vault import vault

logger = logging.getLogger(__name__)

# Load environment variables
env_path = Path(__file__).parent.parent / "assets" / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

# Initialize vault with environment variable password if available
vault_password = os.environ.get('SAFEWAYAI_VAULT_PASSWORD')
if vault_password:
    vault.unlock(vault_password)

# Default configuration (used if vault is not available)
DEFAULT_CONFIG = {
    # Azure subscription details (placeholders)
    "SUBSCRIPTION_KEY": "YOUR_SUBSCRIPTION_KEY",
    "REGION": "southafrica",

    # Azure Maps configuration
    "MAPS_CONFIG": {
        "subscription_key": "YOUR_MAPS_KEY",
        "base_url": "https://atlas.microsoft.com/"
    },

    # Azure AI Services configuration
    "AI_SERVICES_CONFIG": {
        "speech_key": "YOUR_SPEECH_KEY",
        "speech_region": "southafrica",
        "vision_key": "YOUR_VISION_KEY",
        "vision_endpoint": "https://safewayaiservices.cognitiveservices.azure.com/",
        "api_key": "YOUR_API_KEY",
        "endpoint": "https://safewayai-openai.openai.azure.com/",
        "deployment_id": "safewayai-gpt4",
        "api_version": "2023-05-15"
    },

    # Azure Cosmos DB configuration
    "COSMOS_DB_CONFIG": {
        "endpoint": "https://safewayai-db.documents.azure.com:443/",
        "key": "YOUR_COSMOS_DB_KEY",
        "database_id": "safewayai",
        "container_id": "incidents"
    },

    # Azure IoT Hub configuration
    "IOT_HUB_CONFIG": {
        "connection_string": "YOUR_IOT_HUB_CONNECTION_STRING",
        "device_id": "safewayai_mobile"
    },

    # Azure Functions configuration
    "FUNCTIONS_CONFIG": {
        "base_url": "safewayai-functions.azurewebsites.net",
        "api_key": "YOUR_FUNCTIONS_API_KEY",
        "functions": {
            "AnalyzeRouteSafety": {
                "method": "POST",
                "timeout": 30
            },
            "ProcessSafetyReport": {
                "method": "POST",
                "timeout": 20
            },
            "GenerateSafetyAlert": {
                "method": "POST",
                "timeout": 15
            },
            "GetCrimeData": {
                "method": "GET",
                "timeout": 30
            },
            "OptimizeRoute": {
                "method": "POST",
                "timeout": 45
            }
        }
    }
}

def get_config(key, default=None):
    """
    Get a configuration value from the vault or environment variables.

    Args:
        key (str): Configuration key
        default (any, optional): Default value if key not found

    Returns:
        any: Configuration value
    """
    # Try to get from vault first
    value = vault.get(key)

    # If not in vault, try environment variables
    if value is None:
        env_key = f"AZURE_{key}"
        value = os.environ.get(env_key)

    # If still not found, use default config
    if value is None and key in DEFAULT_CONFIG:
        value = DEFAULT_CONFIG[key]

    # Return value or default
    return value if value is not None else default

def set_config(key, value):
    """
    Set a configuration value in the vault.

    Args:
        key (str): Configuration key
        value (any): Configuration value

    Returns:
        bool: True if value was set successfully
    """
    return vault.set(key, value)

# Export configuration values
SUBSCRIPTION_KEY = get_config("SUBSCRIPTION_KEY")
REGION = get_config("REGION")
MAPS_CONFIG = get_config("MAPS_CONFIG")
AI_SERVICES_CONFIG = get_config("AI_SERVICES_CONFIG")
COSMOS_DB_CONFIG = get_config("COSMOS_DB_CONFIG")
IOT_HUB_CONFIG = get_config("IOT_HUB_CONFIG")
FUNCTIONS_CONFIG = get_config("FUNCTIONS_CONFIG")

# Initialize vault with real values if needed (first-time setup)
def initialize_vault_with_real_values():
    """
    Initialize the vault with real values.
    This should only be called during setup or when credentials change.
    """
    # Real configuration values (replace with your actual values)
    real_config = {
        "SUBSCRIPTION_KEY": "YOUR_SUBSCRIPTION_KEY",
        "REGION": "southafrica",
        "MAPS_CONFIG": {
            "subscription_key": "YOUR_MAPS_KEY",
            "base_url": "https://atlas.microsoft.com/"
        },
        "AI_SERVICES_CONFIG": {
            "speech_key": "YOUR_SPEECH_KEY",
            "speech_region": "southafrica",
            "vision_key": "YOUR_VISION_KEY",
            "vision_endpoint": "https://safewayaiservices.cognitiveservices.azure.com/",
            "api_key": "YOUR_API_KEY",
            "endpoint": "https://safewayai-openai.openai.azure.com/",
            "deployment_id": "safewayai-gpt4",
            "api_version": "2023-05-15"
        },
        "COSMOS_DB_CONFIG": {
            "endpoint": "https://safewayai-db.documents.azure.com:443/",
            "key": "YOUR_COSMOS_DB_KEY",
            "database_id": "safewayai",
            "container_id": "incidents"
        },
        "IOT_HUB_CONFIG": {
            "connection_string": "YOUR_IOT_HUB_CONNECTION_STRING",
            "device_id": "safewayai_mobile"
        },
        "FUNCTIONS_CONFIG": {
            "base_url": "safewayai-functions.azurewebsites.net",
            "api_key": "YOUR_FUNCTIONS_API_KEY",
            "functions": {
                "AnalyzeRouteSafety": {
                    "method": "POST",
                    "timeout": 30
                },
                "ProcessSafetyReport": {
                    "method": "POST",
                    "timeout": 20
                },
                "GenerateSafetyAlert": {
                    "method": "POST",
                    "timeout": 15
                },
                "GetCrimeData": {
                    "method": "GET",
                    "timeout": 30
                },
                "OptimizeRoute": {
                    "method": "POST",
                    "timeout": 45
                }
            }
        }
    }

    # Import configuration to vault
    if vault.unlock():
        vault.import_config(real_config)
        logger.info("Vault initialized with real values")
        return True
    else:
        logger.error("Failed to initialize vault with real values")
        return False

# This function should be called manually during setup
# initialize_vault_with_real_values()