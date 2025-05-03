"""
UI integration service for SafeWayAI application.
This module provides functionality to integrate Azure services with the Flet UI.
"""

import logging
import threading
import time
import flet as ft
from app.services.service_manager import ServiceManager
from app.services.location_service import LocationService
from app.services.safe_route_service import SafeRouteService
from app.services.incident_service import IncidentService
from app.services.emergency_detection import EmergencyDetectionService

logger = logging.getLogger(__name__)

class UIIntegrationService:
    """Service for integrating Azure services with the Flet UI."""
    
    _instance = None
    
    def __new__(cls):
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super(UIIntegrationService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the UI integration service."""
        if self._initialized:
            return
            
        logger.info("Initializing UI integration service")
        
        # Get services
        self.service_manager = ServiceManager()
        self.location_service = LocationService()
        self.safe_route_service = SafeRouteService()
        self.incident_service = IncidentService()
        self.emergency_detection = EmergencyDetectionService()
        
        # Initialize state
        self.page = None
        self.safety_status_controls = []
        self.incident_list_controls = []
        self.route_map_controls = []
        self.emergency_alert_controls = []
        
        # Register callbacks
        self.location_service.register_safety_callback(self._on_safety_update)
        self.emergency_detection.register_emergency_callback(self._on_emergency_detected)
        
        self._initialized = True
    
    def set_page(self, page):
        """
        Set the Flet page.
        
        Args:
            page: The Flet page
        """
        self.page = page
    
    def register_safety_status_control(self, control):
        """
        Register a control for safety status updates.
        
        Args:
            control: The control to update
        """
        self.safety_status_controls.append(control)
    
    def register_incident_list_control(self, control):
        """
        Register a control for incident list updates.
        
        Args:
            control: The control to update
        """
        self.incident_list_controls.append(control)
    
    def register_route_map_control(self, control):
        """
        Register a control for route map updates.
        
        Args:
            control: The control to update
        """
        self.route_map_controls.append(control)
    
    def register_emergency_alert_control(self, control):
        """
        Register a control for emergency alert updates.
        
        Args:
            control: The control to update
        """
        self.emergency_alert_controls.append(control)
    
    def _on_safety_update(self, safety_score):
        """
        Handle safety updates.
        
        Args:
            safety_score: The safety score
        """
        try:
            logger.info(f"Safety update: {safety_score}")
            
            # Update safety status controls
            for control in self.safety_status_controls:
                try:
                    self._update_safety_status_control(control, safety_score)
                except Exception as e:
                    logger.error(f"Error updating safety status control: {e}")
            
            # Update the page
            if self.page:
                self.page.update()
                
        except Exception as e:
            logger.error(f"Error handling safety update: {e}")
    
    def _update_safety_status_control(self, control, safety_score):
        """
        Update a safety status control.
        
        Args:
            control: The control to update
            safety_score: The safety score
        """
        try:
            # Get safety level and score
            safety_level = safety_score.get("safety_level", "UNKNOWN")
            score = safety_score.get("safety_score", 0)
            
            # Set color based on safety level
            if safety_level == "HIGH":
                color = ft.colors.GREEN
                icon = ft.icons.SHIELD
                message = "You are in a safe area"
            elif safety_level == "MODERATE":
                color = ft.colors.ORANGE
                icon = ft.icons.SHIELD_OUTLINED
                message = "Exercise caution in this area"
            elif safety_level == "LOW":
                color = ft.colors.RED
                icon = ft.icons.WARNING_AMBER_ROUNDED
                message = "High risk area - stay alert"
            else:
                color = ft.colors.BLUE_GREY
                icon = ft.icons.HELP_OUTLINE
                message = "Safety information unavailable"
            
            # Update the control
            if hasattr(control, "bgcolor"):
                control.bgcolor = color
            
            if hasattr(control, "icon"):
                control.icon = icon
            
            if hasattr(control, "text"):
                control.text = message
            
            if hasattr(control, "value"):
                control.value = score
            
        except Exception as e:
            logger.error(f"Error updating safety status control: {e}")
    
    def _on_emergency_detected(self, emergency_data):
        """
        Handle emergency detection.
        
        Args:
            emergency_data: The emergency data
        """
        try:
            logger.info(f"Emergency detected: {emergency_data}")
            
            # Update emergency alert controls
            for control in self.emergency_alert_controls:
                try:
                    self._update_emergency_alert_control(control, emergency_data)
                except Exception as e:
                    logger.error(f"Error updating emergency alert control: {e}")
            
            # Update the page
            if self.page:
                self.page.update()
                
        except Exception as e:
            logger.error(f"Error handling emergency detection: {e}")
    
    def _update_emergency_alert_control(self, control, emergency_data):
        """
        Update an emergency alert control.
        
        Args:
            control: The control to update
            emergency_data: The emergency data
        """
        try:
            # Get emergency type and confidence
            emergency_type = emergency_data.get("type", "unknown")
            confidence = emergency_data.get("confidence", 0)
            
            # Create alert message
            if emergency_type == "audio_emergency":
                message = "Emergency detected in audio"
            elif emergency_type == "image_emergency":
                message = "Emergency detected in image"
            elif emergency_type == "manual_emergency":
                message = "Emergency reported manually"
            else:
                message = f"Emergency detected: {emergency_type}"
            
            # Add confidence if available
            if confidence > 0:
                message += f" (Confidence: {confidence:.0%})"
            
            # Update the control
            if hasattr(control, "text"):
                control.text = message
            
            if hasattr(control, "visible"):
                control.visible = True
            
            if hasattr(control, "bgcolor"):
                control.bgcolor = ft.colors.RED
            
        except Exception as e:
            logger.error(f"Error updating emergency alert control: {e}")
    
    def update_incident_list(self):
        """Update the incident list controls."""
        try:
            # Get recent incidents
            incidents = self.incident_service.get_recent_incidents(max_incidents=10)
            
            # Update incident list controls
            for control in self.incident_list_controls:
                try:
                    self._update_incident_list_control(control, incidents)
                except Exception as e:
                    logger.error(f"Error updating incident list control: {e}")
            
            # Update the page
            if self.page:
                self.page.update()
                
        except Exception as e:
            logger.error(f"Error updating incident list: {e}")
    
    def _update_incident_list_control(self, control, incidents):
        """
        Update an incident list control.
        
        Args:
            control: The control to update
            incidents: The incidents
        """
        try:
            # Clear the control
            if hasattr(control, "controls") and hasattr(control, "clear"):
                control.clear()
                
                # Add incidents
                if isinstance(incidents, list):
                    for incident in incidents:
                        if isinstance(incident, dict):
                            # Create incident item
                            incident_type = incident.get("incident_type", "Unknown")
                            severity = incident.get("severity", 0)
                            status = incident.get("status", "Unknown")
                            timestamp = incident.get("timestamp", 0)
                            
                            # Format timestamp
                            if timestamp > 0:
                                time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
                            else:
                                time_str = "Unknown time"
                            
                            # Set color based on severity
                            if severity >= 8:
                                color = ft.colors.RED
                            elif severity >= 5:
                                color = ft.colors.ORANGE
                            else:
                                color = ft.colors.YELLOW
                            
                            # Create item
                            item = ft.Container(
                                content=ft.Column([
                                    ft.Row([
                                        ft.Icon(
                                            name=ft.icons.WARNING_AMBER_ROUNDED,
                                            color=color
                                        ),
                                        ft.Text(
                                            value=f"{incident_type} - {status}",
                                            weight=ft.FontWeight.BOLD
                                        )
                                    ]),
                                    ft.Text(
                                        value=incident.get("description", "No description"),
                                        size=14
                                    ),
                                    ft.Text(
                                        value=time_str,
                                        size=12,
                                        color=ft.colors.GREY
                                    )
                                ]),
                                padding=10,
                                margin=ft.margin.only(bottom=5),
                                border=ft.border.all(1, ft.colors.GREY_300),
                                border_radius=5
                            )
                            
                            # Add to control
                            control.controls.append(item)
            
        except Exception as e:
            logger.error(f"Error updating incident list control: {e}")
    
    def update_route_map(self, start_point, end_point):
        """
        Update the route map controls.
        
        Args:
            start_point: The starting point
            end_point: The ending point
        """
        try:
            # Get safe route
            route = self.location_service.get_safe_route(start_point, end_point)
            
            # Update route map controls
            for control in self.route_map_controls:
                try:
                    self._update_route_map_control(control, route)
                except Exception as e:
                    logger.error(f"Error updating route map control: {e}")
            
            # Update the page
            if self.page:
                self.page.update()
                
            return route
            
        except Exception as e:
            logger.error(f"Error updating route map: {e}")
            return None
    
    def _update_route_map_control(self, control, route):
        """
        Update a route map control.
        
        Args:
            control: The control to update
            route: The route
        """
        try:
            # This would typically update a map control with the route
            # For now, we'll just update text information
            
            if hasattr(control, "content") and isinstance(control.content, ft.Column):
                # Clear the column
                control.content.controls.clear()
                
                # Add route information
                control.content.controls.append(
                    ft.Text(
                        value=f"Distance: {route.get('distance', 0):.1f} km",
                        weight=ft.FontWeight.BOLD,
                        size=16
                    )
                )
                
                control.content.controls.append(
                    ft.Text(
                        value=f"Duration: {route.get('duration', 0):.0f} minutes",
                        size=16
                    )
                )
                
                control.content.controls.append(
                    ft.Text(
                        value=f"Safety Score: {route.get('safety_score', 0):.0f}/100",
                        size=16
                    )
                )
                
                # Add safety notes if available
                if "safetyNotes" in route:
                    notes_column = ft.Column(
                        controls=[
                            ft.Text(
                                value="Safety Notes:",
                                weight=ft.FontWeight.BOLD,
                                size=14
                            )
                        ]
                    )
                    
                    for note in route["safetyNotes"]:
                        notes_column.controls.append(
                            ft.Text(
                                value=f"• {note}",
                                size=14
                            )
                        )
                    
                    control.content.controls.append(notes_column)
            
        except Exception as e:
            logger.error(f"Error updating route map control: {e}")
    
    def report_incident(self, incident_data):
        """
        Report an incident.
        
        Args:
            incident_data: The incident data
            
        Returns:
            The created incident
        """
        try:
            # Report the incident
            result = self.incident_service.report_incident(incident_data)
            
            # Update incident list
            self.update_incident_list()
            
            return result
            
        except Exception as e:
            logger.error(f"Error reporting incident: {e}")
            return {"error": str(e)}
    
    def report_emergency(self, emergency_data):
        """
        Report an emergency.
        
        Args:
            emergency_data: The emergency data
            
        Returns:
            The result of reporting the emergency
        """
        try:
            # Report the emergency
            result = self.emergency_detection.report_emergency(emergency_data)
            
            return result
            
        except Exception as e:
            logger.error(f"Error reporting emergency: {e}")
            return {"error": str(e)}
    
    def get_nearby_safe_places(self):
        """
        Get nearby safe places.
        
        Returns:
            List of nearby safe places
        """
        try:
            # Get current location
            location = self.location_service.get_current_location()
            
            # Get nearby safe places
            return self.location_service.get_nearby_safe_places(location)
            
        except Exception as e:
            logger.error(f"Error getting nearby safe places: {e}")
            return []
    
    def get_crime_heatmap(self):
        """
        Get crime heatmap data.
        
        Returns:
            Crime heatmap data
        """
        try:
            # Get current location
            location = self.location_service.get_current_location()
            
            # Get crime heatmap
            return self.location_service.get_crime_heatmap(location)
            
        except Exception as e:
            logger.error(f"Error getting crime heatmap: {e}")
            return None
    
    def start_safety_monitoring(self):
        """Start safety monitoring."""
        try:
            self.location_service.start_safety_monitoring()
        except Exception as e:
            logger.error(f"Error starting safety monitoring: {e}")
    
    def stop_safety_monitoring(self):
        """Stop safety monitoring."""
        try:
            self.location_service.stop_safety_monitoring()
        except Exception as e:
            logger.error(f"Error stopping safety monitoring: {e}")
    
    def start_emergency_monitoring(self):
        """Start emergency monitoring."""
        try:
            self.emergency_detection.start_monitoring()
        except Exception as e:
            logger.error(f"Error starting emergency monitoring: {e}")
    
    def stop_emergency_monitoring(self):
        """Stop emergency monitoring."""
        try:
            self.emergency_detection.stop_monitoring()
        except Exception as e:
            logger.error(f"Error stopping emergency monitoring: {e}")
    
    def share_location(self, contact_id, duration=60):
        """
        Share location with a contact.
        
        Args:
            contact_id: The contact ID
            duration: The duration in minutes
            
        Returns:
            True if successful, False otherwise
        """
        try:
            return self.location_service.share_location(contact_id, duration)
        except Exception as e:
            logger.error(f"Error sharing location: {e}")
            return False
