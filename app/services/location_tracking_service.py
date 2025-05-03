"""
Location Tracking Service for SafeWayAI application.
This module provides real-time location tracking and safety alerts.
"""

import logging
import time
import threading
import random
from datetime import datetime
from app.services.safety_prediction_service import SafetyPredictionService
from app.services.crime_data_service import CrimeDataService

logger = logging.getLogger(__name__)

class LocationTrackingService:
    """Service for real-time location tracking and safety alerts."""
    
    _instance = None
    
    def __new__(cls):
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super(LocationTrackingService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the location tracking service."""
        if self._initialized:
            return
            
        logger.info("Initializing location tracking service")
        
        # Initialize services
        self.safety_prediction_service = SafetyPredictionService()
        self.crime_data_service = CrimeDataService()
        
        # Initialize tracking state
        self.active_tracks = {}
        self.track_lock = threading.Lock()
        
        # Initialize alert thresholds
        self.alert_thresholds = {
            "safety_score": 40,  # Alert if safety score drops below this
            "hotspot_proximity": 0.005,  # Alert if within this distance of a hotspot (approx 500m)
            "deviation": 0.01,  # Alert if deviation from route exceeds this (approx 1km)
            "emergency_button": True  # Enable emergency button alerts
        }
        
        # Start tracking thread
        self.tracking_active = True
        self.tracking_thread = threading.Thread(target=self._tracking_loop)
        self.tracking_thread.daemon = True
        self.tracking_thread.start()
        
        self._initialized = True
    
    def start_tracking(self, user_id, route_data, callback=None):
        """
        Start tracking a user along a route.
        
        Args:
            user_id (str): User identifier
            route_data (dict): Route information including points, safety data
            callback (function, optional): Callback for alerts and updates
            
        Returns:
            str: Tracking ID
        """
        try:
            # Generate tracking ID
            tracking_id = f"track_{user_id}_{int(time.time())}"
            
            # Extract route information
            route_points = route_data.get("route_points", [])
            if not route_points:
                logger.error("Cannot start tracking: no route points provided")
                return None
            
            # Create tracking record
            with self.track_lock:
                self.active_tracks[tracking_id] = {
                    "user_id": user_id,
                    "route_data": route_data,
                    "start_time": datetime.now(),
                    "current_position": route_points[0],
                    "current_index": 0,
                    "progress": 0.0,  # 0-100%
                    "status": "active",
                    "alerts": [],
                    "callback": callback,
                    "last_update": time.time(),
                    "simulation_speed": 1.0,  # For simulated movement
                    "last_safety_check": time.time()
                }
            
            logger.info(f"Started tracking {tracking_id} for user {user_id}")
            return tracking_id
            
        except Exception as e:
            logger.error(f"Error starting tracking: {e}")
            return None
    
    def stop_tracking(self, tracking_id):
        """
        Stop tracking a user.
        
        Args:
            tracking_id (str): Tracking identifier
            
        Returns:
            bool: Success status
        """
        try:
            with self.track_lock:
                if tracking_id in self.active_tracks:
                    self.active_tracks[tracking_id]["status"] = "completed"
                    logger.info(f"Stopped tracking {tracking_id}")
                    return True
                else:
                    logger.warning(f"Tracking ID not found: {tracking_id}")
                    return False
                
        except Exception as e:
            logger.error(f"Error stopping tracking: {e}")
            return False
    
    def get_tracking_status(self, tracking_id):
        """
        Get current tracking status.
        
        Args:
            tracking_id (str): Tracking identifier
            
        Returns:
            dict: Tracking status information
        """
        try:
            with self.track_lock:
                if tracking_id in self.active_tracks:
                    track = self.active_tracks[tracking_id]
                    
                    # Create a copy of the status without the callback
                    status = {k: v for k, v in track.items() if k != "callback"}
                    
                    # Add elapsed time
                    elapsed = datetime.now() - track["start_time"]
                    status["elapsed_seconds"] = elapsed.total_seconds()
                    
                    # Add estimated time remaining
                    if status["progress"] > 0:
                        remaining_seconds = (elapsed.total_seconds() / status["progress"]) * (100 - status["progress"])
                        status["remaining_seconds"] = remaining_seconds
                    else:
                        status["remaining_seconds"] = None
                    
                    return status
                else:
                    logger.warning(f"Tracking ID not found: {tracking_id}")
                    return None
                
        except Exception as e:
            logger.error(f"Error getting tracking status: {e}")
            return None
    
    def update_user_location(self, tracking_id, latitude, longitude):
        """
        Update a user's location manually.
        
        Args:
            tracking_id (str): Tracking identifier
            latitude (float): Current latitude
            longitude (float): Current longitude
            
        Returns:
            dict: Updated tracking status
        """
        try:
            with self.track_lock:
                if tracking_id in self.active_tracks:
                    track = self.active_tracks[tracking_id]
                    
                    # Update position
                    track["current_position"] = {
                        "latitude": latitude,
                        "longitude": longitude
                    }
                    
                    # Update last update time
                    track["last_update"] = time.time()
                    
                    # Calculate progress along route
                    self._update_route_progress(tracking_id)
                    
                    # Check for safety issues
                    self._check_safety(tracking_id)
                    
                    return self.get_tracking_status(tracking_id)
                else:
                    logger.warning(f"Tracking ID not found: {tracking_id}")
                    return None
                
        except Exception as e:
            logger.error(f"Error updating user location: {e}")
            return None
    
    def trigger_emergency(self, tracking_id, emergency_type="sos", details=None):
        """
        Trigger an emergency alert.
        
        Args:
            tracking_id (str): Tracking identifier
            emergency_type (str): Type of emergency (sos, medical, fire, etc.)
            details (dict, optional): Additional details about the emergency
            
        Returns:
            bool: Success status
        """
        try:
            with self.track_lock:
                if tracking_id in self.active_tracks:
                    track = self.active_tracks[tracking_id]
                    
                    # Create emergency alert
                    alert = {
                        "type": "emergency",
                        "emergency_type": emergency_type,
                        "timestamp": datetime.now().isoformat(),
                        "position": track["current_position"],
                        "details": details or {}
                    }
                    
                    # Add to alerts
                    track["alerts"].append(alert)
                    
                    # Set status to emergency
                    track["status"] = "emergency"
                    
                    # Call callback if available
                    if track["callback"]:
                        try:
                            track["callback"](tracking_id, "emergency", alert)
                        except Exception as callback_error:
                            logger.error(f"Error in emergency callback: {callback_error}")
                    
                    logger.info(f"Emergency triggered for {tracking_id}: {emergency_type}")
                    
                    # In a real implementation, this would contact emergency services
                    # or send notifications to emergency contacts
                    
                    return True
                else:
                    logger.warning(f"Tracking ID not found: {tracking_id}")
                    return False
                
        except Exception as e:
            logger.error(f"Error triggering emergency: {e}")
            return False
    
    def _tracking_loop(self):
        """Background thread for updating tracking status."""
        while self.tracking_active:
            try:
                # Process each active track
                with self.track_lock:
                    for tracking_id, track in list(self.active_tracks.items()):
                        if track["status"] in ["active", "warning"]:
                            # Update simulated position
                            self._update_simulated_position(tracking_id)
                            
                            # Check safety if it's time
                            if time.time() - track["last_safety_check"] > 10:  # Check every 10 seconds
                                self._check_safety(tracking_id)
                                track["last_safety_check"] = time.time()
                            
                            # Clean up completed tracks after 1 hour
                        elif track["status"] == "completed" and time.time() - track["last_update"] > 3600:
                            del self.active_tracks[tracking_id]
                
                # Sleep to avoid high CPU usage
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error in tracking loop: {e}")
                time.sleep(5)  # Sleep longer on error
    
    def _update_simulated_position(self, tracking_id):
        """Update simulated position along the route."""
        track = self.active_tracks[tracking_id]
        
        # Only update if in simulation mode
        if track.get("simulation_mode", True):
            route_points = track["route_data"].get("route_points", [])
            if len(route_points) < 2:
                return
            
            current_index = track["current_index"]
            
            # If we've reached the end, mark as completed
            if current_index >= len(route_points) - 1:
                track["status"] = "completed"
                track["progress"] = 100.0
                return
            
            # Calculate time since last update
            elapsed = time.time() - track["last_update"]
            
            # Adjust for simulation speed
            elapsed *= track["simulation_speed"]
            
            # Calculate how far to move
            current_point = route_points[current_index]
            next_point = route_points[current_index + 1]
            
            # Calculate distance between points
            distance = ((next_point["latitude"] - current_point["latitude"]) ** 2 + 
                        (next_point["longitude"] - current_point["longitude"]) ** 2) ** 0.5
            
            # Calculate speed (in coordinate units per second)
            # This is a simplified calculation - in reality would depend on travel mode
            speed = 0.0001  # Approximately 10m/s or 36km/h
            
            # Calculate progress along segment
            progress = elapsed * speed / distance if distance > 0 else 1.0
            
            if progress >= 1.0:
                # Move to next segment
                track["current_index"] = current_index + 1
                track["current_position"] = next_point
                track["last_update"] = time.time()
            else:
                # Interpolate position
                new_lat = current_point["latitude"] + progress * (next_point["latitude"] - current_point["latitude"])
                new_lon = current_point["longitude"] + progress * (next_point["longitude"] - current_point["longitude"])
                
                track["current_position"] = {
                    "latitude": new_lat,
                    "longitude": new_lon
                }
            
            # Update overall progress
            self._update_route_progress(tracking_id)
    
    def _update_route_progress(self, tracking_id):
        """Update progress along the route."""
        track = self.active_tracks[tracking_id]
        route_points = track["route_data"].get("route_points", [])
        
        if len(route_points) < 2:
            track["progress"] = 100.0
            return
        
        # Calculate total route distance
        total_distance = 0
        for i in range(len(route_points) - 1):
            p1 = route_points[i]
            p2 = route_points[i + 1]
            segment_distance = ((p2["latitude"] - p1["latitude"]) ** 2 + 
                               (p2["longitude"] - p1["longitude"]) ** 2) ** 0.5
            total_distance += segment_distance
        
        # Calculate distance traveled
        distance_traveled = 0
        current_pos = track["current_position"]
        
        # Add distance of completed segments
        for i in range(track["current_index"]):
            p1 = route_points[i]
            p2 = route_points[i + 1]
            segment_distance = ((p2["latitude"] - p1["latitude"]) ** 2 + 
                               (p2["longitude"] - p1["longitude"]) ** 2) ** 0.5
            distance_traveled += segment_distance
        
        # Add distance of current segment
        if track["current_index"] < len(route_points) - 1:
            p1 = route_points[track["current_index"]]
            current_segment_distance = ((current_pos["latitude"] - p1["latitude"]) ** 2 + 
                                       (current_pos["longitude"] - p1["longitude"]) ** 2) ** 0.5
            distance_traveled += current_segment_distance
        
        # Calculate progress percentage
        if total_distance > 0:
            track["progress"] = min(100.0, (distance_traveled / total_distance) * 100.0)
        else:
            track["progress"] = 100.0
    
    def _check_safety(self, tracking_id):
        """Check for safety issues along the route."""
        track = self.active_tracks[tracking_id]
        current_pos = track["current_position"]
        
        # Get current time of day
        current_hour = datetime.now().hour
        if 5 <= current_hour < 12:
            time_of_day = "morning"
        elif 12 <= current_hour < 17:
            time_of_day = "afternoon"
        elif 17 <= current_hour < 21:
            time_of_day = "evening"
        else:
            time_of_day = "night"
        
        # Check safety score for current location
        safety_info = self.crime_data_service.get_safety_score_for_location(
            current_pos["latitude"], 
            current_pos["longitude"],
            time_of_day
        )
        
        # Check for hotspots
        route_data = track["route_data"]
        hotspots = route_data.get("hotspots", [])
        
        # Check if we're near any hotspot
        near_hotspot = False
        for hotspot in hotspots:
            hotspot_pos = hotspot.get("location", {})
            distance = ((current_pos["latitude"] - hotspot_pos.get("latitude", 0)) ** 2 + 
                        (current_pos["longitude"] - hotspot_pos.get("longitude", 0)) ** 2) ** 0.5
            
            if distance < self.alert_thresholds["hotspot_proximity"]:
                near_hotspot = True
                
                # Create hotspot alert if we haven't already
                if not any(a.get("type") == "hotspot" and a.get("hotspot_id") == hotspot.get("area_name", "") 
                          for a in track["alerts"]):
                    alert = {
                        "type": "hotspot",
                        "hotspot_id": hotspot.get("area_name", ""),
                        "timestamp": datetime.now().isoformat(),
                        "position": current_pos,
                        "safety_score": safety_info["safety_score"],
                        "advice": hotspot.get("advice", "Exercise caution in this area")
                    }
                    
                    track["alerts"].append(alert)
                    track["status"] = "warning"
                    
                    # Call callback if available
                    if track["callback"]:
                        try:
                            track["callback"](tracking_id, "hotspot_warning", alert)
                        except Exception as callback_error:
                            logger.error(f"Error in hotspot callback: {callback_error}")
        
        # Check for low safety score
        if safety_info["safety_score"] < self.alert_thresholds["safety_score"]:
            # Create safety alert if we haven't already for this area
            if not any(a.get("type") == "safety" and 
                      abs(a.get("position", {}).get("latitude", 0) - current_pos["latitude"]) < 0.001 and
                      abs(a.get("position", {}).get("longitude", 0) - current_pos["longitude"]) < 0.001
                      for a in track["alerts"]):
                alert = {
                    "type": "safety",
                    "timestamp": datetime.now().isoformat(),
                    "position": current_pos,
                    "safety_score": safety_info["safety_score"],
                    "advice": "You are entering an area with higher risk. Stay alert and consider alternative routes."
                }
                
                track["alerts"].append(alert)
                track["status"] = "warning"
                
                # Call callback if available
                if track["callback"]:
                    try:
                        track["callback"](tracking_id, "safety_warning", alert)
                    except Exception as callback_error:
                        logger.error(f"Error in safety callback: {callback_error}")
        
        # Check for route deviation
        if not track.get("simulation_mode", True):  # Only check for real tracking, not simulation
            route_points = route_data.get("route_points", [])
            
            # Find closest point on route
            min_distance = float('inf')
            for point in route_points:
                distance = ((current_pos["latitude"] - point["latitude"]) ** 2 + 
                           (current_pos["longitude"] - point["longitude"]) ** 2) ** 0.5
                
                if distance < min_distance:
                    min_distance = distance
            
            # Check if deviation exceeds threshold
            if min_distance > self.alert_thresholds["deviation"]:
                # Create deviation alert if we haven't already
                if not any(a.get("type") == "deviation" for a in track["alerts"][-3:]):  # Check last 3 alerts
                    alert = {
                        "type": "deviation",
                        "timestamp": datetime.now().isoformat(),
                        "position": current_pos,
                        "deviation_distance": min_distance * 111000,  # Convert to meters (approx)
                        "advice": "You have deviated from the planned route. Consider returning to the route or recalculating."
                    }
                    
                    track["alerts"].append(alert)
                    
                    # Call callback if available
                    if track["callback"]:
                        try:
                            track["callback"](tracking_id, "deviation_warning", alert)
                        except Exception as callback_error:
                            logger.error(f"Error in deviation callback: {callback_error}")
        
        # Return to normal status if no recent warnings
        if track["status"] == "warning":
            # Check if last warning was more than 60 seconds ago
            if (not track["alerts"] or 
                datetime.now().timestamp() - datetime.fromisoformat(track["alerts"][-1]["timestamp"]).timestamp() > 60):
                track["status"] = "active"
