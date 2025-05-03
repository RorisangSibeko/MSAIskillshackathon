import logging
import requests
import json
from app.config.azure_config import AZURE_MAPS_KEY

logger = logging.getLogger(__name__)

class MapsService:
    """Service for interacting with Azure Maps."""
    
    def __init__(self):
        self.api_key = AZURE_MAPS_KEY
        self.base_url = "https://atlas.microsoft.com/search/address/json"
        self.route_url = "https://atlas.microsoft.com/route/directions/json"
        
    def search_address(self, query, limit=5):
        """
        Search for an address using Azure Maps.
        
        Args:
            query (str): The address to search for
            limit (int): Maximum number of results to return
            
        Returns:
            dict: The search results
        """
        try:
            # If no API key is available, return simulated data
            if not self.api_key or self.api_key == "YOUR_AZURE_MAPS_KEY":
                logger.warning("No Azure Maps API key available, returning simulated data")
                return self._get_simulated_search_results(query)
                
            params = {
                "api-version": "1.0",
                "subscription-key": self.api_key,
                "query": query,
                "limit": limit,
                "countrySet": "ZA",  # South Africa
                "language": "en-US"
            }
            
            response = requests.get(self.base_url, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Error searching for address: {response.status_code} - {response.text}")
                return {"error": f"API error: {response.status_code}"}
                
        except Exception as ex:
            logger.error(f"Error searching for address: {ex}")
            return {"error": str(ex)}
            
    def get_route(self, start_coords, end_coords, travel_mode="pedestrian"):
        """
        Get a route between two points using Azure Maps.
        
        Args:
            start_coords (tuple): The starting coordinates (lat, lon)
            end_coords (tuple): The ending coordinates (lat, lon)
            travel_mode (str): The travel mode (pedestrian, car, etc.)
            
        Returns:
            dict: The route information
        """
        try:
            # If no API key is available, return simulated data
            if not self.api_key or self.api_key == "YOUR_AZURE_MAPS_KEY":
                logger.warning("No Azure Maps API key available, returning simulated data")
                return self._get_simulated_route(start_coords, end_coords, travel_mode)
                
            params = {
                "api-version": "1.0",
                "subscription-key": self.api_key,
                "query": f"{start_coords[0]},{start_coords[1]}:{end_coords[0]},{end_coords[1]}",
                "travelMode": travel_mode,
                "computeBestOrder": "false",
                "routeType": "fastest",
                "traffic": "true",
                "language": "en-US"
            }
            
            response = requests.get(self.route_url, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Error getting route: {response.status_code} - {response.text}")
                return {"error": f"API error: {response.status_code}"}
                
        except Exception as ex:
            logger.error(f"Error getting route: {ex}")
            return {"error": str(ex)}
            
    def _get_simulated_search_results(self, query):
        """
        Get simulated search results for testing.
        
        Args:
            query (str): The address to search for
            
        Returns:
            dict: Simulated search results
        """
        # Create a simulated response based on the query
        if "johannesburg" in query.lower():
            lat, lon = -26.2041, 28.0473
        elif "sandton" in query.lower():
            lat, lon = -26.1052, 28.0560
        elif "pretoria" in query.lower():
            lat, lon = -25.7479, 28.2293
        elif "cape town" in query.lower():
            lat, lon = -33.9249, 18.4241
        elif "durban" in query.lower():
            lat, lon = -29.8587, 31.0218
        else:
            # Default to Johannesburg
            lat, lon = -26.2041, 28.0473
            
        return {
            "results": [
                {
                    "type": "Point Address",
                    "id": "ZA/PAD/p0/123456",
                    "score": 4.9,
                    "address": {
                        "streetName": "Main Road",
                        "municipality": "City of Johannesburg",
                        "countrySubdivision": "Gauteng",
                        "countryCode": "ZA",
                        "country": "South Africa",
                        "countryCodeISO3": "ZAF",
                        "freeformAddress": query,
                        "localName": "Johannesburg"
                    },
                    "position": {
                        "lat": lat,
                        "lon": lon
                    }
                }
            ]
        }
        
    def _get_simulated_route(self, start_coords, end_coords, travel_mode):
        """
        Get simulated route data for testing.
        
        Args:
            start_coords (tuple): The starting coordinates (lat, lon)
            end_coords (tuple): The ending coordinates (lat, lon)
            travel_mode (str): The travel mode (pedestrian, car, etc.)
            
        Returns:
            dict: Simulated route data
        """
        # Calculate a simple straight-line distance
        from math import sqrt, pow
        
        # Convert to kilometers (very rough approximation)
        distance = sqrt(pow(start_coords[0] - end_coords[0], 2) + pow(start_coords[1] - end_coords[1], 2)) * 111
        
        # Calculate duration based on travel mode and distance
        if travel_mode == "pedestrian":
            # Walking speed ~5 km/h
            duration_minutes = (distance / 5) * 60
        else:
            # Driving speed ~40 km/h in urban areas
            duration_minutes = (distance / 40) * 60
            
        return {
            "routes": [
                {
                    "summary": {
                        "lengthInMeters": int(distance * 1000),
                        "travelTimeInSeconds": int(duration_minutes * 60),
                        "trafficDelayInSeconds": 0,
                        "departureTime": "2023-05-20T12:00:00Z",
                        "arrivalTime": "2023-05-20T12:30:00Z"
                    },
                    "legs": [
                        {
                            "summary": {
                                "lengthInMeters": int(distance * 1000),
                                "travelTimeInSeconds": int(duration_minutes * 60),
                                "trafficDelayInSeconds": 0,
                                "departureTime": "2023-05-20T12:00:00Z",
                                "arrivalTime": "2023-05-20T12:30:00Z"
                            },
                            "points": [
                                {"latitude": start_coords[0], "longitude": start_coords[1]},
                                {"latitude": end_coords[0], "longitude": end_coords[1]}
                            ]
                        }
                    ]
                }
            ]
        }
