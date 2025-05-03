"""
Incident service for SafeWayAI application.
This module provides functionality to report and manage incidents.
"""

import logging
import json
import time
import uuid
from datetime import datetime
from app.services.service_manager import ServiceManager

logger = logging.getLogger(__name__)

class IncidentService:
    """Service for reporting and managing incidents."""
    
    _instance = None
    
    def __new__(cls):
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super(IncidentService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the incident service."""
        if self._initialized:
            return
            
        logger.info("Initializing incident service")
        
        # Get service manager
        self.service_manager = ServiceManager()
        
        self._initialized = True
    
    def report_incident(self, incident_data):
        """
        Report a new incident.
        
        Args:
            incident_data (dict): The incident data
            
        Returns:
            dict: The created incident
        """
        try:
            logger.info(f"Reporting incident: {incident_data}")
            
            # First, try to use the Azure Functions service
            if hasattr(self.service_manager, 'functions_service') and self.service_manager.functions_service:
                try:
                    result = self.service_manager.functions_service.report_incident(incident_data)
                    
                    if "error" not in result:
                        logger.info("Incident reported using Azure Functions")
                        return result
                    else:
                        logger.warning(f"Error from Azure Functions: {result.get('error')}")
                except Exception as e:
                    logger.warning(f"Error using Azure Functions for incident reporting: {e}")
            
            # Fallback to direct Cosmos DB integration
            logger.info("Falling back to direct Cosmos DB integration")
            
            # Ensure required fields
            if "type" not in incident_data:
                incident_data["type"] = "incident"
            
            if "timestamp" not in incident_data:
                incident_data["timestamp"] = time.time()
            
            if "status" not in incident_data:
                incident_data["status"] = "reported"
            
            # Create the incident in Cosmos DB
            if hasattr(self.service_manager, 'cosmos_service') and self.service_manager.cosmos_service:
                result = self.service_manager.cosmos_service.create_incident(incident_data)
                
                # Also send to IoT Hub if connected
                if hasattr(self.service_manager, 'iot_service') and self.service_manager.iot_service:
                    self.service_manager.iot_service.send_telemetry({
                        "type": "incident_reported",
                        "incident_id": result.get("id"),
                        "incident_type": incident_data.get("incident_type"),
                        "timestamp": time.time()
                    })
                
                return result
            else:
                logger.error("Cosmos DB service not available")
                return {"error": "Incident reporting service not available"}
            
        except Exception as e:
            logger.error(f"Error reporting incident: {e}")
            return {"error": str(e)}
    
    def get_incident(self, incident_id):
        """
        Get an incident by ID.
        
        Args:
            incident_id (str): The incident ID
            
        Returns:
            dict: The incident
        """
        try:
            logger.info(f"Getting incident: {incident_id}")
            
            # Use Cosmos DB to get the incident
            if hasattr(self.service_manager, 'cosmos_service') and self.service_manager.cosmos_service:
                return self.service_manager.cosmos_service.get_incident(incident_id)
            else:
                logger.error("Cosmos DB service not available")
                return {"error": "Incident service not available"}
            
        except Exception as e:
            logger.error(f"Error getting incident: {e}")
            return {"error": str(e)}
    
    def update_incident(self, incident_id, update_data):
        """
        Update an incident.
        
        Args:
            incident_id (str): The incident ID
            update_data (dict): The data to update
            
        Returns:
            dict: The updated incident
        """
        try:
            logger.info(f"Updating incident {incident_id}: {update_data}")
            
            # Use Cosmos DB to update the incident
            if hasattr(self.service_manager, 'cosmos_service') and self.service_manager.cosmos_service:
                result = self.service_manager.cosmos_service.update_incident(incident_id, update_data)
                
                # Also send to IoT Hub if connected
                if hasattr(self.service_manager, 'iot_service') and self.service_manager.iot_service:
                    self.service_manager.iot_service.send_telemetry({
                        "type": "incident_updated",
                        "incident_id": incident_id,
                        "update_type": update_data.get("status", "updated"),
                        "timestamp": time.time()
                    })
                
                return result
            else:
                logger.error("Cosmos DB service not available")
                return {"error": "Incident service not available"}
            
        except Exception as e:
            logger.error(f"Error updating incident: {e}")
            return {"error": str(e)}
    
    def get_nearby_incidents(self, latitude, longitude, radius_km=1.0, max_incidents=10):
        """
        Get incidents near a location.
        
        Args:
            latitude (float): The latitude
            longitude (float): The longitude
            radius_km (float, optional): The radius in kilometers
            max_incidents (int, optional): Maximum number of incidents to return
            
        Returns:
            list: List of incidents
        """
        try:
            logger.info(f"Getting incidents near ({latitude}, {longitude}) within {radius_km} km")
            
            # First, try to use the Azure Functions service
            if hasattr(self.service_manager, 'functions_service') and self.service_manager.functions_service:
                try:
                    result = self.service_manager.functions_service.get_nearby_incidents(
                        {"latitude": latitude, "longitude": longitude},
                        radius_km
                    )
                    
                    if "error" not in result:
                        logger.info("Nearby incidents retrieved using Azure Functions")
                        return result
                    else:
                        logger.warning(f"Error from Azure Functions: {result.get('error')}")
                except Exception as e:
                    logger.warning(f"Error using Azure Functions for nearby incidents: {e}")
            
            # Fallback to direct Cosmos DB integration
            logger.info("Falling back to direct Cosmos DB integration")
            
            # Use Cosmos DB to get nearby incidents
            if hasattr(self.service_manager, 'cosmos_service') and self.service_manager.cosmos_service:
                return self.service_manager.cosmos_service.get_incidents_by_location(
                    latitude, longitude, radius_km, max_incidents
                )
            else:
                logger.error("Cosmos DB service not available")
                return {"error": "Incident service not available"}
            
        except Exception as e:
            logger.error(f"Error getting nearby incidents: {e}")
            return {"error": str(e)}
    
    def get_recent_incidents(self, max_incidents=10):
        """
        Get recent incidents.
        
        Args:
            max_incidents (int, optional): Maximum number of incidents to return
            
        Returns:
            list: List of incidents
        """
        try:
            logger.info(f"Getting recent incidents (max {max_incidents})")
            
            # Use Cosmos DB to query incidents
            if hasattr(self.service_manager, 'cosmos_service') and self.service_manager.cosmos_service:
                return self.service_manager.cosmos_service.query_incidents(
                    query_params=None,
                    max_items=max_incidents
                )
            else:
                logger.error("Cosmos DB service not available")
                return {"error": "Incident service not available"}
            
        except Exception as e:
            logger.error(f"Error getting recent incidents: {e}")
            return {"error": str(e)}
