"""
Live Tracking Component for SafeWayAI application.
This module provides real-time location tracking visualization.
"""

import flet as ft
import logging
import time
import random
from app.utils.enhanced_theme import get_color_scheme

colors = get_color_scheme()
logger = logging.getLogger(__name__)

class LiveTracking(ft.Container):
    """Live tracking component with real-time visualization."""
    
    def __init__(self, 
                 route=None, 
                 width=None, 
                 height=None,
                 on_stop=None,
                 on_sos=None,
                 on_share=None):
        """
        Initialize the live tracking component.
        
        Args:
            route (dict): Route data dictionary
            width (int, optional): Component width
            height (int, optional): Component height
            on_stop (function, optional): Callback when tracking is stopped
            on_sos (function, optional): Callback when SOS is triggered
            on_share (function, optional): Callback when route is shared
        """
        self.route = route or {}
        self.on_stop = on_stop
        self.on_sos = on_sos
        self.on_share = on_share
        
        # Tracking state
        self.is_tracking = False
        self.current_position = 0
        self.route_points = self.route.get("route_points", [])
        self.tracking_id = None
        self.alerts = []
        self.eta_minutes = self.route.get("duration_min", 0)
        self.distance_remaining = self.route.get("distance_km", 0)
        
        # Create the header
        header = ft.Row(
            controls=[
                ft.Text(
                    value="Live Navigation",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Container(
                    content=ft.Text(
                        value="LIVE",
                        size=12,
                        color=ft.colors.WHITE,
                        weight=ft.FontWeight.BOLD,
                    ),
                    bgcolor=colors["danger"],
                    border_radius=5,
                    padding=ft.padding.only(left=8, top=4, right=8, bottom=4),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        
        # Create the status display
        self.status_display = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(
                                name="schedule",
                                color=colors["primary"],
                                size=20,
                            ),
                            ft.Text(
                                value=f"ETA: {self.eta_minutes} min",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                        spacing=5,
                    ),
                    ft.Row(
                        controls=[
                            ft.Icon(
                                name="straighten",
                                color=colors["primary"],
                                size=20,
                            ),
                            ft.Text(
                                value=f"Distance remaining: {self.distance_remaining:.1f} km",
                                size=16,
                            ),
                        ],
                        spacing=5,
                    ),
                    ft.Row(
                        controls=[
                            ft.Icon(
                                name="shield",
                                color=self._get_safety_color(self.route.get("safety_score", 0)),
                                size=20,
                            ),
                            ft.Text(
                                value=f"Current area safety: {self.route.get('safety_score', 0)}/100",
                                size=16,
                            ),
                        ],
                        spacing=5,
                    ),
                ],
                spacing=10,
            ),
            padding=10,
            border_radius=10,
            bgcolor=ft.colors.BLUE_50,
        )
        
        # Create the map placeholder
        self.map_placeholder = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(
                        name="map",
                        size=50,
                        color=colors["primary"],
                    ),
                    ft.Text(
                        value="Live tracking map would display here",
                        color=ft.colors.BLACK,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        value="Using Azure Maps for visualization",
                        color=ft.colors.GREY_700,
                        size=12,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            alignment=ft.alignment.center,
            bgcolor=ft.colors.BLUE_50,
            border_radius=10,
            padding=20,
            width=width,
            height=200,
        )
        
        # Create the alerts section
        self.alerts_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        value="Safety Alerts",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        value="No alerts - You're on a safe path",
                        size=14,
                        italic=True,
                    ),
                ],
                spacing=5,
            ),
            padding=10,
            border_radius=10,
            bgcolor=ft.colors.BLUE_50,
        )
        
        # Create the action buttons
        action_buttons = ft.Row(
            controls=[
                ft.ElevatedButton(
                    text="Stop Navigation",
                    icon="stop",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        color=ft.colors.WHITE,
                        bgcolor=colors["primary"],
                    ),
                    on_click=self._handle_stop,
                ),
                ft.ElevatedButton(
                    text="Emergency SOS",
                    icon="emergency",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        color=ft.colors.WHITE,
                        bgcolor=colors["danger"],
                    ),
                    on_click=self._handle_sos,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        
        # Create the share journey section
        share_journey = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        value="Share Your Journey",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        value="Let trusted contacts know where you are",
                        size=14,
                    ),
                    ft.Row(
                        controls=[
                            ft.TextField(
                                hint_text="Enter phone number or email",
                                expand=True,
                            ),
                            ft.IconButton(
                                icon="send",
                                tooltip="Share journey",
                                icon_color=colors["primary"],
                                on_click=self._handle_share,
                            ),
                        ],
                    ),
                ],
                spacing=5,
            ),
            padding=10,
            border_radius=10,
            bgcolor=ft.colors.BLUE_50,
        )
        
        # Create the main content
        content = ft.Column(
            controls=[
                header,
                self.status_display,
                self.map_placeholder,
                self.alerts_container,
                action_buttons,
                share_journey,
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
        )
        
        # Initialize the container
        super().__init__(
            content=content,
            width=width,
            height=height,
            border_radius=10,
            bgcolor=ft.colors.WHITE,
            padding=15,
            border=ft.border.all(1, ft.colors.GREY_400),
        )
    
    def _handle_stop(self, e):
        """Handle stop navigation button click."""
        self.is_tracking = False
        if self.on_stop:
            self.on_stop(e)
    
    def _handle_sos(self, e):
        """Handle SOS button click."""
        if self.on_sos:
            self.on_sos(e)
    
    def _handle_share(self, e):
        """Handle share journey button click."""
        if self.on_share:
            self.on_share(e)
    
    def _get_safety_color(self, score):
        """Get color based on safety score."""
        if score >= 85:
            return colors["safety_high"]
        elif score >= 70:
            return colors["safety_medium"]
        elif score >= 50:
            return colors["warning"]
        else:
            return colors["danger"]
    
    def start_tracking(self, tracking_id=None):
        """
        Start live tracking.
        
        Args:
            tracking_id (str, optional): Tracking session ID
        
        Returns:
            bool: Success status
        """
        if not self.route_points:
            logger.warning("Cannot start tracking: No route points available")
            return False
        
        self.is_tracking = True
        self.current_position = 0
        self.tracking_id = tracking_id or f"track_{int(time.time())}"
        self.alerts = []
        
        # Update UI
        self._update_tracking_display()
        
        logger.info(f"Started live tracking with ID: {self.tracking_id}")
        return True
    
    def stop_tracking(self):
        """
        Stop live tracking.
        
        Returns:
            bool: Success status
        """
        if not self.is_tracking:
            return False
        
        self.is_tracking = False
        
        # Update UI
        self._update_tracking_display()
        
        logger.info(f"Stopped live tracking: {self.tracking_id}")
        return True
    
    def update_position(self, position_index=None, latitude=None, longitude=None):
        """
        Update current position.
        
        Args:
            position_index (int, optional): Index in route_points
            latitude (float, optional): Current latitude
            longitude (float, optional): Current longitude
            
        Returns:
            bool: Success status
        """
        if not self.is_tracking:
            return False
        
        if position_index is not None:
            self.current_position = min(position_index, len(self.route_points) - 1)
        elif latitude is not None and longitude is not None:
            # Find closest point on route
            # In a real implementation, this would use proper distance calculation
            # For now, we'll just increment the position
            self.current_position = min(self.current_position + 1, len(self.route_points) - 1)
        else:
            # Simulate movement along the route
            self.current_position = min(self.current_position + 1, len(self.route_points) - 1)
        
        # Update remaining distance and ETA
        progress = self.current_position / max(1, len(self.route_points) - 1)
        self.distance_remaining = self.route.get("distance_km", 0) * (1 - progress)
        self.eta_minutes = int(self.route.get("duration_min", 0) * (1 - progress))
        
        # Update UI
        self._update_tracking_display()
        
        # Check if we've reached the destination
        if self.current_position >= len(self.route_points) - 1:
            logger.info(f"Reached destination: {self.tracking_id}")
            self.is_tracking = False
            return False
        
        return True
    
    def add_alert(self, alert_text, alert_level="info"):
        """
        Add a safety alert.
        
        Args:
            alert_text (str): Alert message
            alert_level (str): Alert level (info, warning, danger)
            
        Returns:
            bool: Success status
        """
        if not self.is_tracking:
            return False
        
        # Add alert to list
        self.alerts.append({
            "text": alert_text,
            "level": alert_level,
            "time": time.time(),
        })
        
        # Update UI
        self._update_alerts_display()
        
        return True
    
    def _update_tracking_display(self):
        """Update the tracking display with current information."""
        if not self.is_tracking:
            # Reset display
            self.status_display.content = ft.Column(
                controls=[
                    ft.Text(
                        value="Navigation Stopped",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        value="Start navigation to track your journey",
                        size=14,
                    ),
                ],
                spacing=10,
            )
        else:
            # Update status display
            self.status_display.content = ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(
                                name="schedule",
                                color=colors["primary"],
                                size=20,
                            ),
                            ft.Text(
                                value=f"ETA: {self.eta_minutes} min",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                        spacing=5,
                    ),
                    ft.Row(
                        controls=[
                            ft.Icon(
                                name="straighten",
                                color=colors["primary"],
                                size=20,
                            ),
                            ft.Text(
                                value=f"Distance remaining: {self.distance_remaining:.1f} km",
                                size=16,
                            ),
                        ],
                        spacing=5,
                    ),
                    ft.Row(
                        controls=[
                            ft.Icon(
                                name="shield",
                                color=self._get_safety_color(self.route.get("safety_score", 0)),
                                size=20,
                            ),
                            ft.Text(
                                value=f"Current area safety: {self.route.get('safety_score', 0)}/100",
                                size=16,
                            ),
                        ],
                        spacing=5,
                    ),
                    ft.ProgressBar(
                        width=None,
                        value=self.current_position / max(1, len(self.route_points) - 1),
                        color=colors["primary"],
                        bgcolor=ft.colors.GREY_300,
                    ),
                ],
                spacing=10,
            )
            
            # Update map placeholder
            progress = self.current_position / max(1, len(self.route_points) - 1)
            self.map_placeholder.content = ft.Column(
                controls=[
                    ft.Icon(
                        name="navigation",
                        size=50,
                        color=colors["primary"],
                    ),
                    ft.Text(
                        value=f"Currently at {int(progress * 100)}% of your journey",
                        color=ft.colors.BLACK,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        value=f"Tracking ID: {self.tracking_id}",
                        color=ft.colors.GREY_700,
                        size=12,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            )
        
        self.update()
    
    def _update_alerts_display(self):
        """Update the alerts display with current alerts."""
        if not self.alerts:
            self.alerts_container.content = ft.Column(
                controls=[
                    ft.Text(
                        value="Safety Alerts",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        value="No alerts - You're on a safe path",
                        size=14,
                        italic=True,
                    ),
                ],
                spacing=5,
            )
        else:
            alert_controls = [
                ft.Text(
                    value="Safety Alerts",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                )
            ]
            
            for alert in self.alerts:
                # Determine icon and color based on alert level
                if alert["level"] == "danger":
                    icon_name = "warning"
                    icon_color = colors["danger"]
                elif alert["level"] == "warning":
                    icon_name = "warning"
                    icon_color = colors["warning"]
                else:
                    icon_name = "info"
                    icon_color = colors["primary"]
                
                alert_controls.append(
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Icon(
                                    name=icon_name,
                                    color=icon_color,
                                    size=16,
                                ),
                                ft.Text(
                                    value=alert["text"],
                                    size=14,
                                ),
                            ],
                            spacing=10,
                        ),
                        padding=5,
                        border_radius=5,
                        bgcolor=ft.colors.with_opacity(0.1, icon_color),
                    )
                )
            
            self.alerts_container.content = ft.Column(
                controls=alert_controls,
                spacing=5,
            )
        
        self.update()
