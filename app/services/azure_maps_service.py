"""
Azure Maps service for SafeWayAI application.
This module provides functionality to interact with Azure Maps for route finding.
"""

import requests
import json
import logging
from app.config.azure_config import MAPS_CONFIG

logger = logging.getLogger(__name__)

class AzureMapsService:
    """Service for interacting with Azure Maps."""
    
    def __init__(self):
        """Initialize the Azure Maps service."""
        self.subscription_key = MAPS_CONFIG["subscription_key"]
        self.base_url = MAPS_CONFIG["base_url"]
        logger.info("Azure Maps service initialized")
    
    def get_route(self, start_point, end_point, route_type="safe"):
        """
        Get a route between two points.
        
        Args:
            start_point (tuple): The starting point (latitude, longitude)
            end_point (tuple): The ending point (latitude, longitude)
            route_type (str): The type of route to find (safe, fastest, shortest)
            
        Returns:
            dict: The route information
        """
        try:
            # Format coordinates for Azure Maps API
            start_coords = f"{start_point[1]},{start_point[0]}"  # lon,lat format
            end_coords = f"{end_point[1]},{end_point[0]}"  # lon,lat format
            
            # Build the request URL
            url = f"{self.base_url}route/directions/json"
            
            # Set up parameters
            params = {
                "subscription-key": self.subscription_key,
                "api-version": "1.0",
                "query": f"{start_coords}:{end_coords}",
                "routeType": "shortest",  # Base route type
                "traffic": "true",
                "travelMode": "pedestrian",  # Default to pedestrian for safety
                "computeBestOrder": "false",
                "instructionsType": "text",
                "language": "en-US"
            }
            
            # Make the request
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            # Parse the response
            route_data = response.json()
            
            # If safe route is requested, we need to process the route data
            # to consider safety factors (this would be a custom implementation)
            if route_type == "safe":
                return self._enhance_route_with_safety_data(route_data)
            
            return route_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting route from Azure Maps: {e}")
            return {"error": str(e)}
    
    def _enhance_route_with_safety_data(self, route_data):
        """
        Enhance the route data with safety information.
        
        This would typically involve:
        1. Analyzing the route segments
        2. Checking each segment against crime data
        3. Identifying high-risk areas
        4. Suggesting safer alternatives where needed
        
        Args:
            route_data (dict): The original route data from Azure Maps
            
        Returns:
            dict: Enhanced route data with safety information
        """
        try:
            # This is a placeholder for the actual implementation
            # In a real implementation, we would:
            # 1. Extract route segments
            # 2. Query our safety database for each segment
            # 3. Assign safety scores
            # 4. Potentially reroute around high-risk areas
            
            # For now, we'll just add a mock safety score to the route
            enhanced_data = route_data.copy()
            
            if "routes" in enhanced_data and enhanced_data["routes"]:
                for i, route in enumerate(enhanced_data["routes"]):
                    # Add a safety score (1-10, where 10 is safest)
                    route["safetyScore"] = 7
                    
                    # Add safety notes
                    route["safetyNotes"] = [
                        "This route avoids known high-crime areas",
                        "Well-lit streets throughout most of the journey",
                        "Moderate pedestrian traffic expected"
                    ]
                    
                    # Flag any segments of concern
                    if "legs" in route:
                        for j, leg in enumerate(route["legs"]):
                            leg["safetyConcerns"] = []
                            
                            # This would be based on real data in production
                            if j % 3 == 0:  # Just for demonstration
                                leg["safetyConcerns"].append({
                                    "type": "low_lighting",
                                    "description": "Limited street lighting in this area",
                                    "severity": "medium"
                                })
            
            return enhanced_data
            
        except Exception as e:
            logger.error(f"Error enhancing route with safety data: {e}")
            return route_data  # Return original data if enhancement fails
    
    def search_address(self, query, limit=5):
        """
        Search for an address or point of interest.
        
        Args:
            query (str): The search query
            limit (int): Maximum number of results to return
            
        Returns:
            dict: Search results
        """
        try:
            # Build the request URL
            url = f"{self.base_url}search/address/json"
            
            # Set up parameters
            params = {
                "subscription-key": self.subscription_key,
                "api-version": "1.0",
                "query": query,
                "limit": limit,
                "typeahead": "true",
                "language": "en-US"
            }
            
            # Make the request
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            # Return the search results
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error searching address in Azure Maps: {e}")
            return {"error": str(e)}
