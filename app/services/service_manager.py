"""
Service manager for SafeWayAI application.
This module provides a centralized manager for all Azure services.
"""

import logging
from app.services.azure_maps_service import AzureMapsService
from app.services.azure_ai_service import AzureAIService
from app.services.azure_cosmos_service import AzureCosmosService
from app.services.azure_iot_service import AzureIoTService
from app.services.azure_functions_service import AzureFunctionsService

logger = logging.getLogger(__name__)

class ServiceManager:
    """Manager for all Azure services."""
    
    _instance = None
    
    def __new__(cls):
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super(ServiceManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the service manager."""
        if self._initialized:
            return
            
        logger.info("Initializing service manager")
        
        # Initialize services
        self._maps_service = None
        self._ai_service = None
        self._cosmos_service = None
        self._iot_service = None
        self._functions_service = None
        
        self._initialized = True
    
    @property
    def maps_service(self):
        """Get the Azure Maps service."""
        if self._maps_service is None:
            logger.info("Initializing Azure Maps service")
            self._maps_service = AzureMapsService()
        return self._maps_service
    
    @property
    def ai_service(self):
        """Get the Azure AI service."""
        if self._ai_service is None:
            logger.info("Initializing Azure AI service")
            self._ai_service = AzureAIService()
        return self._ai_service
    
    @property
    def cosmos_service(self):
        """Get the Azure Cosmos DB service."""
        if self._cosmos_service is None:
            logger.info("Initializing Azure Cosmos DB service")
            self._cosmos_service = AzureCosmosService()
        return self._cosmos_service
    
    @property
    def iot_service(self):
        """Get the Azure IoT Hub service."""
        if self._iot_service is None:
            logger.info("Initializing Azure IoT Hub service")
            self._iot_service = AzureIoTService()
        return self._iot_service
    
    @property
    def functions_service(self):
        """Get the Azure Functions service."""
        if self._functions_service is None:
            logger.info("Initializing Azure Functions service")
            self._functions_service = AzureFunctionsService()
        return self._functions_service
    
    def close_all(self):
        """Close all services."""
        logger.info("Closing all services")
        
        if self._iot_service:
            self._iot_service.close()
            
        # Reset all services
        self._maps_service = None
        self._ai_service = None
        self._cosmos_service = None
        self._iot_service = None
        self._functions_service = None
