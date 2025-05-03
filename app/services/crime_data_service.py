"""
Crime Data Service for SafeWayAI application.
This module provides access to crime data from various sources.
"""

import logging
import requests
import json
import os
import time
from datetime import datetime, timedelta
import random
from app.config.azure_config import COSMOS_DB_CONFIG, AI_SERVICES_CONFIG

logger = logging.getLogger(__name__)

class CrimeDataService:
    """Service for accessing and analyzing crime data."""
    
    _instance = None
    
    def __new__(cls):
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super(CrimeDataService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the crime data service."""
        if self._initialized:
            return
            
        logger.info("Initializing crime data service")
        
        # Initialize configuration
        self.cosmos_config = COSMOS_DB_CONFIG
        self.ai_config = AI_SERVICES_CONFIG
        
        # Initialize cache
        self.crime_data_cache = {}
        self.cache_expiry = 3600  # Cache expiry in seconds (1 hour)
        self.last_cache_update = 0
        
        # Initialize crime data sources
        self.data_sources = {
            "police_api": {
                "enabled": False,
                "url": "https://data.police.uk/api/",
                "api_key": os.environ.get("POLICE_API_KEY", "")
            },
            "azure_cosmos": {
                "enabled": True,
                "connection_string": self.cosmos_config.get("connection_string", ""),
                "database": self.cosmos_config.get("database", "safewayai"),
                "container": "crime_data"
            },
            "local_data": {
                "enabled": True,
                "file_path": os.path.join("data", "crime_data.json")
            }
        }
        
        # Load initial data
        self._load_initial_data()
        
        self._initialized = True
    
    def _load_initial_data(self):
        """Load initial crime data from available sources."""
        try:
            # Try to load from Cosmos DB
            if self.data_sources["azure_cosmos"]["enabled"]:
                self._load_from_cosmos_db()
            
            # If no data loaded, try local file
            if not self.crime_data_cache and self.data_sources["local_data"]["enabled"]:
                self._load_from_local_file()
            
            # If still no data, generate synthetic data
            if not self.crime_data_cache:
                self._generate_synthetic_data()
            
            self.last_cache_update = time.time()
            
        except Exception as e:
            logger.error(f"Error loading initial crime data: {e}")
            # Fallback to synthetic data
            self._generate_synthetic_data()
    
    def _load_from_cosmos_db(self):
        """Load crime data from Azure Cosmos DB."""
        try:
            # In a real implementation, this would connect to Cosmos DB
            # For now, we'll simulate a response
            logger.info("Simulating loading crime data from Cosmos DB")
            
            # Simulate a delay
            time.sleep(0.2)
            
            # For now, we'll just generate synthetic data
            self._generate_synthetic_data()
            
        except Exception as e:
            logger.error(f"Error loading from Cosmos DB: {e}")
    
    def _load_from_local_file(self):
        """Load crime data from local file."""
        try:
            file_path = self.data_sources["local_data"]["file_path"]
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    self.crime_data_cache = json.load(f)
                logger.info(f"Loaded crime data from {file_path}")
            else:
                logger.warning(f"Local crime data file not found: {file_path}")
        except Exception as e:
            logger.error(f"Error loading from local file: {e}")
    
    def _generate_synthetic_data(self):
        """Generate synthetic crime data for testing."""
        logger.info("Generating synthetic crime data")
        
        # Define areas (using Johannesburg coordinates as example)
        areas = {
            "cbd": {
                "center": {"latitude": -26.2041, "longitude": 28.0473},
                "radius": 2.0,
                "crime_level": "high",
                "crime_types": ["theft", "robbery", "assault"]
            },
            "sandton": {
                "center": {"latitude": -26.1052, "longitude": 28.0560},
                "radius": 3.0,
                "crime_level": "low",
                "crime_types": ["theft"]
            },
            "soweto": {
                "center": {"latitude": -26.2227, "longitude": 27.8900},
                "radius": 5.0,
                "crime_level": "medium",
                "crime_types": ["theft", "assault"]
            },
            "rosebank": {
                "center": {"latitude": -26.1467, "longitude": 28.0437},
                "radius": 1.5,
                "crime_level": "low",
                "crime_types": ["theft"]
            },
            "randburg": {
                "center": {"latitude": -26.0941, "longitude": 28.0060},
                "radius": 2.5,
                "crime_level": "medium",
                "crime_types": ["theft", "robbery"]
            }
        }
        
        # Generate crime data for each area
        crime_data = {}
        
        for area_name, area_info in areas.items():
            crime_data[area_name] = {
                "center": area_info["center"],
                "radius": area_info["radius"],
                "crime_level": area_info["crime_level"],
                "incidents": self._generate_incidents_for_area(area_info, 50)
            }
        
        # Add grid-based crime data (1km grid)
        grid_size = 0.01  # approximately 1km
        lat_min, lat_max = -26.3, -26.0
        lon_min, lon_max = 27.9, 28.2
        
        grid_data = {}
        
        for lat in range(int(lat_min / grid_size), int(lat_max / grid_size)):
            for lon in range(int(lon_min / grid_size), int(lon_max / grid_size)):
                grid_lat = lat * grid_size
                grid_lon = lon * grid_size
                
                # Determine crime level based on proximity to known areas
                crime_level = self._determine_grid_crime_level(grid_lat, grid_lon, areas)
                
                grid_key = f"{grid_lat:.4f},{grid_lon:.4f}"
                grid_data[grid_key] = {
                    "center": {"latitude": grid_lat, "longitude": grid_lon},
                    "crime_level": crime_level,
                    "crime_score": self._crime_level_to_score(crime_level),
                    "incidents_count": {
                        "theft": random.randint(0, 20) if crime_level != "very_low" else 0,
                        "robbery": random.randint(0, 10) if crime_level in ["high", "medium"] else 0,
                        "assault": random.randint(0, 5) if crime_level == "high" else 0,
                        "other": random.randint(0, 3)
                    }
                }
        
        # Store the data
        self.crime_data_cache = {
            "areas": crime_data,
            "grid": grid_data,
            "last_updated": datetime.now().isoformat()
        }
    
    def _generate_incidents_for_area(self, area_info, count):
        """Generate synthetic crime incidents for an area."""
        incidents = []
        center = area_info["center"]
        radius = area_info["radius"]
        crime_types = area_info["crime_types"]
        
        # Generate random incidents within the area
        for _ in range(count):
            # Random position within radius
            lat_offset = (random.random() * 2 - 1) * radius * 0.01
            lon_offset = (random.random() * 2 - 1) * radius * 0.01
            
            # Random date within last 90 days
            days_ago = random.randint(0, 90)
            incident_date = (datetime.now() - timedelta(days=days_ago)).isoformat()
            
            # Random time of day (weighted)
            hour_weights = [1, 1, 1, 1, 1, 2, 3, 5, 5, 4, 4, 4, 4, 4, 4, 4, 5, 6, 7, 8, 10, 8, 5, 3]
            hour = random.choices(range(24), weights=hour_weights)[0]
            
            # Random crime type from area's common types
            crime_type = random.choice(crime_types)
            
            incidents.append({
                "id": f"incident_{len(incidents)}",
                "type": crime_type,
                "date": incident_date,
                "hour": hour,
                "location": {
                    "latitude": center["latitude"] + lat_offset,
                    "longitude": center["longitude"] + lon_offset
                },
                "severity": random.choice(["low", "medium", "high"]),
                "description": f"{crime_type.capitalize()} incident"
            })
        
        return incidents
    
    def _determine_grid_crime_level(self, lat, lon, areas):
        """Determine crime level for a grid cell based on proximity to known areas."""
        # Calculate distance to each area center
        min_distance = float('inf')
        closest_area = None
        
        for area_name, area_info in areas.items():
            center = area_info["center"]
            distance = ((lat - center["latitude"]) ** 2 + (lon - center["longitude"]) ** 2) ** 0.5
            
            if distance < min_distance:
                min_distance = distance
                closest_area = area_name
        
        # Determine crime level based on distance and area crime level
        if min_distance < 0.01:  # Very close to area center
            return areas[closest_area]["crime_level"]
        elif min_distance < 0.03:  # Close to area
            level = areas[closest_area]["crime_level"]
            if level == "high":
                return "medium"
            elif level == "medium":
                return "low"
            else:
                return "very_low"
        else:
            # Random level with bias toward very_low
            return random.choices(
                ["very_low", "low", "medium", "high"],
                weights=[70, 20, 8, 2]
            )[0]
    
    def _crime_level_to_score(self, level):
        """Convert crime level to a safety score (0-100)."""
        if level == "very_low":
            return random.randint(90, 100)
        elif level == "low":
            return random.randint(75, 89)
        elif level == "medium":
            return random.randint(50, 74)
        elif level == "high":
            return random.randint(25, 49)
        else:
            return random.randint(0, 24)
    
    def get_crime_data_for_route(self, route_points):
        """
        Get crime data for a route.
        
        Args:
            route_points (list): List of coordinates along the route
            
        Returns:
            dict: Crime data for the route
        """
        try:
            # Check if cache needs refresh
            if time.time() - self.last_cache_update > self.cache_expiry:
                self._load_initial_data()
            
            # Extract grid cells that the route passes through
            grid_cells = self._get_grid_cells_for_route(route_points)
            
            # Calculate average crime score for the route
            total_score = 0
            cell_count = 0
            crime_counts = {"theft": 0, "robbery": 0, "assault": 0, "other": 0}
            
            for cell_key in grid_cells:
                if cell_key in self.crime_data_cache["grid"]:
                    cell_data = self.crime_data_cache["grid"][cell_key]
                    total_score += cell_data["crime_score"]
                    cell_count += 1
                    
                    # Aggregate crime counts
                    for crime_type, count in cell_data["incidents_count"].items():
                        crime_counts[crime_type] += count
            
            # Calculate average score
            avg_score = total_score / max(1, cell_count)
            safety_score = 100 - avg_score  # Convert crime score to safety score
            
            # Generate insights
            insights = self._generate_insights_for_route(route_points, safety_score, crime_counts)
            
            return {
                "safety_score": safety_score,
                "crime_counts": crime_counts,
                "insights": insights,
                "hotspots": self._identify_hotspots_on_route(route_points)
            }
            
        except Exception as e:
            logger.error(f"Error getting crime data for route: {e}")
            return {
                "safety_score": 75,  # Default moderate safety score
                "crime_counts": {"theft": 0, "robbery": 0, "assault": 0, "other": 0},
                "insights": ["Limited crime data available for this route"],
                "hotspots": []
            }
    
    def _get_grid_cells_for_route(self, route_points):
        """Get grid cells that a route passes through."""
        grid_cells = set()
        grid_size = 0.01  # Same as used in _generate_synthetic_data
        
        for point in route_points:
            lat = point["latitude"]
            lon = point["longitude"]
            
            # Round to grid
            grid_lat = round(lat / grid_size) * grid_size
            grid_lon = round(lon / grid_size) * grid_size
            
            grid_key = f"{grid_lat:.4f},{grid_lon:.4f}"
            grid_cells.add(grid_key)
        
        return grid_cells
    
    def _generate_insights_for_route(self, route_points, safety_score, crime_counts):
        """Generate insights for a route based on crime data."""
        insights = []
        
        # Overall safety insight
        if safety_score >= 90:
            insights.append("This route passes through areas with very low crime rates")
        elif safety_score >= 75:
            insights.append("This route generally avoids high-crime areas")
        elif safety_score >= 50:
            insights.append("Some areas along this route have moderate crime rates")
        else:
            insights.append("Exercise caution - this route passes through areas with higher crime rates")
        
        # Crime type insights
        total_crimes = sum(crime_counts.values())
        if total_crimes > 0:
            # Theft insights
            theft_percentage = (crime_counts["theft"] / total_crimes) * 100
            if theft_percentage > 70:
                insights.append("Theft is the most common crime in this area - secure your belongings")
            elif theft_percentage > 40:
                insights.append("Be aware of your belongings as theft occurs in some areas along this route")
            
            # Robbery insights
            robbery_percentage = (crime_counts["robbery"] / total_crimes) * 100
            if robbery_percentage > 30:
                insights.append("This route has some history of robbery incidents - stay alert")
            
            # Assault insights
            assault_percentage = (crime_counts["assault"] / total_crimes) * 100
            if assault_percentage > 20:
                insights.append("Some areas have reported assault incidents - avoid isolated areas")
        
        # Time-based insights
        current_hour = datetime.now().hour
        if 22 <= current_hour or current_hour <= 4:
            insights.append("Late night travel carries additional risk - consider alternative transportation")
        elif 18 <= current_hour < 22:
            insights.append("Be extra vigilant when traveling after dark")
        
        return insights
    
    def _identify_hotspots_on_route(self, route_points):
        """Identify crime hotspots along a route."""
        hotspots = []
        
        # Check each point against known high-crime areas
        for i, point in enumerate(route_points):
            lat = point["latitude"]
            lon = point["longitude"]
            
            # Check against areas
            for area_name, area_info in self.crime_data_cache["areas"].items():
                if area_info["crime_level"] == "high":
                    center = area_info["center"]
                    radius = area_info["radius"] * 0.01  # Convert to coordinate units
                    
                    # Calculate distance
                    distance = ((lat - center["latitude"]) ** 2 + (lon - center["longitude"]) ** 2) ** 0.5
                    
                    if distance < radius:
                        # This point is in a high-crime area
                        hotspots.append({
                            "point_index": i,
                            "location": {"latitude": lat, "longitude": lon},
                            "area_name": area_name,
                            "crime_level": "high",
                            "advice": "Exercise extreme caution in this area"
                        })
        
        return hotspots
    
    def get_safety_score_for_location(self, latitude, longitude, time_of_day=None):
        """
        Get safety score for a specific location.
        
        Args:
            latitude (float): Latitude coordinate
            longitude (float): Longitude coordinate
            time_of_day (str, optional): Time of day (morning, afternoon, evening, night)
            
        Returns:
            dict: Safety information for the location
        """
        try:
            # Check if cache needs refresh
            if time.time() - self.last_cache_update > self.cache_expiry:
                self._load_initial_data()
            
            # Find the nearest grid cell
            grid_size = 0.01
            grid_lat = round(latitude / grid_size) * grid_size
            grid_lon = round(longitude / grid_size) * grid_size
            
            grid_key = f"{grid_lat:.4f},{grid_lon:.4f}"
            
            # Get crime data for the cell
            if grid_key in self.crime_data_cache["grid"]:
                cell_data = self.crime_data_cache["grid"][grid_key]
                crime_score = cell_data["crime_score"]
            else:
                # If no data, estimate based on nearby cells
                crime_score = self._estimate_crime_score(latitude, longitude)
            
            # Convert to safety score
            base_safety_score = 100 - crime_score
            
            # Adjust for time of day
            if time_of_day:
                safety_score = self._adjust_for_time_of_day(base_safety_score, time_of_day)
            else:
                safety_score = base_safety_score
            
            return {
                "location": {"latitude": latitude, "longitude": longitude},
                "safety_score": safety_score,
                "crime_level": self._score_to_crime_level(crime_score),
                "time_of_day": time_of_day
            }
            
        except Exception as e:
            logger.error(f"Error getting safety score for location: {e}")
            return {
                "location": {"latitude": latitude, "longitude": longitude},
                "safety_score": 75,
                "crime_level": "unknown",
                "time_of_day": time_of_day
            }
    
    def _estimate_crime_score(self, latitude, longitude):
        """Estimate crime score for a location without direct data."""
        # Find the 4 nearest grid cells and interpolate
        grid_size = 0.01
        lat_grid = latitude // grid_size
        lon_grid = longitude // grid_size
        
        nearby_cells = [
            f"{lat_grid * grid_size:.4f},{lon_grid * grid_size:.4f}",
            f"{(lat_grid + 1) * grid_size:.4f},{lon_grid * grid_size:.4f}",
            f"{lat_grid * grid_size:.4f},{(lon_grid + 1) * grid_size:.4f}",
            f"{(lat_grid + 1) * grid_size:.4f},{(lon_grid + 1) * grid_size:.4f}"
        ]
        
        total_score = 0
        count = 0
        
        for cell_key in nearby_cells:
            if cell_key in self.crime_data_cache["grid"]:
                total_score += self.crime_data_cache["grid"][cell_key]["crime_score"]
                count += 1
        
        if count > 0:
            return total_score / count
        else:
            # Default moderate crime score
            return 25
    
    def _adjust_for_time_of_day(self, base_safety_score, time_of_day):
        """Adjust safety score based on time of day."""
        if time_of_day == "morning":
            # Morning is generally safer
            return min(100, base_safety_score + 10)
        elif time_of_day == "afternoon":
            # Afternoon is about average
            return base_safety_score
        elif time_of_day == "evening":
            # Evening is slightly less safe
            return max(0, base_safety_score - 10)
        elif time_of_day == "night":
            # Night is significantly less safe
            return max(0, base_safety_score - 20)
        else:
            return base_safety_score
    
    def _score_to_crime_level(self, crime_score):
        """Convert crime score to descriptive level."""
        if crime_score < 10:
            return "very_low"
        elif crime_score < 25:
            return "low"
        elif crime_score < 50:
            return "medium"
        else:
            return "high"
