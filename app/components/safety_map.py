"""
Safety Map Component for SafeWayAI application.
This module provides an interactive map with safety visualization.
"""

import flet as ft
import logging
import json
import time
import random
from app.utils.enhanced_theme import get_color_scheme

colors = get_color_scheme()
logger = logging.getLogger(__name__)

class SafetyMap(ft.Column):
    """Interactive map component with safety visualization."""

    def __init__(self,
                 width=None,
                 height=300,
                 on_map_click=None,
                 on_map_ready=None,
                 api_key=None):
        """
        Initialize the safety map component.

        Args:
            width (int, optional): Map width
            height (int, optional): Map height
            on_map_click (function, optional): Callback for map clicks
            on_map_ready (function, optional): Callback when map is ready
            api_key (str, optional): Azure Maps API key
        """
        super().__init__(spacing=5)

        # Map state
        self.width = width
        self.height = height
        self.on_map_click = on_map_click
        self.on_map_ready = on_map_ready
        self.api_key = api_key

        # Map state
        self.map_ready = False
        self.center_lat = -26.2041  # Default to Johannesburg
        self.center_lon = 28.0473
        self.zoom_level = 12
        self.map_type = "road"  # road, satellite, hybrid
        self.routes = []
        self.markers = []
        self.safety_overlay = None

        # Generate a unique ID for this map instance
        self.map_id = f"safety_map_{int(time.time() * 1000)}"

        # Create loading indicator
        self.loading_indicator = ft.ProgressRing(
            width=40,
            height=40,
            stroke_width=4,
            color=colors["primary"]
        )

        # Create map placeholder (shown when web view is not available)
        self.map_placeholder = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(
                        name="map",
                        size=50,
                        color=colors["primary"],
                    ),
                    ft.Text(
                        value="Interactive map would display here",
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
            width=self.width,
            height=self.height,
        )

        # Create map controls
        self.map_controls = ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.icons.ZOOM_IN,
                    tooltip="Zoom in",
                    icon_color=colors["primary"],
                    on_click=self._zoom_in,
                ),
                ft.IconButton(
                    icon=ft.icons.ZOOM_OUT,
                    tooltip="Zoom out",
                    icon_color=colors["primary"],
                    on_click=self._zoom_out,
                ),
                ft.IconButton(
                    icon=ft.icons.LAYERS,
                    tooltip="Change map type",
                    icon_color=colors["primary"],
                    on_click=self._toggle_map_type,
                ),
                ft.IconButton(
                    icon=ft.icons.SHIELD,
                    tooltip="Toggle safety overlay",
                    icon_color=colors["primary"],
                    on_click=self._toggle_safety_overlay,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        # In a real implementation, we would use a WebView to display the map
        # For now, we'll use a simulated map with a Container that visually shows the route
        self.map_container = ft.Container(
            content=self.map_placeholder,
            width=self.width,
            height=self.height,
            border_radius=10,
            border=ft.border.all(1, ft.colors.GREY_400),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        )

        # Add controls to the column
        self.controls = [
            self.map_container,
            self.map_controls,
        ]

    def _zoom_in(self, e=None):
        """Zoom in on the map."""
        self.zoom_level = min(20, self.zoom_level + 1)
        self._update_map()

    def _zoom_out(self, e=None):
        """Zoom out on the map."""
        self.zoom_level = max(1, self.zoom_level - 1)
        self._update_map()

    def _toggle_map_type(self, e=None):
        """Toggle between map types."""
        if self.map_type == "road":
            self.map_type = "satellite"
        elif self.map_type == "satellite":
            self.map_type = "hybrid"
        else:
            self.map_type = "road"

        self._update_map()

    def _toggle_safety_overlay(self, e=None):
        """Toggle the safety overlay on the map."""
        if self.safety_overlay:
            self.safety_overlay = None
        else:
            self.safety_overlay = "heatmap"  # or "grid"

        self._update_map()

    def _update_map(self):
        """Update the map with current settings."""
        # In a real implementation, this would update the WebView
        # For now, we'll update the placeholder with a visual representation

        # Update the map placeholder to reflect current state
        map_type_display = {
            "road": "Road Map",
            "satellite": "Satellite Map",
            "hybrid": "Hybrid Map"
        }.get(self.map_type, "Road Map")

        safety_overlay_display = "Enabled" if self.safety_overlay else "Disabled"

        # Create a stack for the map visualization
        map_stack_controls = [
            # Base map background
            ft.Container(
                bgcolor=ft.colors.BLUE_50,
                border_radius=10,
                width=None,
                height=None,
                expand=True,
            )
        ]

        # Add routes to the visualization
        for route in self.routes:
            # Create a visual representation of the route
            route_color = route.get("color", colors["primary"])
            route_width = route.get("width", 4)

            # Create a container to represent the route
            route_container = ft.Container(
                bgcolor=route_color,
                width=None,
                height=route_width,
                border_radius=route_width/2,
                margin=ft.margin.only(top=100, bottom=100),  # Center vertically
                expand=True,
            )

            map_stack_controls.append(route_container)

        # Add markers to the visualization
        for marker in self.markers:
            marker_color = marker.get("color", colors["primary"])
            marker_icon = marker.get("icon", "location_on")
            marker_title = marker.get("title", "")

            # Create a container for the marker
            marker_container = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(
                            name=marker_icon,
                            color=marker_color,
                            size=24,
                        ),
                        ft.Text(
                            value=marker_title,
                            color=ft.colors.BLACK,
                            size=10,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=2,
                ),
                padding=5,
                border_radius=15,
                bgcolor=ft.colors.WHITE.with_opacity(0.8),
            )

            # Position the marker based on its index
            index = self.markers.index(marker)
            left_position = 20 + (index * 60) % (self.width or 300 - 40)

            # Add the marker to the stack with positioning
            map_stack_controls.append(
                ft.Container(
                    content=marker_container,
                    alignment=ft.alignment.center,
                    left=left_position,
                    top=80 + (index * 30) % 100,
                )
            )

        # Create the map info text
        map_info = ft.Column(
            controls=[
                ft.Text(
                    value=f"Interactive Map (Zoom: {self.zoom_level})",
                    color=ft.colors.BLACK,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    value=f"Type: {map_type_display} | Safety Overlay: {safety_overlay_display}",
                    color=ft.colors.GREY_700,
                    size=12,
                ),
                ft.Text(
                    value=f"Center: {self.center_lat:.4f}, {self.center_lon:.4f}",
                    color=ft.colors.GREY_700,
                    size=12,
                ),
                ft.Text(
                    value=f"Routes: {len(self.routes)} | Markers: {len(self.markers)}",
                    color=ft.colors.GREY_700,
                    size=12,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5,
        )

        # Add the info text to the top of the stack
        map_stack_controls.append(
            ft.Container(
                content=map_info,
                alignment=ft.alignment.top_center,
                padding=10,
            )
        )

        # Create the stack with all map elements
        map_stack = ft.Stack(
            controls=map_stack_controls,
            width=None,
            height=None,
            expand=True,
        )

        # Update the map placeholder with the stack
        self.map_placeholder.content = map_stack

        # Update the UI if the control is added to a page
        try:
            self.update()
        except AssertionError:
            # Control not added to page yet, that's okay
            pass

    def set_center(self, latitude, longitude, zoom=None):
        """
        Set the map center coordinates.

        Args:
            latitude (float): Latitude coordinate
            longitude (float): Longitude coordinate
            zoom (int, optional): Zoom level
        """
        self.center_lat = latitude
        self.center_lon = longitude
        if zoom is not None:
            self.zoom_level = zoom

        self._update_map()

    def add_marker(self, latitude, longitude, title=None, description=None, icon=None, color=None):
        """
        Add a marker to the map.

        Args:
            latitude (float): Marker latitude
            longitude (float): Marker longitude
            title (str, optional): Marker title
            description (str, optional): Marker description
            icon (str, optional): Marker icon
            color (str, optional): Marker color

        Returns:
            str: Marker ID
        """
        marker_id = f"marker_{len(self.markers)}"

        marker = {
            "id": marker_id,
            "latitude": latitude,
            "longitude": longitude,
            "title": title,
            "description": description,
            "icon": icon or "location_on",
            "color": color or colors["primary"],
        }

        self.markers.append(marker)
        self._update_map()

        return marker_id

    def remove_marker(self, marker_id):
        """
        Remove a marker from the map.

        Args:
            marker_id (str): Marker ID to remove

        Returns:
            bool: Success status
        """
        for i, marker in enumerate(self.markers):
            if marker["id"] == marker_id:
                self.markers.pop(i)
                self._update_map()
                return True

        return False

    def clear_markers(self):
        """Clear all markers from the map."""
        self.markers = []
        self._update_map()

    def add_route(self, route_points, color=None, width=None, safety_score=None):
        """
        Add a route to the map.

        Args:
            route_points (list): List of coordinates along the route
            color (str, optional): Route color
            width (int, optional): Route line width
            safety_score (int, optional): Route safety score (0-100)

        Returns:
            str: Route ID
        """
        route_id = f"route_{len(self.routes)}"

        # If safety score is provided, determine color based on score
        if safety_score is not None and color is None:
            if safety_score >= 85:
                color = colors["safety_high"]
            elif safety_score >= 70:
                color = colors["safety_medium"]
            elif safety_score >= 50:
                color = colors["warning"]
            else:
                color = colors["danger"]

        route = {
            "id": route_id,
            "points": route_points,
            "color": color or colors["primary"],
            "width": width or 4,
            "safety_score": safety_score,
        }

        self.routes.append(route)
        self._update_map()

        return route_id

    def remove_route(self, route_id):
        """
        Remove a route from the map.

        Args:
            route_id (str): Route ID to remove

        Returns:
            bool: Success status
        """
        for i, route in enumerate(self.routes):
            if route["id"] == route_id:
                self.routes.pop(i)
                self._update_map()
                return True

        return False

    def clear_routes(self):
        """Clear all routes from the map."""
        self.routes = []
        self._update_map()

    def add_safety_overlay(self, overlay_type="heatmap", data=None):
        """
        Add a safety overlay to the map.

        Args:
            overlay_type (str): Type of overlay ("heatmap" or "grid")
            data (dict, optional): Safety data for the overlay

        Returns:
            bool: Success status
        """
        self.safety_overlay = overlay_type
        self._update_map()
        return True

    def remove_safety_overlay(self):
        """Remove the safety overlay from the map."""
        self.safety_overlay = None
        self._update_map()

    def get_html_content(self):
        """
        Get the HTML content for the map.

        Returns:
            str: HTML content
        """
        # In a real implementation, this would generate HTML with Azure Maps
        # For now, we'll return a placeholder

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>SafeWayAI Map</title>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <style>
                html, body {{
                    margin: 0;
                    padding: 0;
                    width: 100%;
                    height: 100%;
                }}
                #map {{
                    width: 100%;
                    height: 100%;
                }}
            </style>
        </head>
        <body>
            <div id="map"></div>
            <script>
                // This would be actual Azure Maps JavaScript in a real implementation
                console.log("Map initialized with ID: {self.map_id}");
                console.log("Center: {self.center_lat}, {self.center_lon}");
                console.log("Zoom: {self.zoom_level}");
                console.log("Map type: {self.map_type}");
                console.log("Routes: {len(self.routes)}");
                console.log("Markers: {len(self.markers)}");
                console.log("Safety overlay: {self.safety_overlay}");
            </script>
        </body>
        </html>
        """

        return html
