"""
AI Safety Analysis Service for SafeWayAI application.
This module provides AI-driven safety analysis for route calculation.
"""

import logging
import random
import time
from datetime import datetime
import json
from app.config.azure_config import AI_SERVICES_CONFIG

logger = logging.getLogger(__name__)

class AISafetyService:
    """Service for AI-driven safety analysis."""
    
    _instance = None
    
    def __new__(cls):
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super(AISafetyService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the AI safety service."""
        if self._initialized:
            return
            
        logger.info("Initializing AI safety service")
        
        # Initialize AI configuration
        self.api_key = AI_SERVICES_CONFIG.get("api_key", "")
        self.endpoint = AI_SERVICES_CONFIG.get("endpoint", "")
        
        # Safety factors and their weights
        self.safety_factors = {
            "crime_rate": 0.30,           # Historical crime data
            "lighting": 0.15,             # Street lighting quality
            "foot_traffic": 0.15,         # Pedestrian density
            "police_presence": 0.10,      # Proximity to police stations/patrols
            "time_of_day": 0.10,          # Time-based risk assessment
            "surveillance": 0.10,         # CCTV coverage
            "road_quality": 0.05,         # Road/sidewalk condition
            "emergency_services": 0.05,   # Proximity to hospitals/fire stations
        }
        
        # Initialize safety data cache
        self.safety_data_cache = {}
        
        self._initialized = True
    
    def analyze_route_safety(self, route_points, time_of_day=None):
        """
        Analyze the safety of a route using AI.
        
        Args:
            route_points (list): List of coordinates along the route
            time_of_day (str, optional): Time of day for the journey
            
        Returns:
            dict: Safety analysis results
        """
        try:
            logger.info(f"Analyzing safety for route with {len(route_points)} points")
            
            # Use current time if not specified
            if time_of_day is None:
                current_hour = datetime.now().hour
                if 5 <= current_hour < 12:
                    time_of_day = "morning"
                elif 12 <= current_hour < 17:
                    time_of_day = "afternoon"
                elif 17 <= current_hour < 21:
                    time_of_day = "evening"
                else:
                    time_of_day = "night"
            
            # Check if we have a valid API key and endpoint
            if self.api_key and self.endpoint and self.api_key != "YOUR_API_KEY":
                # In a real implementation, we would call Azure AI services here
                return self._call_azure_ai_service(route_points, time_of_day)
            else:
                # Fall back to simulated analysis
                return self._simulate_safety_analysis(route_points, time_of_day)
                
        except Exception as e:
            logger.error(f"Error analyzing route safety: {e}")
            return {
                "error": str(e),
                "safety_score": 70,  # Default moderate safety score
                "factors": {}
            }
    
    def _call_azure_ai_service(self, route_points, time_of_day):
        """
        Call Azure AI services for safety analysis.
        
        Args:
            route_points (list): List of coordinates along the route
            time_of_day (str): Time of day for the journey
            
        Returns:
            dict: Safety analysis from Azure AI
        """
        try:
            logger.info("Calling Azure AI service for safety analysis")
            
            # In a real implementation, this would make an API call to Azure AI services
            # For now, we'll simulate a response with a slight delay
            time.sleep(0.5)
            
            # Simulate an AI response
            return self._simulate_safety_analysis(route_points, time_of_day)
            
        except Exception as e:
            logger.error(f"Error calling Azure AI service: {e}")
            return {
                "error": str(e),
                "safety_score": 70,
                "factors": {}
            }
    
    def _simulate_safety_analysis(self, route_points, time_of_day):
        """
        Simulate AI safety analysis for testing.
        
        Args:
            route_points (list): List of coordinates along the route
            time_of_day (str): Time of day for the journey
            
        Returns:
            dict: Simulated safety analysis
        """
        try:
            # Extract start and end points
            start_point = route_points[0] if route_points else {"latitude": 0, "longitude": 0}
            end_point = route_points[-1] if len(route_points) > 1 else start_point
            
            # Generate a cache key based on start/end points and time
            cache_key = f"{start_point['latitude']},{start_point['longitude']}-{end_point['latitude']},{end_point['longitude']}-{time_of_day}"
            
            # Check if we have cached results
            if cache_key in self.safety_data_cache:
                return self.safety_data_cache[cache_key]
            
            # Time of day affects safety
            time_factors = {
                "morning": {"base": 85, "range": 10},
                "afternoon": {"base": 80, "range": 15},
                "evening": {"base": 70, "range": 20},
                "night": {"base": 60, "range": 25}
            }
            
            time_factor = time_factors.get(time_of_day, {"base": 75, "range": 15})
            
            # Base safety score adjusted by time of day
            base_score = time_factor["base"]
            score_range = time_factor["range"]
            
            # Randomize slightly but keep within reasonable range
            safety_score = max(40, min(95, base_score + random.randint(-score_range, score_range)))
            
            # Generate factor scores
            factor_scores = {}
            for factor, weight in self.safety_factors.items():
                # Time of day is handled specially
                if factor == "time_of_day":
                    if time_of_day == "night":
                        factor_scores[factor] = max(30, min(60, base_score - 20 + random.randint(-10, 10)))
                    elif time_of_day == "evening":
                        factor_scores[factor] = max(50, min(80, base_score - 10 + random.randint(-10, 10)))
                    else:
                        factor_scores[factor] = max(70, min(95, base_score + 10 + random.randint(-10, 10)))
                else:
                    # Other factors vary around the base score
                    factor_scores[factor] = max(30, min(95, base_score + random.randint(-15, 15)))
            
            # Calculate weighted safety score
            weighted_score = 0
            for factor, score in factor_scores.items():
                weighted_score += score * self.safety_factors[factor]
            
            # Round to nearest integer
            final_safety_score = round(weighted_score)
            
            # Generate safety insights
            insights = self._generate_safety_insights(factor_scores, time_of_day)
            
            # Create the result
            result = {
                "safety_score": final_safety_score,
                "factors": factor_scores,
                "insights": insights,
                "time_of_day": time_of_day
            }
            
            # Cache the result
            self.safety_data_cache[cache_key] = result
            
            return result
            
        except Exception as e:
            logger.error(f"Error simulating safety analysis: {e}")
            return {
                "safety_score": 70,
                "factors": {factor: 70 for factor in self.safety_factors},
                "insights": ["Limited safety data available"],
                "time_of_day": time_of_day
            }
    
    def _generate_safety_insights(self, factor_scores, time_of_day):
        """
        Generate natural language insights about safety factors.
        
        Args:
            factor_scores (dict): Scores for each safety factor
            time_of_day (str): Time of day for the journey
            
        Returns:
            list: Safety insights
        """
        insights = []
        
        # Crime rate insights
        crime_score = factor_scores.get("crime_rate", 70)
        if crime_score >= 85:
            insights.append("This route passes through areas with very low crime rates")
        elif crime_score >= 70:
            insights.append("This route generally avoids high-crime areas")
        elif crime_score >= 50:
            insights.append("Some areas along this route have moderate crime rates")
        else:
            insights.append("Exercise caution - some areas have higher crime rates")
        
        # Lighting insights
        lighting_score = factor_scores.get("lighting", 70)
        if time_of_day in ["evening", "night"]:
            if lighting_score >= 85:
                insights.append("Excellent street lighting throughout the route")
            elif lighting_score >= 70:
                insights.append("Good street lighting in most areas")
            elif lighting_score >= 50:
                insights.append("Street lighting is adequate but some areas may be dimly lit")
            else:
                insights.append("Limited street lighting in some areas - use caution at night")
        
        # Foot traffic insights
        traffic_score = factor_scores.get("foot_traffic", 70)
        if traffic_score >= 85:
            insights.append("High pedestrian activity provides safety in numbers")
        elif traffic_score >= 70:
            insights.append("Moderate pedestrian traffic along most of the route")
        elif traffic_score >= 50:
            insights.append("Some sections have limited pedestrian activity")
        else:
            insights.append("Low foot traffic in some areas - stay alert")
        
        # Police presence
        police_score = factor_scores.get("police_presence", 70)
        if police_score >= 80:
            insights.append("Regular police patrols in this area")
        
        # Surveillance
        surveillance_score = factor_scores.get("surveillance", 70)
        if surveillance_score >= 80:
            insights.append("Good CCTV coverage along the route")
        elif surveillance_score <= 50:
            insights.append("Limited surveillance coverage in some areas")
        
        # Time-specific advice
        if time_of_day == "night":
            insights.append("Take extra precautions when traveling at night")
        
        return insights
    
    def get_alternative_routes(self, start_point, end_point, primary_route, time_of_day=None):
        """
        Generate alternative routes with different safety/speed tradeoffs.
        
        Args:
            start_point (dict): Starting coordinates
            end_point (dict): Ending coordinates
            primary_route (dict): The primary route data
            time_of_day (str, optional): Time of day for the journey
            
        Returns:
            list: Alternative routes
        """
        try:
            logger.info("Generating alternative routes")
            
            # In a real implementation, we would call Azure Maps to get alternative routes
            # and then analyze each one for safety
            
            # For now, we'll generate simulated alternatives
            alternatives = []
            
            # Get the primary route's properties
            primary_distance = primary_route.get("distance", 1.0)
            primary_duration = primary_route.get("duration", 10)
            primary_safety = primary_route.get("safety_score", 80)
            
            # Generate a faster but less safe alternative
            faster_route = {
                "route_type": "faster",
                "distance": max(0.5, primary_distance * 0.85),  # 15% shorter
                "duration": max(5, int(primary_duration * 0.75)),  # 25% faster
                "safety_score": max(40, primary_safety - random.randint(10, 20)),  # Less safe
                "route_points": self._generate_alternative_points(start_point, end_point)
            }
            
            # Analyze safety for the faster route
            safety_analysis = self._simulate_safety_analysis(faster_route["route_points"], time_of_day)
            faster_route.update({
                "safety_score": safety_analysis["safety_score"],
                "factors": safety_analysis["factors"],
                "insights": safety_analysis["insights"]
            })
            
            alternatives.append(faster_route)
            
            # If the primary route isn't already very safe, generate a safer but slower alternative
            if primary_safety < 85:
                safer_route = {
                    "route_type": "safer",
                    "distance": primary_distance * 1.2,  # 20% longer
                    "duration": int(primary_duration * 1.3),  # 30% slower
                    "safety_score": min(95, primary_safety + random.randint(10, 15)),  # Safer
                    "route_points": self._generate_alternative_points(start_point, end_point)
                }
                
                # Analyze safety for the safer route
                safety_analysis = self._simulate_safety_analysis(safer_route["route_points"], time_of_day)
                safer_route.update({
                    "safety_score": safety_analysis["safety_score"],
                    "factors": safety_analysis["factors"],
                    "insights": safety_analysis["insights"]
                })
                
                alternatives.append(safer_route)
            
            return alternatives
            
        except Exception as e:
            logger.error(f"Error generating alternative routes: {e}")
            return []
    
    def _generate_alternative_points(self, start_point, end_point):
        """
        Generate alternative route points between start and end.
        
        Args:
            start_point (dict): Starting coordinates
            end_point (dict): Ending coordinates
            
        Returns:
            list: List of points along the route
        """
        # In a real implementation, this would come from Azure Maps
        # For now, we'll create a simple path with a slight deviation
        
        # Extract coordinates
        start_lat = start_point.get("latitude", 0)
        start_lon = start_point.get("longitude", 0)
        end_lat = end_point.get("latitude", 0)
        end_lon = end_point.get("longitude", 0)
        
        # Calculate midpoint with some random deviation
        mid_lat = (start_lat + end_lat) / 2 + random.uniform(-0.01, 0.01)
        mid_lon = (start_lon + end_lon) / 2 + random.uniform(-0.01, 0.01)
        
        # Create a simple 3-point route
        return [
            {"latitude": start_lat, "longitude": start_lon},
            {"latitude": mid_lat, "longitude": mid_lon},
            {"latitude": end_lat, "longitude": end_lon}
        ]
