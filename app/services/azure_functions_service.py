"""
Azure Functions service for SafeWayAI application.
This module provides functionality to interact with Azure Functions.
"""

import logging
import json
import requests
from app.config.azure_config import FUNCTIONS_CONFIG

logger = logging.getLogger(__name__)

class AzureFunctionsService:
    """Service for interacting with Azure Functions."""
    
    def __init__(self):
        """Initialize the Azure Functions service."""
        self.base_url = f"https://{FUNCTIONS_CONFIG['base_url']}"
        self.api_key = FUNCTIONS_CONFIG["api_key"]
        logger.info("Azure Functions service initialized")
    
    def call_function(self, function_name, data=None, method="POST"):
        """
        Call an Azure Function.
        
        Args:
            function_name (str): The name of the function
            data (dict, optional): The data to send
            method (str, optional): The HTTP method
            
        Returns:
            dict: The function response
        """
        try:
            # Build the URL
            url = f"{self.base_url}/api/{function_name}"
            
            # Set up headers
            headers = {
                "Content-Type": "application/json",
                "x-functions-key": self.api_key
            }
            
            # Make the request
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, params=data)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=data)
            elif method.upper() == "PUT":
                response = requests.put(url, headers=headers, json=data)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=headers, json=data)
            else:
                logger.error(f"Unsupported HTTP method: {method}")
                return {"error": f"Unsupported HTTP method: {method}"}
            
            # Check response
            response.raise_for_status()
            
            # Parse the response
            if response.content:
                return response.json()
            else:
                return {"status": "success"}
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Azure Function {function_name}: {e}")
            return {"error": str(e)}
    
    def analyze_safety(self, location):
        """
        Analyze the safety of a location.
        
        Args:
            location (dict): The location data (latitude, longitude)
            
        Returns:
            dict: Safety analysis results
        """
        try:
            return self.call_function(
                "AnalyzeSafety",
                data=location,
                method="POST"
            )
            
        except Exception as e:
            logger.error(f"Error analyzing safety: {e}")
            return {"error": str(e)}
    
    def report_incident(self, incident_data):
        """
        Report an incident.
        
        Args:
            incident_data (dict): The incident data
            
        Returns:
            dict: The response from the function
        """
        try:
            return self.call_function(
                "ReportIncident",
                data=incident_data,
                method="POST"
            )
            
        except Exception as e:
            logger.error(f"Error reporting incident: {e}")
            return {"error": str(e)}
    
    def get_safe_route(self, start_point, end_point):
        """
        Get a safe route between two points.
        
        Args:
            start_point (dict): The starting point (latitude, longitude)
            end_point (dict): The ending point (latitude, longitude)
            
        Returns:
            dict: Safe route information
        """
        try:
            return self.call_function(
                "GetSafeRoute",
                data={
                    "startPoint": start_point,
                    "endPoint": end_point
                },
                method="POST"
            )
            
        except Exception as e:
            logger.error(f"Error getting safe route: {e}")
            return {"error": str(e)}
    
    def get_nearby_incidents(self, location, radius_km=1.0):
        """
        Get incidents near a location.
        
        Args:
            location (dict): The location (latitude, longitude)
            radius_km (float, optional): The radius in kilometers
            
        Returns:
            dict: Nearby incidents
        """
        try:
            return self.call_function(
                "GetNearbyIncidents",
                data={
                    "latitude": location["latitude"],
                    "longitude": location["longitude"],
                    "radiusKm": radius_km
                },
                method="GET"
            )
            
        except Exception as e:
            logger.error(f"Error getting nearby incidents: {e}")
            return {"error": str(e)}
    
    def process_emergency_alert(self, alert_data):
        """
        Process an emergency alert.
        
        Args:
            alert_data (dict): The alert data
            
        Returns:
            dict: The response from the function
        """
        try:
            return self.call_function(
                "ProcessEmergencyAlert",
                data=alert_data,
                method="POST"
            )
            
        except Exception as e:
            logger.error(f"Error processing emergency alert: {e}")
            return {"error": str(e)}
