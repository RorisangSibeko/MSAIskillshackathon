"""
Safe route service for SafeWayAI application.
This module provides functionality to find safe routes using Azure Maps and safety data.
"""

import logging
import json
import time
from app.services.service_manager import ServiceManager

logger = logging.getLogger(__name__)

class SafeRouteService:
    """Service for finding safe routes."""
    
    _instance = None
    
    def __new__(cls):
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super(SafeRouteService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the safe route service."""
        if self._initialized:
            return
            
        logger.info("Initializing safe route service")
        
        # Get service manager
        self.service_manager = ServiceManager()
        
        self._initialized = True
    
    def find_safe_route(self, start_point, end_point, safety_priority=0.7):
        """
        Find a safe route between two points.
        
        Args:
            start_point (tuple): The starting point (latitude, longitude)
            end_point (tuple): The ending point (latitude, longitude)
            safety_priority (float, optional): Priority for safety vs. speed (0-1)
            
        Returns:
            dict: Safe route information
        """
        try:
            logger.info(f"Finding safe route from {start_point} to {end_point}")
            
            # First, try to use the Azure Functions service for a comprehensive solution
            if hasattr(self.service_manager, 'functions_service') and self.service_manager.functions_service:
                try:
                    result = self.service_manager.functions_service.get_safe_route(
                        {"latitude": start_point[0], "longitude": start_point[1]},
                        {"latitude": end_point[0], "longitude": end_point[1]}
                    )
                    
                    if "error" not in result:
                        logger.info("Safe route found using Azure Functions")
                        return result
                    else:
                        logger.warning(f"Error from Azure Functions: {result.get('error')}")
                except Exception as e:
                    logger.warning(f"Error using Azure Functions for safe route: {e}")
            
            # Fallback to direct Azure Maps integration
            logger.info("Falling back to direct Azure Maps integration")
            
            # Get a basic route from Azure Maps
            route_data = self.service_manager.maps_service.get_route(
                start_point, end_point, route_type="safe"
            )
            
            # Enhance the route with safety information
            enhanced_route = self._enhance_route_with_safety_data(route_data, safety_priority)
            
            return enhanced_route
            
        except Exception as e:
            logger.error(f"Error finding safe route: {e}")
            return {"error": str(e)}
    
    def _enhance_route_with_safety_data(self, route_data, safety_priority):
        """
        Enhance the route data with safety information.
        
        Args:
            route_data (dict): The original route data from Azure Maps
            safety_priority (float): Priority for safety vs. speed (0-1)
            
        Returns:
            dict: Enhanced route data with safety information
        """
        try:
            # This would typically involve:
            # 1. Breaking the route into segments
            # 2. Checking each segment against our safety database
            # 3. Potentially rerouting around high-risk areas
            # 4. Adding safety information to the route
            
            # For now, we'll use the implementation in the maps service
            return route_data
            
        except Exception as e:
            logger.error(f"Error enhancing route with safety data: {e}")
            return route_data
    
    def get_safety_score_for_location(self, latitude, longitude):
        """
        Get a safety score for a specific location.
        
        Args:
            latitude (float): The latitude
            longitude (float): The longitude
            
        Returns:
            dict: Safety score information
        """
        try:
            # First, try to use the Azure Functions service
            if hasattr(self.service_manager, 'functions_service') and self.service_manager.functions_service:
                try:
                    result = self.service_manager.functions_service.analyze_safety({
                        "latitude": latitude,
                        "longitude": longitude
                    })
                    
                    if "error" not in result:
                        logger.info("Safety score retrieved using Azure Functions")
                        return result
                    else:
                        logger.warning(f"Error from Azure Functions: {result.get('error')}")
                except Exception as e:
                    logger.warning(f"Error using Azure Functions for safety score: {e}")
            
            # Fallback to a local implementation
            logger.info("Falling back to local safety score implementation")
            
            # Get nearby incidents from Cosmos DB
            if hasattr(self.service_manager, 'cosmos_service') and self.service_manager.cosmos_service:
                try:
                    incidents = self.service_manager.cosmos_service.get_incidents_by_location(
                        latitude, longitude, radius_km=1.0
                    )
                    
                    # Calculate safety score based on incidents
                    if isinstance(incidents, list):
                        # More incidents = lower safety score
                        incident_count = len(incidents)
                        base_score = max(10 - incident_count, 1)  # 1-10 scale
                        
                        # Adjust based on severity of incidents
                        severity_sum = sum(
                            incident.get("severity", 1) 
                            for incident in incidents 
                            if isinstance(incident, dict)
                        )
                        
                        if incident_count > 0:
                            avg_severity = severity_sum / incident_count
                            # Adjust score based on severity (higher severity = lower score)
                            adjusted_score = base_score - (avg_severity - 1)
                        else:
                            adjusted_score = base_score
                        
                        # Ensure score is in range 1-10
                        final_score = max(1, min(10, adjusted_score))
                        
                        return {
                            "safety_score": final_score,
                            "incident_count": incident_count,
                            "safety_level": self._score_to_level(final_score),
                            "timestamp": time.time()
                        }
                    else:
                        logger.warning(f"Unexpected incidents result: {incidents}")
                except Exception as e:
                    logger.warning(f"Error getting incidents from Cosmos DB: {e}")
            
            # If all else fails, return a default score
            return {
                "safety_score": 7,  # Default moderate-high safety score
                "incident_count": 0,
                "safety_level": "MODERATE",
                "timestamp": time.time(),
                "note": "Default safety score (no incident data available)"
            }
            
        except Exception as e:
            logger.error(f"Error getting safety score for location: {e}")
            return {"error": str(e)}
    
    def _score_to_level(self, score):
        """
        Convert a numeric safety score to a level.
        
        Args:
            score (float): The safety score (1-10)
            
        Returns:
            str: The safety level
        """
        if score >= 8:
            return "HIGH"
        elif score >= 5:
            return "MODERATE"
        else:
            return "LOW"
