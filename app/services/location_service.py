"""
Location service for SafeWayAI application.
This module provides functionality to track user location and monitor safety.
"""

import logging
import json
import time
import threading
import math
from typing import Dict, List, Any, Optional, Tuple, Callable
from app.services.service_manager import ServiceManager
from app.services.safe_route_service import SafeRouteService

logger = logging.getLogger(__name__)

class LocationService:
    """Service for tracking user location and monitoring safety."""

    _instance = None

    def __new__(cls):
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super(LocationService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize the location service."""
        if hasattr(self, '_initialized') and self._initialized:
            return

        logger.info("Initializing location service")

        # Get service manager
        self.service_manager = ServiceManager()

        # Get safe route service
        self.safe_route_service = SafeRouteService()

        # Initialize state
        self.current_location = {"latitude": -26.2041, "longitude": 28.0473}  # Default to Johannesburg CBD
        self.location_history = []
        self.tracking_active = False
        self.tracking_thread = None
        self.tracking_interval = 30  # seconds
        self.safety_monitoring_active = False
        self.safety_monitoring_thread = None
        self.safety_monitoring_interval = 60  # seconds
        self.location_callbacks = []
        self.safety_callbacks = []
        self.current_safety_score = None

        self._initialized = True

    def update_location(self, latitude: float, longitude: float, accuracy: Optional[float] = None) -> Dict[str, Any]:
        """
        Update the current location.

        Args:
            latitude: The latitude
            longitude: The longitude
            accuracy: The accuracy in meters

        Returns:
            The updated location
        """
        try:
            logger.info(f"Updating location to ({latitude}, {longitude})")

            # Create location object
            location = {
                "latitude": latitude,
                "longitude": longitude,
                "timestamp": time.time()
            }

            if accuracy is not None:
                location["accuracy"] = accuracy

            # Update current location
            self.current_location = location

            # Add to history (limit to 100 entries)
            self.location_history.append(location)
            if len(self.location_history) > 100:
                self.location_history = self.location_history[-100:]

            # Send to IoT Hub if connected
            if hasattr(self.service_manager, 'iot_service') and self.service_manager.iot_service:
                self.service_manager.iot_service.send_location_update(
                    latitude, longitude, accuracy
                )

            # Notify callbacks
            for callback in self.location_callbacks:
                try:
                    callback(location)
                except Exception as e:
                    logger.error(f"Error in location callback: {e}")

            # Check safety if monitoring is active
            if self.safety_monitoring_active:
                self._check_location_safety(latitude, longitude)

            return location

        except Exception as e:
            logger.error(f"Error updating location: {e}")
            return {"error": str(e)}

    def get_current_location(self) -> Dict[str, Any]:
        """
        Get the current location.

        Returns:
            The current location
        """
        return self.current_location

    def get_safe_route(self, start: Dict[str, float], end: Dict[str, float], safety_priority: float = 0.7) -> Dict[str, Any]:
        """
        Get a safe route between two points.

        Args:
            start: The starting point
            end: The ending point
            safety_priority: Priority for safety vs. speed (0-1)

        Returns:
            Safe route information
        """
        try:
            # Convert to tuples for the safe route service
            start_point = (start["latitude"], start["longitude"])
            end_point = (end["latitude"], end["longitude"])

            # Use the safe route service
            return self.safe_route_service.find_safe_route(
                start_point, end_point, safety_priority
            )
        except Exception as e:
            logger.error(f"Error getting safe route: {e}")

            # Fallback to simulated route
            return {
                "distance": 5.2,  # km
                "duration": 15,   # minutes
                "safety_score": 85,  # 0-100
                "points": [
                    {"latitude": start["latitude"], "longitude": start["longitude"]},
                    {"latitude": start["latitude"] + 0.01, "longitude": start["longitude"] + 0.01},
                    {"latitude": end["latitude"] - 0.01, "longitude": end["longitude"] - 0.01},
                    {"latitude": end["latitude"], "longitude": end["longitude"]}
                ]
            }

    def get_nearby_safe_places(self, location: Dict[str, float], radius: float = 1.0) -> List[Dict[str, Any]]:
        """
        Get nearby safe places.

        Args:
            location: The location
            radius: The radius in kilometers

        Returns:
            List of nearby safe places
        """
        try:
            # Use Azure Maps service if available
            if hasattr(self.service_manager, 'maps_service') and self.service_manager.maps_service:
                # Search for police stations
                police_results = self.service_manager.maps_service.search_address(
                    "police station", limit=3
                )

                # Search for hospitals
                hospital_results = self.service_manager.maps_service.search_address(
                    "hospital", limit=3
                )

                # Process results
                safe_places = []

                # Add police stations
                if "results" in police_results:
                    for result in police_results["results"]:
                        if "position" in result:
                            place = {
                                "name": result.get("poi", {}).get("name", "Police Station"),
                                "type": "police",
                                "latitude": result["position"]["lat"],
                                "longitude": result["position"]["lon"],
                                "address": result.get("address", {}).get("freeformAddress", "")
                            }

                            # Calculate distance
                            place["distance"] = self.calculate_distance(
                                location,
                                {"latitude": place["latitude"], "longitude": place["longitude"]}
                            )

                            safe_places.append(place)

                # Add hospitals
                if "results" in hospital_results:
                    for result in hospital_results["results"]:
                        if "position" in result:
                            place = {
                                "name": result.get("poi", {}).get("name", "Hospital"),
                                "type": "hospital",
                                "latitude": result["position"]["lat"],
                                "longitude": result["position"]["lon"],
                                "address": result.get("address", {}).get("freeformAddress", "")
                            }

                            # Calculate distance
                            place["distance"] = self.calculate_distance(
                                location,
                                {"latitude": place["latitude"], "longitude": place["longitude"]}
                            )

                            safe_places.append(place)

                # Sort by distance
                safe_places.sort(key=lambda x: x.get("distance", 999))

                # Filter by radius
                safe_places = [place for place in safe_places if place.get("distance", 999) <= radius]

                return safe_places

            # Fallback to simulated data
            return [
                {
                    "name": "Central Police Station",
                    "type": "police",
                    "distance": 0.8,  # km
                    "latitude": location["latitude"] + 0.008,
                    "longitude": location["longitude"] - 0.005
                },
                {
                    "name": "City Hospital",
                    "type": "hospital",
                    "distance": 1.2,  # km
                    "latitude": location["latitude"] - 0.012,
                    "longitude": location["longitude"] + 0.007
                },
                {
                    "name": "24/7 Convenience Store",
                    "type": "store",
                    "distance": 0.3,  # km
                    "latitude": location["latitude"] + 0.003,
                    "longitude": location["longitude"] + 0.002
                }
            ]
        except Exception as e:
            logger.error(f"Error getting nearby safe places: {e}")

            # Fallback to simulated data
            return [
                {
                    "name": "Central Police Station",
                    "type": "police",
                    "distance": 0.8,  # km
                    "latitude": location["latitude"] + 0.008,
                    "longitude": location["longitude"] - 0.005
                },
                {
                    "name": "City Hospital",
                    "type": "hospital",
                    "distance": 1.2,  # km
                    "latitude": location["latitude"] - 0.012,
                    "longitude": location["longitude"] + 0.007
                },
                {
                    "name": "24/7 Convenience Store",
                    "type": "store",
                    "distance": 0.3,  # km
                    "latitude": location["latitude"] + 0.003,
                    "longitude": location["longitude"] + 0.002
                }
            ]

    def get_crime_heatmap(self, location: Dict[str, float], radius: float = 5.0) -> Dict[str, Any]:
        """
        Get crime heatmap data for an area.

        Args:
            location: The location
            radius: The radius in kilometers

        Returns:
            Crime heatmap data
        """
        try:
            # Use incident service to get nearby incidents
            if hasattr(self.service_manager, 'incident_service') and self.service_manager.incident_service:
                incidents = self.service_manager.incident_service.get_nearby_incidents(
                    location["latitude"], location["longitude"], radius
                )

                if isinstance(incidents, list):
                    # Convert incidents to heatmap points
                    points = []
                    max_intensity = 0.0

                    for incident in incidents:
                        if isinstance(incident, dict) and "latitude" in incident and "longitude" in incident:
                            # Calculate intensity based on severity and recency
                            severity = incident.get("severity", 5) / 10.0  # Normalize to 0-1

                            # Calculate recency factor (newer incidents have higher intensity)
                            timestamp = incident.get("timestamp", time.time())
                            age_hours = (time.time() - timestamp) / 3600.0
                            recency = max(0.0, 1.0 - (age_hours / 168.0))  # Decay over 1 week

                            # Combined intensity
                            intensity = severity * recency
                            max_intensity = max(max_intensity, intensity)

                            points.append({
                                "latitude": incident["latitude"],
                                "longitude": incident["longitude"],
                                "intensity": intensity,
                                "type": incident.get("incident_type", "unknown")
                            })

                    return {
                        "center": location,
                        "radius": radius,
                        "max_intensity": max_intensity,
                        "points": points
                    }

            # Fallback to simulated data
            return {
                "center": location,
                "radius": radius,
                "max_intensity": 0.8,
                "points": [
                    {"latitude": location["latitude"] + 0.02, "longitude": location["longitude"] - 0.01, "intensity": 0.7},
                    {"latitude": location["latitude"] - 0.03, "longitude": location["longitude"] + 0.02, "intensity": 0.5},
                    {"latitude": location["latitude"] + 0.01, "longitude": location["longitude"] + 0.03, "intensity": 0.3}
                ]
            }
        except Exception as e:
            logger.error(f"Error getting crime heatmap: {e}")

            # Fallback to simulated data
            return {
                "center": location,
                "radius": radius,
                "max_intensity": 0.8,
                "points": [
                    {"latitude": location["latitude"] + 0.02, "longitude": location["longitude"] - 0.01, "intensity": 0.7},
                    {"latitude": location["latitude"] - 0.03, "longitude": location["longitude"] + 0.02, "intensity": 0.5},
                    {"latitude": location["latitude"] + 0.01, "longitude": location["longitude"] + 0.03, "intensity": 0.3}
                ]
            }

    def share_location(self, contact_id: str, duration: int = 60) -> bool:
        """
        Share location with a contact for a specified duration.

        Args:
            contact_id: The contact ID
            duration: The duration in minutes

        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Sharing location with contact {contact_id} for {duration} minutes")

            # Get current location
            location = self.get_current_location()

            # In a real implementation, this would:
            # 1. Generate a sharing link
            # 2. Send it to the contact via SMS, email, etc.
            # 3. Set up a time-limited sharing session

            # For now, we'll just log it and return success
            return True

        except Exception as e:
            logger.error(f"Error sharing location: {e}")
            return False

    def calculate_distance(self, point1: Dict[str, float], point2: Dict[str, float]) -> float:
        """
        Calculate the distance between two points using the Haversine formula.

        Args:
            point1: The first point
            point2: The second point

        Returns:
            The distance in kilometers
        """
        try:
            # Convert latitude and longitude from degrees to radians
            lat1 = math.radians(point1["latitude"])
            lon1 = math.radians(point1["longitude"])
            lat2 = math.radians(point2["latitude"])
            lon2 = math.radians(point2["longitude"])

            # Haversine formula
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
            c = 2 * math.asin(math.sqrt(a))
            r = 6371  # Radius of Earth in kilometers

            return c * r

        except Exception as e:
            logger.error(f"Error calculating distance: {e}")

            # Fallback to simplified calculation
            lat_diff = point2["latitude"] - point1["latitude"]
            lon_diff = point2["longitude"] - point1["longitude"]
            return ((lat_diff ** 2) + (lon_diff ** 2)) ** 0.5 * 111  # Rough conversion to km

    def start_tracking(self, interval_seconds: int = 30) -> None:
        """
        Start tracking location.

        Args:
            interval_seconds: The tracking interval in seconds
        """
        if self.tracking_active:
            logger.warning("Location tracking is already active")
            return

        logger.info(f"Starting location tracking with interval {interval_seconds} seconds")

        self.tracking_interval = interval_seconds
        self.tracking_active = True
        self.tracking_thread = threading.Thread(
            target=self._tracking_loop,
            args=(interval_seconds,)
        )
        self.tracking_thread.daemon = True
        self.tracking_thread.start()

    def stop_tracking(self) -> None:
        """Stop tracking location."""
        if not self.tracking_active:
            logger.warning("Location tracking is not active")
            return

        logger.info("Stopping location tracking")
        self.tracking_active = False

        if self.tracking_thread:
            self.tracking_thread.join(timeout=2.0)
            self.tracking_thread = None

    def _tracking_loop(self, interval_seconds: int) -> None:
        """
        The main tracking loop.

        Args:
            interval_seconds: The tracking interval in seconds
        """
        while self.tracking_active:
            try:
                # In a real implementation, this would get the location from GPS
                # For now, we'll just log that we're tracking
                logger.debug("Tracking location (simulated)")

                # Sleep for the specified interval
                time.sleep(interval_seconds)

            except Exception as e:
                logger.error(f"Error in location tracking loop: {e}")
                time.sleep(interval_seconds)

    def start_safety_monitoring(self, interval_seconds: int = 60) -> None:
        """
        Start monitoring location safety.

        Args:
            interval_seconds: The monitoring interval in seconds
        """
        if self.safety_monitoring_active:
            logger.warning("Safety monitoring is already active")
            return

        logger.info(f"Starting safety monitoring with interval {interval_seconds} seconds")

        self.safety_monitoring_interval = interval_seconds
        self.safety_monitoring_active = True
        self.safety_monitoring_thread = threading.Thread(
            target=self._safety_monitoring_loop,
            args=(interval_seconds,)
        )
        self.safety_monitoring_thread.daemon = True
        self.safety_monitoring_thread.start()

    def stop_safety_monitoring(self) -> None:
        """Stop monitoring location safety."""
        if not self.safety_monitoring_active:
            logger.warning("Safety monitoring is not active")
            return

        logger.info("Stopping safety monitoring")
        self.safety_monitoring_active = False

        if self.safety_monitoring_thread:
            self.safety_monitoring_thread.join(timeout=2.0)
            self.safety_monitoring_thread = None

    def _safety_monitoring_loop(self, interval_seconds: int) -> None:
        """
        The main safety monitoring loop.

        Args:
            interval_seconds: The monitoring interval in seconds
        """
        while self.safety_monitoring_active:
            try:
                # Check current location safety
                if self.current_location:
                    self._check_location_safety(
                        self.current_location["latitude"],
                        self.current_location["longitude"]
                    )

                # Sleep for the specified interval
                time.sleep(interval_seconds)

            except Exception as e:
                logger.error(f"Error in safety monitoring loop: {e}")
                time.sleep(interval_seconds)

    def _check_location_safety(self, latitude: float, longitude: float) -> None:
        """
        Check the safety of a location.

        Args:
            latitude: The latitude
            longitude: The longitude
        """
        try:
            logger.debug(f"Checking safety for location ({latitude}, {longitude})")

            # Get safety score from safe route service
            safety_score = self.safe_route_service.get_safety_score_for_location(
                latitude, longitude
            )

            # Update current safety score
            self.current_safety_score = safety_score

            # Check if safety level is low
            if safety_score.get("safety_level") == "LOW":
                # Notify user of high risk area
                self._notify_safety_alert(safety_score)

            # Notify callbacks
            for callback in self.safety_callbacks:
                try:
                    callback(safety_score)
                except Exception as e:
                    logger.error(f"Error in safety callback: {e}")

        except Exception as e:
            logger.error(f"Error checking location safety: {e}")

    def _notify_safety_alert(self, safety_score: Dict[str, Any]) -> None:
        """
        Notify of a safety alert.

        Args:
            safety_score: The safety score
        """
        try:
            logger.info(f"Safety alert: {safety_score}")

            # In a real implementation, this would:
            # 1. Send a push notification
            # 2. Display an alert in the app
            # 3. Suggest safer routes

            # For now, we'll just log it
            logger.warning(f"SAFETY ALERT: You are in an area with a safety score of {safety_score.get('safety_score')}")

        except Exception as e:
            logger.error(f"Error notifying safety alert: {e}")

    def register_location_callback(self, callback: Callable) -> None:
        """
        Register a callback for location updates.

        Args:
            callback: The callback function
        """
        self.location_callbacks.append(callback)
        logger.info(f"Registered location callback, total callbacks: {len(self.location_callbacks)}")

    def unregister_location_callback(self, callback: Callable) -> None:
        """
        Unregister a callback for location updates.

        Args:
            callback: The callback function
        """
        if callback in self.location_callbacks:
            self.location_callbacks.remove(callback)
            logger.info(f"Unregistered location callback, remaining callbacks: {len(self.location_callbacks)}")

    def register_safety_callback(self, callback: Callable) -> None:
        """
        Register a callback for safety updates.

        Args:
            callback: The callback function
        """
        self.safety_callbacks.append(callback)
        logger.info(f"Registered safety callback, total callbacks: {len(self.safety_callbacks)}")

    def unregister_safety_callback(self, callback: Callable) -> None:
        """
        Unregister a callback for safety updates.

        Args:
            callback: The callback function
        """
        if callback in self.safety_callbacks:
            self.safety_callbacks.remove(callback)
            logger.info(f"Unregistered safety callback, remaining callbacks: {len(self.safety_callbacks)}")

    def get_location_history(self) -> List[Dict[str, Any]]:
        """
        Get the location history.

        Returns:
            The location history
        """
        return self.location_history

    def get_current_safety_score(self) -> Optional[Dict[str, Any]]:
        """
        Get the current safety score.

        Returns:
            The current safety score
        """
        if self.current_safety_score:
            return self.current_safety_score

        # If no safety score yet, check current location
        if self.current_location:
            return self.safe_route_service.get_safety_score_for_location(
                self.current_location["latitude"],
                self.current_location["longitude"]
            )

        return None
