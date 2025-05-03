"""
Safety Prediction Service for SafeWayAI application.
This module provides AI-driven safety predictions for routes.
"""

import logging
import time
import json
import os
import random
from datetime import datetime, timedelta
import numpy as np
from app.config.azure_config import AI_SERVICES_CONFIG
from app.services.crime_data_service import CrimeDataService

logger = logging.getLogger(__name__)

class SafetyPredictionService:
    """Service for AI-driven safety predictions."""
    
    _instance = None
    
    def __new__(cls):
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super(SafetyPredictionService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the safety prediction service."""
        if self._initialized:
            return
            
        logger.info("Initializing safety prediction service")
        
        # Initialize configuration
        self.ai_config = AI_SERVICES_CONFIG
        
        # Initialize crime data service
        self.crime_data_service = CrimeDataService()
        
        # Initialize model parameters
        self.model_params = {
            "crime_weight": 0.35,
            "lighting_weight": 0.15,
            "foot_traffic_weight": 0.15,
            "police_weight": 0.10,
            "time_weight": 0.10,
            "surveillance_weight": 0.05,
            "road_weight": 0.05,
            "emergency_weight": 0.05
        }
        
        # Initialize prediction cache
        self.prediction_cache = {}
        self.cache_expiry = 1800  # Cache expiry in seconds (30 minutes)
        
        # Load model (in a real implementation, this would load an actual ML model)
        self._load_model()
        
        self._initialized = True
    
    def _load_model(self):
        """Load the prediction model."""
        try:
            # In a real implementation, this would load a trained ML model
            # For now, we'll just set up some parameters
            
            # Check if we have Azure AI credentials
            if self.ai_config.get("api_key") and self.ai_config.get("endpoint"):
                logger.info("Using Azure AI services for predictions")
                self.use_azure_ai = True
            else:
                logger.info("Using local prediction model")
                self.use_azure_ai = False
            
            # Set up time-based risk factors
            self.time_risk_factors = {
                "morning": {
                    "base_modifier": 0.8,  # Lower risk in morning
                    "theft": 1.0,
                    "robbery": 0.7,
                    "assault": 0.6
                },
                "afternoon": {
                    "base_modifier": 1.0,  # Baseline risk
                    "theft": 1.2,
                    "robbery": 0.9,
                    "assault": 0.8
                },
                "evening": {
                    "base_modifier": 1.2,  # Higher risk in evening
                    "theft": 1.3,
                    "robbery": 1.2,
                    "assault": 1.1
                },
                "night": {
                    "base_modifier": 1.5,  # Highest risk at night
                    "theft": 1.0,  # Less theft at night (fewer people)
                    "robbery": 1.5,
                    "assault": 1.7
                }
            }
            
            # Set up lighting factors (by time of day)
            self.lighting_factors = {
                "morning": 0.9,  # Good visibility
                "afternoon": 1.0,  # Best visibility
                "evening": 1.3,  # Reduced visibility
                "night": 1.8    # Poor visibility
            }
            
            # Set up foot traffic patterns (by time of day)
            self.foot_traffic_patterns = {
                "morning": {
                    "residential": 0.7,
                    "commercial": 0.8,
                    "industrial": 0.5,
                    "entertainment": 0.2
                },
                "afternoon": {
                    "residential": 0.5,
                    "commercial": 1.0,
                    "industrial": 0.8,
                    "entertainment": 0.6
                },
                "evening": {
                    "residential": 0.8,
                    "commercial": 0.7,
                    "industrial": 0.3,
                    "entertainment": 1.0
                },
                "night": {
                    "residential": 0.9,
                    "commercial": 0.2,
                    "industrial": 0.1,
                    "entertainment": 0.8
                }
            }
            
        except Exception as e:
            logger.error(f"Error loading prediction model: {e}")
            # Set default parameters
            self.use_azure_ai = False
    
    def predict_route_safety(self, route_points, time_of_day=None, travel_mode="walking"):
        """
        Predict safety for a route using AI analysis.
        
        Args:
            route_points (list): List of coordinates along the route
            time_of_day (str, optional): Time of day for the journey
            travel_mode (str): Mode of travel (walking, driving, transit)
            
        Returns:
            dict: Safety prediction results
        """
        try:
            logger.info(f"Predicting safety for route with {len(route_points)} points at {time_of_day}")
            
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
            
            # Generate cache key
            cache_key = self._generate_cache_key(route_points, time_of_day, travel_mode)
            
            # Check cache
            if cache_key in self.prediction_cache:
                cache_entry = self.prediction_cache[cache_key]
                if time.time() - cache_entry["timestamp"] < self.cache_expiry:
                    return cache_entry["prediction"]
            
            # Get crime data for the route
            crime_data = self.crime_data_service.get_crime_data_for_route(route_points)
            
            # If we have Azure AI credentials, use Azure for prediction
            if self.use_azure_ai:
                prediction = self._predict_with_azure_ai(route_points, time_of_day, travel_mode, crime_data)
            else:
                # Otherwise use our local model
                prediction = self._predict_with_local_model(route_points, time_of_day, travel_mode, crime_data)
            
            # Cache the prediction
            self.prediction_cache[cache_key] = {
                "timestamp": time.time(),
                "prediction": prediction
            }
            
            return prediction
            
        except Exception as e:
            logger.error(f"Error predicting route safety: {e}")
            return {
                "error": str(e),
                "safety_score": 70,  # Default moderate safety score
                "factors": {},
                "insights": ["Error in safety prediction"]
            }
    
    def _generate_cache_key(self, route_points, time_of_day, travel_mode):
        """Generate a cache key for a route prediction."""
        # Use start and end points for the key
        start = route_points[0]
        end = route_points[-1]
        
        return f"{start['latitude']:.4f},{start['longitude']:.4f}-{end['latitude']:.4f},{end['longitude']:.4f}-{time_of_day}-{travel_mode}"
    
    def _predict_with_azure_ai(self, route_points, time_of_day, travel_mode, crime_data):
        """Use Azure AI services for prediction."""
        try:
            logger.info("Using Azure AI for safety prediction")
            
            # In a real implementation, this would call Azure AI services
            # For now, we'll simulate a response with a slight delay
            time.sleep(0.3)
            
            # Simulate an AI response
            return self._predict_with_local_model(route_points, time_of_day, travel_mode, crime_data)
            
        except Exception as e:
            logger.error(f"Error using Azure AI for prediction: {e}")
            return self._predict_with_local_model(route_points, time_of_day, travel_mode, crime_data)
    
    def _predict_with_local_model(self, route_points, time_of_day, travel_mode, crime_data):
        """Use local model for prediction."""
        try:
            # Start with the crime-based safety score
            base_safety_score = crime_data["safety_score"]
            
            # Adjust for time of day
            time_modifier = self.time_risk_factors[time_of_day]["base_modifier"]
            time_adjusted_score = base_safety_score / time_modifier
            
            # Adjust for travel mode
            if travel_mode == "walking":
                # Walking is most vulnerable
                mode_adjusted_score = time_adjusted_score * 0.9
            elif travel_mode == "transit":
                # Transit is safer due to other people
                mode_adjusted_score = time_adjusted_score * 1.1
            else:  # driving
                # Driving is safest
                mode_adjusted_score = time_adjusted_score * 1.2
            
            # Calculate individual factor scores
            factor_scores = self._calculate_factor_scores(route_points, time_of_day, travel_mode, crime_data)
            
            # Calculate weighted safety score
            weighted_score = 0
            for factor, score in factor_scores.items():
                weight = self.model_params.get(f"{factor}_weight", 0.1)
                weighted_score += score * weight
            
            # Round to nearest integer and ensure it's in range
            final_safety_score = max(0, min(100, round(weighted_score)))
            
            # Generate safety insights
            insights = self._generate_safety_insights(factor_scores, time_of_day, travel_mode, crime_data)
            
            # Generate hotspot warnings
            hotspot_warnings = self._generate_hotspot_warnings(crime_data.get("hotspots", []))
            if hotspot_warnings:
                insights.extend(hotspot_warnings)
            
            # Create the result
            result = {
                "safety_score": final_safety_score,
                "factors": factor_scores,
                "insights": insights,
                "time_of_day": time_of_day,
                "travel_mode": travel_mode,
                "hotspots": crime_data.get("hotspots", [])
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error in local prediction model: {e}")
            return {
                "safety_score": 70,
                "factors": {
                    "crime_rate": 70,
                    "lighting": 70,
                    "foot_traffic": 70,
                    "police_presence": 70,
                    "time_of_day": 70,
                    "surveillance": 70,
                    "road_quality": 70,
                    "emergency_services": 70
                },
                "insights": ["Limited safety data available"],
                "time_of_day": time_of_day,
                "travel_mode": travel_mode
            }
    
    def _calculate_factor_scores(self, route_points, time_of_day, travel_mode, crime_data):
        """Calculate scores for individual safety factors."""
        # Start with crime rate from crime data
        crime_score = 100 - (crime_data.get("safety_score", 25))  # Convert safety to crime
        
        # Calculate lighting score based on time of day
        lighting_factor = self.lighting_factors.get(time_of_day, 1.0)
        lighting_score = max(0, min(100, 100 - (crime_score * lighting_factor * 0.7)))
        
        # Estimate foot traffic based on time and area type
        # For simplicity, we'll use a random area type
        area_type = random.choice(["residential", "commercial", "industrial", "entertainment"])
        foot_traffic_factor = self.foot_traffic_patterns.get(time_of_day, {}).get(area_type, 0.5)
        foot_traffic_score = max(0, min(100, 100 - (crime_score * foot_traffic_factor)))
        
        # Police presence is inversely related to crime in high-crime areas
        if crime_score > 70:
            police_score = 60 + random.randint(0, 20)  # Higher police presence in high-crime areas
        elif crime_score > 40:
            police_score = 40 + random.randint(0, 30)
        else:
            police_score = 20 + random.randint(0, 40)  # Lower police presence in low-crime areas
        
        # Time of day score
        if time_of_day == "morning":
            time_score = 90 + random.randint(0, 10)
        elif time_of_day == "afternoon":
            time_score = 80 + random.randint(0, 15)
        elif time_of_day == "evening":
            time_score = 60 + random.randint(0, 20)
        else:  # night
            time_score = 30 + random.randint(0, 30)
        
        # Surveillance score is higher in commercial areas and lower in residential
        if area_type == "commercial" or area_type == "entertainment":
            surveillance_score = 70 + random.randint(0, 20)
        elif area_type == "industrial":
            surveillance_score = 50 + random.randint(0, 30)
        else:  # residential
            surveillance_score = 30 + random.randint(0, 40)
        
        # Road quality is generally good in commercial areas
        if area_type == "commercial":
            road_score = 80 + random.randint(0, 15)
        elif area_type == "entertainment":
            road_score = 75 + random.randint(0, 15)
        elif area_type == "industrial":
            road_score = 60 + random.randint(0, 20)
        else:  # residential
            road_score = 70 + random.randint(0, 20)
        
        # Emergency services are better in commercial and entertainment areas
        if area_type == "commercial" or area_type == "entertainment":
            emergency_score = 80 + random.randint(0, 15)
        elif area_type == "industrial":
            emergency_score = 70 + random.randint(0, 20)
        else:  # residential
            emergency_score = 60 + random.randint(0, 25)
        
        # Return all factor scores
        return {
            "crime_rate": 100 - crime_score,  # Convert back to safety score
            "lighting": lighting_score,
            "foot_traffic": foot_traffic_score,
            "police_presence": police_score,
            "time_of_day": time_score,
            "surveillance": surveillance_score,
            "road_quality": road_score,
            "emergency_services": emergency_score
        }
    
    def _generate_safety_insights(self, factor_scores, time_of_day, travel_mode, crime_data):
        """Generate natural language insights about safety factors."""
        insights = []
        
        # Add insights from crime data
        if "insights" in crime_data and crime_data["insights"]:
            insights.extend(crime_data["insights"])
        
        # Crime rate insights
        crime_score = 100 - factor_scores.get("crime_rate", 70)  # Convert to crime score
        if crime_score < 10:
            insights.append("This route passes through areas with very low crime rates")
        elif crime_score < 25:
            insights.append("This route generally avoids high-crime areas")
        elif crime_score < 50:
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
        
        # Travel mode specific advice
        if travel_mode == "walking":
            insights.append("When walking, stay in well-lit areas and remain aware of your surroundings")
        elif travel_mode == "transit":
            insights.append("Public transit is generally safe, but be cautious at stations and stops")
        
        # Time-specific advice
        if time_of_day == "night":
            insights.append("Take extra precautions when traveling at night")
            if travel_mode == "walking":
                insights.append("Consider using ride-sharing services instead of walking at night")
        
        return insights
    
    def _generate_hotspot_warnings(self, hotspots):
        """Generate warnings for crime hotspots on the route."""
        warnings = []
        
        if hotspots:
            warnings.append(f"This route passes through {len(hotspots)} identified high-risk areas")
            
            # Add specific warnings for the first few hotspots
            for i, hotspot in enumerate(hotspots[:2]):
                if "area_name" in hotspot:
                    warnings.append(f"Exercise caution in the {hotspot['area_name']} area")
        
        return warnings
    
    def get_alternative_routes(self, start_point, end_point, primary_route, time_of_day=None, travel_mode="walking"):
        """
        Generate alternative routes with different safety/speed tradeoffs.
        
        Args:
            start_point (dict): Starting coordinates
            end_point (dict): Ending coordinates
            primary_route (dict): The primary route data
            time_of_day (str, optional): Time of day for the journey
            travel_mode (str): Mode of travel
            
        Returns:
            list: Alternative routes
        """
        try:
            logger.info("Generating alternative routes with AI safety analysis")
            
            # In a real implementation, we would call Azure Maps to get alternative routes
            # and then analyze each one for safety
            
            # For now, we'll generate simulated alternatives
            alternatives = []
            
            # Get the primary route's properties
            primary_distance = primary_route.get("distance", 1.0)
            primary_duration = primary_route.get("duration", 10)
            primary_safety = primary_route.get("safety_score", 80)
            
            # Generate a faster but less safe alternative
            faster_route_points = self._generate_alternative_points(start_point, end_point)
            
            faster_route = {
                "route_type": "faster",
                "distance": max(0.5, primary_distance * 0.85),  # 15% shorter
                "duration": max(5, int(primary_duration * 0.75)),  # 25% faster
                "route_points": faster_route_points
            }
            
            # Analyze safety for the faster route
            faster_safety = self.predict_route_safety(faster_route_points, time_of_day, travel_mode)
            faster_route.update({
                "safety_score": faster_safety["safety_score"],
                "factors": faster_safety["factors"],
                "insights": faster_safety["insights"],
                "hotspots": faster_safety.get("hotspots", [])
            })
            
            alternatives.append(faster_route)
            
            # If the primary route isn't already very safe, generate a safer but slower alternative
            if primary_safety < 85:
                safer_route_points = self._generate_alternative_points(start_point, end_point, "safer")
                
                safer_route = {
                    "route_type": "safer",
                    "distance": primary_distance * 1.2,  # 20% longer
                    "duration": int(primary_duration * 1.3),  # 30% slower
                    "route_points": safer_route_points
                }
                
                # Analyze safety for the safer route
                safer_safety = self.predict_route_safety(safer_route_points, time_of_day, travel_mode)
                safer_route.update({
                    "safety_score": safer_safety["safety_score"],
                    "factors": safer_safety["factors"],
                    "insights": safer_safety["insights"],
                    "hotspots": safer_safety.get("hotspots", [])
                })
                
                alternatives.append(safer_route)
            
            return alternatives
            
        except Exception as e:
            logger.error(f"Error generating alternative routes: {e}")
            return []
    
    def _generate_alternative_points(self, start_point, end_point, route_type="faster"):
        """
        Generate alternative route points between start and end.
        
        Args:
            start_point (dict): Starting coordinates
            end_point (dict): Ending coordinates
            route_type (str): Type of route to generate ("faster" or "safer")
            
        Returns:
            list: List of points along the route
        """
        # In a real implementation, this would come from Azure Maps
        # For now, we'll create a simple path with a deviation
        
        # Extract coordinates
        start_lat = start_point.get("latitude", 0)
        start_lon = start_point.get("longitude", 0)
        end_lat = end_point.get("latitude", 0)
        end_lon = end_point.get("longitude", 0)
        
        # Calculate midpoint with some random deviation
        if route_type == "faster":
            # Faster route is more direct but might go through riskier areas
            mid_lat = (start_lat + end_lat) / 2 + random.uniform(-0.005, 0.005)
            mid_lon = (start_lon + end_lon) / 2 + random.uniform(-0.005, 0.005)
            
            # Create a simple 3-point route
            return [
                {"latitude": start_lat, "longitude": start_lon},
                {"latitude": mid_lat, "longitude": mid_lon},
                {"latitude": end_lat, "longitude": end_lon}
            ]
        else:
            # Safer route has more waypoints and avoids certain areas
            # Create a more complex route with 5 points
            quarter_lat1 = start_lat + (end_lat - start_lat) * 0.25 + random.uniform(-0.01, 0.01)
            quarter_lon1 = start_lon + (end_lon - start_lon) * 0.25 + random.uniform(-0.01, 0.01)
            
            mid_lat = (start_lat + end_lat) / 2 + random.uniform(-0.01, 0.01)
            mid_lon = (start_lon + end_lon) / 2 + random.uniform(-0.01, 0.01)
            
            quarter_lat2 = start_lat + (end_lat - start_lat) * 0.75 + random.uniform(-0.01, 0.01)
            quarter_lon2 = start_lon + (end_lon - start_lon) * 0.75 + random.uniform(-0.01, 0.01)
            
            return [
                {"latitude": start_lat, "longitude": start_lon},
                {"latitude": quarter_lat1, "longitude": quarter_lon1},
                {"latitude": mid_lat, "longitude": mid_lon},
                {"latitude": quarter_lat2, "longitude": quarter_lon2},
                {"latitude": end_lat, "longitude": end_lon}
            ]
