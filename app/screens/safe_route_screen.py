import flet as ft
import logging
import time
import os
from datetime import datetime
import threading
import requests
from app.utils.enhanced_theme import get_color_scheme
from app.components.header import Header
from app.components.card_templates import social_impact_banner
from app.components.safety_map import SafetyMap
from app.components.safety_analysis_panel import SafetyAnalysisPanel
from app.components.route_comparison import RouteComparison
from app.components.live_tracking import LiveTracking
from app.services.ai_safety_service import AISafetyService
from app.services.crime_data_service import CrimeDataService
from app.services.safety_prediction_service import SafetyPredictionService
from app.services.location_tracking_service import LocationTrackingService
from app.services.feedback_service import FeedbackService
from app.services.azure_functions_service import AzureFunctionsService
from app.config.azure_config import MAPS_CONFIG

colors = get_color_scheme()
logger = logging.getLogger(__name__)

class SafeRouteScreen:
    def __init__(self, app):
        self.app = app
        self.page = app.page
        self.colors = colors

        # Initialize services
        self.ai_safety_service = AISafetyService()
        self.crime_data_service = CrimeDataService()
        self.safety_prediction_service = SafetyPredictionService()
        self.location_tracking_service = LocationTrackingService()
        self.feedback_service = FeedbackService()
        self.azure_functions_service = AzureFunctionsService()

        # Initialize tracking state
        self.active_tracking_id = None
        self.tracking_thread = None
        self.tracking_active = False

        # Initialize map
        self.safety_map = None
        self.map_api_key = MAPS_CONFIG.get("subscription_key", "")

        # Initialize advanced components
        self.safety_analysis_panel = None
        self.route_comparison = None
        self.live_tracking = None

        # Initialize state for advanced features
        self.show_safety_analysis = False
        self.show_route_comparison = False
        self.show_live_tracking = False

        # Initialize route data
        self.routes = []
        self.current_route = None

        # Initialize container references
        self.route_container = None
        self.route_options_container = None

        # Initialize safety analysis panel
        self.safety_analysis_panel = None

        # Initialize route comparison panel
        self.route_comparison = None

        # Initialize live tracking panel
        self.live_tracking = None

        # Store references to input fields
        self.start_location_field = None
        self.destination_field = None
        self.travel_mode_dropdown = None
        self.time_dropdown = None

        # Store references to route display elements
        self.map_container = None
        self.safest_route_card = None
        self.faster_route_card = None
        self.safety_factors_container = None

        # Store current route data
        self.current_route = None
        self.alternative_routes = []

    def build(self):
        """Build the safe route finder screen."""
        # Create header with back button
        header = Header(
            title="Find Safe Route",
            show_logo=True,
            show_back_button=True,
            on_back=self._go_back
        ).build()

        # Create content
        content = ft.Column(
            controls=[
                # Social impact banner
                social_impact_banner(
                    message="AI for social good - Finding safer paths for everyone",
                    icon="diversity_3",
                    color=self.colors["route_finder"]
                ),

                # Location inputs
                self._build_location_inputs(),

                # Map placeholder
                self._build_map_placeholder(),

                # Route options
                self._build_route_options(),

                # Action buttons
                self._build_action_buttons(),
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

        # Create view
        view = ft.View(
            route="/safe_route",
            controls=[content],
            appbar=header,
            padding=0
        )

        return view

    def _build_location_inputs(self):
        # Create and store references to input fields
        self.start_location_field = ft.TextField(
            label="Current Location",
            hint_text="Your current location",
            prefix_icon="my_location",
            suffix_icon=ft.IconButton(
                icon="gps_fixed",
                tooltip="Use current location",
                on_click=self._use_current_location,
            ),
            border_radius=8,
            value="55 Anderson Street, Johannesburg",  # Default value for testing
        )

        self.destination_field = ft.TextField(
            label="Destination",
            hint_text="Where are you going?",
            prefix_icon="location_on",
            suffix_icon=ft.IconButton(
                icon="search",
                tooltip="Search locations",
                on_click=self._search_locations,
            ),
            border_radius=8,
            value="Sandton City Mall, Johannesburg",  # Default value for testing
        )

        self.travel_mode_dropdown = ft.Dropdown(
            label="Travel Mode",
            hint_text="How are you traveling?",
            options=[
                ft.dropdown.Option("walking", "Walking"),
                ft.dropdown.Option("driving", "Driving"),
                ft.dropdown.Option("transit", "Public Transit"),
            ],
            value="walking",
            expand=True,
        )

        self.time_dropdown = ft.Dropdown(
            label="Time of Day",
            hint_text="When are you traveling?",
            options=[
                ft.dropdown.Option("now", "Current Time"),
                ft.dropdown.Option("morning", "Morning (5am-12pm)"),
                ft.dropdown.Option("afternoon", "Afternoon (12pm-5pm)"),
                ft.dropdown.Option("evening", "Evening (5pm-9pm)"),
                ft.dropdown.Option("night", "Night (9pm-5am)"),
            ],
            value="now",
            expand=True,
        )

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        value="Enter your route details",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                    ),
                    self.start_location_field,
                    self.destination_field,
                    ft.Row(
                        controls=[
                            self.travel_mode_dropdown,
                            self.time_dropdown,
                        ],
                        spacing=10,
                    ),
                ],
                spacing=15,
            ),
            padding=ft.padding.all(20),
        )

    def _build_map_placeholder(self):
        # Create safety map component
        self.safety_map = SafetyMap(
            width=None,
            height=300,
            on_map_click=self._handle_map_click,
            on_map_ready=self._handle_map_ready,
            api_key=self.map_api_key
        )

        # Create map container
        self.map_container = ft.Container(
            bgcolor=ft.colors.GREY_300,
            border_radius=10,
            height=300,
            alignment=ft.alignment.center,
            content=self.safety_map,
        )

        # Create route container for displaying the selected route
        self.route_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        value="Selected Route",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        value="No route selected yet",
                        size=16,
                        italic=True,
                    ),
                ],
                spacing=10,
            ),
            padding=ft.padding.all(20),
            visible=False,
        )

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Stack(
                        controls=[
                            # Map placeholder
                            self.map_container,

                            # Map controls overlay
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.IconButton(
                                            icon="add",
                                            bgcolor=ft.colors.WHITE,
                                            icon_color=ft.colors.BLACK,
                                            tooltip="Zoom in",
                                            on_click=lambda e: self.safety_map._zoom_in() if self.safety_map else None,
                                        ),
                                        ft.IconButton(
                                            icon="remove",
                                            bgcolor=ft.colors.WHITE,
                                            icon_color=ft.colors.BLACK,
                                            tooltip="Zoom out",
                                            on_click=lambda e: self.safety_map._zoom_out() if self.safety_map else None,
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.END,
                                ),
                                alignment=ft.alignment.top_right,
                                padding=10,
                            ),
                        ],
                    ),
                    self.route_container,
                ],
            ),
            padding=ft.padding.symmetric(horizontal=20),
        )

    def _handle_map_click(self, lat, lon):
        """Handle map click event."""
        try:
            logger.info(f"Map clicked at: {lat}, {lon}")
            # In a real implementation, this would allow selecting points on the map
            # For now, we'll just show a snackbar
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Map clicked at: {lat}, {lon}"),
                action="OK",
            )
            self.page.snack_bar.open = True
            self.page.update()
        except Exception as ex:
            logger.error(f"Error handling map click: {ex}")

    def _handle_map_ready(self):
        """Handle map ready event."""
        try:
            logger.info("Map is ready")
            # In a real implementation, this would initialize the map
            # For now, we'll just set the center to Johannesburg
            if self.safety_map:
                self.safety_map.set_center(-26.2041, 28.0473, 12)
        except Exception as ex:
            logger.error(f"Error handling map ready: {ex}")

    def _build_route_options(self):
        # Create safest route card
        self.safest_route_card = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Container(
                                    content=ft.Text(
                                        value="SAFEST",
                                        color=ft.colors.WHITE,
                                        weight=ft.FontWeight.BOLD,
                                        size=12,
                                    ),
                                    bgcolor=colors["safety_high"],
                                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                    border_radius=4,
                                ),
                                ft.Text(
                                    value="15 min",
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(
                                    value="1.2 km",
                                    color=colors["text_secondary"],
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Row(
                            controls=[
                                ft.Icon(
                                    name="shield",
                                    color=colors["safety_high"],
                                    size=16,
                                ),
                                ft.Text(
                                    value="Safety Score: 95/100",
                                    color=colors["safety_high"],
                                    weight=ft.FontWeight.BOLD,
                                    size=14,
                                ),
                            ],
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=5,
                        ),
                        ft.Text(
                            value="Well-lit streets with high foot traffic and regular police patrols",
                            size=14,
                        ),
                    ],
                    spacing=10,
                ),
                padding=15,
            ),
            elevation=3,
            color=ft.colors.WHITE,
        )

        # Create faster route card
        self.faster_route_card = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Container(
                                    content=ft.Text(
                                        value="FASTER",
                                        color=ft.colors.WHITE,
                                        weight=ft.FontWeight.BOLD,
                                        size=12,
                                    ),
                                    bgcolor=colors["warning"],
                                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                    border_radius=4,
                                ),
                                ft.Text(
                                    value="12 min",
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(
                                    value="0.9 km",
                                    color=colors["text_secondary"],
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Row(
                            controls=[
                                ft.Icon(
                                    name="shield",
                                    color=colors["safety_medium"],
                                    size=16,
                                ),
                                ft.Text(
                                    value="Safety Score: 72/100",
                                    color=colors["safety_medium"],
                                    weight=ft.FontWeight.BOLD,
                                    size=14,
                                ),
                            ],
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=5,
                        ),
                        ft.Text(
                            value="Some areas with limited lighting and lower foot traffic",
                            size=14,
                        ),
                    ],
                    spacing=10,
                ),
                padding=15,
            ),
            elevation=2,
        )

        # Create safety factors expansion tile
        safety_factors = ft.ExpansionTile(
            title=ft.Text("Safety Factors Considered"),
            subtitle=ft.Text("Tap to see what makes a route safe"),
            controls=[
                ft.ListTile(
                    leading=ft.Icon("lightbulb", color=colors["warning"]),
                    title=ft.Text("Street Lighting"),
                    subtitle=ft.Text("Well-lit areas are safer at night"),
                ),
                ft.ListTile(
                    leading=ft.Icon("people", color=colors["info"]),
                    title=ft.Text("Foot Traffic"),
                    subtitle=ft.Text("Busier areas provide safety in numbers"),
                ),
                ft.ListTile(
                    leading=ft.Icon("local_police", color=colors["primary"]),
                    title=ft.Text("Police Presence"),
                    subtitle=ft.Text("Areas with regular patrols"),
                ),
                ft.ListTile(
                    leading=ft.Icon("history", color=colors["danger"]),
                    title=ft.Text("Crime History"),
                    subtitle=ft.Text("Areas with lower incident reports"),
                ),
                ft.ListTile(
                    leading=ft.Icon("camera", color=colors["success"]),
                    title=ft.Text("Surveillance"),
                    subtitle=ft.Text("Areas with CCTV coverage"),
                ),
            ],
        )

        # Create action buttons for navigation
        navigation_buttons = ft.Row(
            controls=[
                ft.ElevatedButton(
                    text="Start Navigation",
                    icon="navigation",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        color=colors["primary"],
                    ),
                    on_click=self._start_navigation,
                ),
                ft.ElevatedButton(
                    text="Emergency SOS",
                    icon="emergency",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        bgcolor=colors["danger"],
                        color=ft.colors.WHITE,
                    ),
                    on_click=self._trigger_emergency,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )

        # Create advanced feature buttons
        advanced_buttons = ft.Row(
            controls=[
                ft.OutlinedButton(
                    text="Detailed Analysis",
                    icon="analytics",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        color=colors["primary"],
                    ),
                    on_click=self._show_safety_analysis,
                ),
                ft.OutlinedButton(
                    text="Compare Routes",
                    icon="compare_arrows",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        color=colors["primary"],
                    ),
                    on_click=self._show_route_comparison,
                ),
                ft.OutlinedButton(
                    text="Live Tracking",
                    icon="gps_fixed",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        color=colors["primary"],
                    ),
                    on_click=self._show_live_tracking,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )

        # Create community feedback section
        feedback_section = ft.ExpansionTile(
            title=ft.Text("Community Feedback"),
            subtitle=ft.Text("Report safety concerns or incidents"),
            controls=[
                ft.Text(
                    "Help make routes safer by reporting issues you encounter",
                    size=14,
                ),
                ft.Dropdown(
                    label="Report Type",
                    hint_text="Select type of report",
                    options=[
                        ft.dropdown.Option("crime", "Crime Incident"),
                        ft.dropdown.Option("hazard", "Road Hazard"),
                        ft.dropdown.Option("lighting", "Poor Lighting"),
                        ft.dropdown.Option("infrastructure", "Infrastructure Issue"),
                    ],
                    width=300,
                ),
                ft.TextField(
                    label="Description",
                    hint_text="Describe the safety concern",
                    multiline=True,
                    min_lines=2,
                    max_lines=4,
                    width=300,
                ),
                ft.Dropdown(
                    label="Severity",
                    hint_text="How serious is this issue?",
                    options=[
                        ft.dropdown.Option("low", "Low - Minor concern"),
                        ft.dropdown.Option("medium", "Medium - Moderate risk"),
                        ft.dropdown.Option("high", "High - Significant danger"),
                        ft.dropdown.Option("critical", "Critical - Immediate threat"),
                    ],
                    width=300,
                ),
                ft.ElevatedButton(
                    text="Submit Report",
                    icon="report",
                    on_click=self._submit_safety_report,
                ),
            ],
        )

        # Create community alerts section
        community_alerts = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon("campaign", color=colors["warning"]),
                            ft.Text(
                                "Community Safety Alerts",
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Text(
                        "Recent alerts from community members",
                        size=12,
                    ),
                    ft.Container(
                        content=ft.Text(
                            "No active alerts in this area",
                            italic=True,
                        ),
                        padding=10,
                    ),
                ],
                spacing=5,
            ),
            padding=10,
            border_radius=10,
            bgcolor=ft.colors.AMBER_50,
        )

        # Create the route options container
        self.route_options_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        value="Route Options",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                    ),
                    self.safest_route_card,
                    self.faster_route_card,
                    navigation_buttons,
                    advanced_buttons,
                    safety_factors,
                    feedback_section,
                    community_alerts,
                ],
                spacing=10,
            ),
            padding=ft.padding.all(20),
        )

        # Return the container with all route options
        return self.route_options_container

    def _build_action_buttons(self):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.ElevatedButton(
                        text="Find Safe Route",
                        icon="navigation",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=ft.padding.all(15),
                        ),
                        expand=True,
                        on_click=self._find_safe_route,
                    ),
                    ft.IconButton(
                        icon="share",
                        tooltip="Share this route",
                        icon_color=colors["primary"],
                        on_click=self._share_route,
                    ),
                    ft.IconButton(
                        icon="save",
                        tooltip="Save this route",
                        icon_color=colors["primary"],
                        on_click=self._save_route,
                    ),
                ],
                spacing=10,
            ),
            padding=ft.padding.only(left=20, right=20, bottom=30),
        )

    def _go_back(self, e=None):
        """Navigate back to the home screen."""
        self.app.page.go("/")

    def _use_current_location(self, e=None):
        """Use the current location (would use device GPS in a real implementation)."""
        # In a real implementation, this would use the device's GPS
        # For now, we'll set a default location in Johannesburg
        self.start_location_field.value = "Current Location: Johannesburg CBD"
        self.page.update()

    def _search_locations(self, e=None):
        """Search for locations using Azure Maps."""
        # This would open a search dialog in a real implementation
        # For now, we'll just show a snackbar
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Location search would open here"),
            action="OK",
        )
        self.page.snack_bar.open = True
        self.page.update()

    def _find_safe_route(self, e=None):
        """Find a safe route between the start and end points using AI safety analysis."""
        try:
            # Show loading state
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Finding the safest route using AI analysis..."),
            )
            self.page.snack_bar.open = True
            self.page.update()

            # Get input values
            start_location = self.start_location_field.value
            destination = self.destination_field.value
            travel_mode = self.travel_mode_dropdown.value
            time_of_day = self.time_dropdown.value

            # Convert "now" to actual time of day
            if time_of_day == "now":
                current_hour = datetime.now().hour
                if 5 <= current_hour < 12:
                    time_of_day = "morning"
                elif 12 <= current_hour < 17:
                    time_of_day = "afternoon"
                elif 17 <= current_hour < 21:
                    time_of_day = "evening"
                else:
                    time_of_day = "night"

            # Validate inputs
            if not start_location or not destination:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Please enter both start and destination locations"),
                )
                self.page.snack_bar.open = True
                self.page.update()
                return

            logger.info(f"Finding route from {start_location} to {destination} via {travel_mode} at {time_of_day}")

            # Try to use the Azure Maps service to geocode the addresses
            try:
                # Get the maps service from the app
                maps_service = None
                if hasattr(self.app, 'service_manager') and hasattr(self.app.service_manager, 'maps_service'):
                    maps_service = self.app.service_manager.maps_service

                start_coords = None
                dest_coords = None

                if maps_service:
                    # Geocode the start location
                    start_results = maps_service.search_address(start_location, limit=1)
                    if "error" not in start_results and "results" in start_results and start_results["results"]:
                        start_pos = start_results["results"][0].get("position", {})
                        start_coords = (start_pos.get("lat"), start_pos.get("lon"))

                    # Geocode the destination
                    dest_results = maps_service.search_address(destination, limit=1)
                    if "error" not in dest_results and "results" in dest_results and dest_results["results"]:
                        dest_pos = dest_results["results"][0].get("position", {})
                        dest_coords = (dest_pos.get("lat"), dest_pos.get("lon"))

                # If geocoding failed, use simulated coordinates
                if not start_coords or not dest_coords:
                    # Use simulated coordinates
                    start_coords = (-26.2041, 28.0473)  # Johannesburg
                    dest_coords = (-26.1052, 28.0560)   # Sandton

                # Create location objects
                start_point = {"latitude": start_coords[0], "longitude": start_coords[1]}
                end_point = {"latitude": dest_coords[0], "longitude": dest_coords[1]}

                # Generate route points (in a real implementation, this would come from Azure Maps)
                route_points = [
                    start_point,
                    {"latitude": (start_coords[0] + dest_coords[0]) / 2, "longitude": (start_coords[1] + dest_coords[1]) / 2},
                    end_point
                ]

                # Calculate route distance and duration based on travel mode
                # This is a simplified calculation - in a real implementation, use Azure Maps
                from math import sqrt, pow

                # Calculate straight-line distance in kilometers (very rough approximation)
                distance = sqrt(pow(start_coords[0] - dest_coords[0], 2) + pow(start_coords[1] - dest_coords[1], 2)) * 111

                # Calculate duration based on travel mode
                if travel_mode == "walking":
                    # Walking speed ~5 km/h
                    duration = (distance / 5) * 60  # minutes
                elif travel_mode == "transit":
                    # Transit speed ~25 km/h
                    duration = (distance / 25) * 60  # minutes
                else:  # driving
                    # Driving speed ~40 km/h in urban areas
                    duration = (distance / 40) * 60  # minutes

                # Use AI to analyze route safety with our enhanced prediction service
                safety_analysis = self.safety_prediction_service.predict_route_safety(
                    route_points,
                    time_of_day,
                    travel_mode
                )

                # Create the primary route data
                primary_route = {
                    "route_type": "safest",
                    "start_location": start_location,
                    "destination": destination,
                    "travel_mode": travel_mode,
                    "time_of_day": time_of_day,
                    "distance": distance,
                    "duration": int(duration),
                    "safety_score": safety_analysis["safety_score"],
                    "safety_factors": safety_analysis["factors"],
                    "safety_insights": safety_analysis["insights"],
                    "route_points": route_points
                }

                # Store the current route
                self.current_route = primary_route

                # Generate alternative routes with enhanced prediction
                self.alternative_routes = self.safety_prediction_service.get_alternative_routes(
                    start_point, end_point, primary_route, time_of_day, travel_mode
                )

                # Update the UI with the results
                self._update_route_display_with_ai_analysis(primary_route, self.alternative_routes)

            except Exception as ex:
                logger.warning(f"Error using AI safety analysis: {ex}")
                # Fall back to simulated data
                self._update_route_display(start_location, destination, travel_mode)

        except Exception as ex:
            logger.error(f"Error finding route: {ex}")
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error: {str(ex)}"),
            )
            self.page.snack_bar.open = True
            self.page.update()

    def _update_route_display(self, start_location, destination, travel_mode):
        """Update the route display with simulated results."""
        try:
            # Update map display
            self.map_container.content = ft.Column(
                controls=[
                    ft.Text(
                        value=f"Route from {start_location} to {destination}",
                        color=ft.colors.BLACK,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        value=f"Travel mode: {travel_mode}",
                        color=ft.colors.BLACK,
                    ),
                    ft.Icon(
                        name="map",
                        size=50,
                        color=colors["primary"],
                    ),
                    ft.Text(
                        value="Map with route would display here",
                        color=ft.colors.BLACK,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            )

            # Update route cards with simulated data
            # In a real implementation, this would use actual data from the API

            # Update safest route card
            self._update_safest_route_card(
                duration=18,
                distance=1.5,
                safety_score=92,
                description="Well-lit streets with high foot traffic and regular police patrols"
            )

            # Update faster route card
            self._update_faster_route_card(
                duration=14,
                distance=1.2,
                safety_score=68,
                description="Some areas with limited lighting and lower foot traffic"
            )

            # Show success message
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Safe route found!"),
            )
            self.page.snack_bar.open = True

            # Update the page
            self.page.update()

        except Exception as ex:
            logger.error(f"Error updating route display: {ex}")
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error updating display: {str(ex)}"),
            )
            self.page.snack_bar.open = True
            self.page.update()

    def _update_route_display_with_ai_analysis(self, primary_route, alternative_routes):
        """Update the route display with AI-analyzed route data."""
        try:
            # Extract route information
            start_location = primary_route["start_location"]
            destination = primary_route["destination"]
            travel_mode = primary_route["travel_mode"]
            time_of_day = primary_route["time_of_day"]
            distance = primary_route["distance"]
            duration = primary_route["duration"]
            safety_score = primary_route["safety_score"]
            safety_insights = primary_route["safety_insights"]
            safety_factors = primary_route["safety_factors"]
            route_points = primary_route["route_points"]

            # Create route info header
            route_info_header = ft.Column(
                controls=[
                    ft.Text(
                        value=f"AI-Analyzed Safe Route",
                        color=ft.colors.BLACK,
                        weight=ft.FontWeight.BOLD,
                        size=18,
                    ),
                    ft.Text(
                        value=f"From {start_location} to {destination}",
                        color=ft.colors.BLACK,
                    ),
                    ft.Row(
                        controls=[
                            ft.Icon(
                                name=self._get_travel_mode_icon(travel_mode),
                                size=20,
                                color=colors["primary"],
                            ),
                            ft.Text(
                                value=f"{travel_mode.capitalize()} | ",
                                color=ft.colors.BLACK,
                            ),
                            ft.Icon(
                                name=self._get_time_icon(time_of_day),
                                size=20,
                                color=colors["primary"],
                            ),
                            ft.Text(
                                value=f"{time_of_day.capitalize()}",
                                color=ft.colors.BLACK,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        controls=[
                            ft.Icon(
                                name="map",
                                size=20,
                                color=colors["primary"],
                            ),
                            ft.Text(
                                value=f"Distance: {distance:.1f} km | Duration: {duration} min",
                                color=ft.colors.BLACK,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
            )

            # Create safety score display
            safety_score_display = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(
                            name="shield",
                            size=24,
                            color=self._get_safety_color(safety_score),
                        ),
                        ft.Text(
                            value=f"Overall Safety Score: {safety_score}/100",
                            color=self._get_safety_color(safety_score),
                            weight=ft.FontWeight.BOLD,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                padding=10,
                border_radius=10,
                bgcolor=ft.colors.BLUE_50,
            )

            # Create or update the map
            if not self.safety_map:
                # Create new map
                self.safety_map = SafetyMap(
                    width=None,
                    height=250,
                    api_key=self.map_api_key,
                    on_map_click=self._handle_map_click,
                    on_map_ready=self._handle_map_ready
                )

                # Set center based on route
                if primary_route["route_points"] and len(primary_route["route_points"]) > 0:
                    mid_point = primary_route["route_points"][len(primary_route["route_points"]) // 2]
                    self.safety_map.set_center(
                        mid_point["latitude"],
                        mid_point["longitude"],
                        zoom=13
                    )
            else:
                # Clear existing routes and markers
                self.safety_map.clear_routes()
                self.safety_map.clear_markers()

                # Set center based on route
                if primary_route["route_points"] and len(primary_route["route_points"]) > 0:
                    mid_point = primary_route["route_points"][len(primary_route["route_points"]) // 2]
                    self.safety_map.set_center(
                        mid_point["latitude"],
                        mid_point["longitude"],
                        zoom=13
                    )

            # Add the primary route to the map
            if primary_route["route_points"] and len(primary_route["route_points"]) > 1:
                self.safety_map.add_route(primary_route["route_points"], safety_score=safety_score)

                # Add start and end markers
                self.safety_map.add_marker(
                    primary_route["route_points"][0]["latitude"],
                    primary_route["route_points"][0]["longitude"],
                    title="Start",
                    icon="play_circle"
                )

                self.safety_map.add_marker(
                    primary_route["route_points"][-1]["latitude"],
                    primary_route["route_points"][-1]["longitude"],
                    title="Destination",
                    icon="location_on"
                )

            # Add safety overlay
            self.safety_map.add_safety_overlay("heatmap")

            # Update map container
            self.map_container.content = ft.Column(
                controls=[
                    route_info_header,
                    safety_score_display,
                    self.safety_map,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            )

            # Find the faster alternative route if available
            faster_route = None
            for route in alternative_routes:
                if route.get("route_type") == "faster":
                    faster_route = route
                    break

            # Update safest route card with primary route data
            self._update_safest_route_card(
                duration=duration,
                distance=distance,
                safety_score=safety_score,
                description=safety_insights[0] if safety_insights else "AI-recommended safest route"
            )

            # Update faster route card if available
            if faster_route:
                self._update_faster_route_card(
                    duration=faster_route["duration"],
                    distance=faster_route["distance"],
                    safety_score=faster_route["safety_score"],
                    description=faster_route["insights"][0] if "insights" in faster_route and faster_route["insights"] else "Faster alternative route"
                )
            else:
                # Create a simulated faster route
                alt_duration = max(1, int(duration * 0.85))  # 15% faster
                alt_distance = max(0.5, distance * 0.9)  # 10% shorter
                alt_safety_score = max(50, safety_score - 20)  # Less safe

                self._update_faster_route_card(
                    duration=alt_duration,
                    distance=alt_distance,
                    safety_score=alt_safety_score,
                    description=self._get_safety_description(alt_safety_score)
                )

            # Update safety factors display
            self._update_safety_factors_display(safety_factors, safety_insights, time_of_day)

            # Show success message
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("AI-analyzed safe route found!"),
            )
            self.page.snack_bar.open = True

            # Update the page
            self.page.update()

        except Exception as ex:
            logger.error(f"Error updating route display with AI analysis: {ex}")
            # Fall back to simulated data
            self._update_route_display(
                primary_route.get("start_location", ""),
                primary_route.get("destination", ""),
                primary_route.get("travel_mode", "walking")
            )

    def _update_safety_factors_display(self, safety_factors, safety_insights, time_of_day):
        """Update the safety factors display with AI analysis."""
        try:
            # Create a list of safety factor tiles
            factor_tiles = []

            # Add tiles for each safety factor
            for factor, score in safety_factors.items():
                icon_name = self._get_factor_icon(factor)
                factor_name = self._get_factor_display_name(factor)

                factor_tiles.append(
                    ft.ListTile(
                        leading=ft.Icon(
                            icon_name,
                            color=self._get_safety_color(score),
                        ),
                        title=ft.Text(factor_name),
                        subtitle=ft.Text(f"Score: {score}/100"),
                    )
                )

            # Add insights section
            insights_container = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            value="AI Safety Insights",
                            weight=ft.FontWeight.BOLD,
                            size=16,
                        ),
                        *[
                            ft.Row(
                                controls=[
                                    ft.Icon("info", size=16, color=colors["info"]),
                                    ft.Text(insight, size=14),
                                ],
                                vertical_alignment=ft.CrossAxisAlignment.START,
                                spacing=10,
                            )
                            for insight in safety_insights
                        ],
                    ],
                    spacing=5,
                ),
                padding=10,
                bgcolor=ft.colors.BLUE_50,
                border_radius=8,
                margin=ft.margin.only(bottom=10),
            )

            # Add time-specific advice
            time_advice = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(
                            self._get_time_icon(time_of_day),
                            color=colors["warning"],
                        ),
                        ft.Text(
                            f"This route was analyzed for {time_of_day} travel",
                            weight=ft.FontWeight.BOLD,
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=10,
                bgcolor=ft.colors.AMBER_50,
                border_radius=8,
            )

            # Update the safety factors expansion tile
            safety_factors_tile = ft.ExpansionTile(
                title=ft.Text("AI Safety Analysis Factors"),
                subtitle=ft.Text("Tap to see what makes a route safe"),
                controls=[
                    insights_container,
                    *factor_tiles,
                    time_advice,
                ],
            )

            # Find and replace the safety factors tile in the route options
            for i, control in enumerate(self._build_route_options().content.controls):
                if isinstance(control, ft.ExpansionTile):
                    self._build_route_options().content.controls[i] = safety_factors_tile
                    break

        except Exception as ex:
            logger.error(f"Error updating safety factors display: {ex}")

    def _get_travel_mode_icon(self, travel_mode):
        """Get the icon for a travel mode."""
        if travel_mode == "walking":
            return "directions_walk"
        elif travel_mode == "transit":
            return "directions_transit"
        else:  # driving
            return "directions_car"

    def _get_time_icon(self, time_of_day):
        """Get the icon for a time of day."""
        if time_of_day == "morning":
            return "wb_sunny"
        elif time_of_day == "afternoon":
            return "wb_sunny"
        elif time_of_day == "evening":
            return "nights_stay"
        else:  # night
            return "dark_mode"

    def _get_factor_icon(self, factor):
        """Get the icon for a safety factor."""
        icons = {
            "crime_rate": "security",
            "lighting": "lightbulb",
            "foot_traffic": "people",
            "police_presence": "local_police",
            "time_of_day": "access_time",
            "surveillance": "camera",
            "road_quality": "road",
            "emergency_services": "local_hospital",
        }
        return icons.get(factor, "info")

    def _get_factor_display_name(self, factor):
        """Get a display name for a safety factor."""
        names = {
            "crime_rate": "Crime Rate",
            "lighting": "Street Lighting",
            "foot_traffic": "Pedestrian Traffic",
            "police_presence": "Police Presence",
            "time_of_day": "Time of Day",
            "surveillance": "CCTV Coverage",
            "road_quality": "Road Quality",
            "emergency_services": "Emergency Services",
        }
        return names.get(factor, factor.replace("_", " ").title())

    def _get_safety_color(self, safety_score):
        """Get a color based on the safety score."""
        if safety_score >= 85:
            return colors["safety_high"]
        elif safety_score >= 70:
            return colors["safety_medium"]
        elif safety_score >= 50:
            return colors["warning"]
        else:
            return colors["danger"]

    def _get_safety_description(self, safety_score):
        """Generate a safety description based on the safety score."""
        if safety_score >= 90:
            return "Well-lit streets with high foot traffic and regular police patrols"
        elif safety_score >= 80:
            return "Generally safe area with good visibility and moderate foot traffic"
        elif safety_score >= 70:
            return "Mostly safe with some areas having limited lighting"
        elif safety_score >= 60:
            return "Mixed safety profile with some areas to be cautious about"
        elif safety_score >= 50:
            return "Some areas with limited lighting and lower foot traffic"
        else:
            return "Areas with safety concerns, exercise caution when traveling"

    def _update_safest_route_card(self, duration, distance, safety_score, description):
        """Update the safest route card with new data."""
        # Get the container inside the card
        container = self.safest_route_card.content

        # Get the column inside the container
        column = container.content

        # Update the duration text
        column.controls[0].controls[1].value = f"{duration} min"

        # Update the distance text
        column.controls[0].controls[2].value = f"{distance} km"

        # Update the safety score text
        column.controls[1].controls[1].value = f"Safety Score: {safety_score}/100"

        # Update the description text
        column.controls[2].value = description

    def _update_faster_route_card(self, duration, distance, safety_score, description):
        """Update the faster route card with new data."""
        # Get the container inside the card
        container = self.faster_route_card.content

        # Get the column inside the container
        column = container.content

        # Update the duration text
        column.controls[0].controls[1].value = f"{duration} min"

        # Update the distance text
        column.controls[0].controls[2].value = f"{distance} km"

        # Update the safety score text
        column.controls[1].controls[1].value = f"Safety Score: {safety_score}/100"

        # Update the description text
        column.controls[2].value = description

    def _share_route(self, e=None):
        """Share the current route."""
        # In a real implementation, this would open a share dialog
        # For now, we'll just show a snackbar
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Sharing route..."),
            action="OK",
        )
        self.page.snack_bar.open = True
        self.page.update()

    def _save_route(self, e=None):
        """Save the current route."""
        # In a real implementation, this would save the route to the user's account
        # For now, we'll just show a snackbar
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Route saved!"),
            action="OK",
        )
        self.page.snack_bar.open = True
        self.page.update()

    def _start_navigation(self, e=None):
        """Start real-time navigation and safety monitoring."""
        try:
            # If no route exists, automatically find one
            if not self.current_route:
                # Show loading message
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Finding the safest route..."),
                )
                self.page.snack_bar.open = True
                self.page.update()

                # Get input values from the fields
                start_location = self.start_location_field.value if self.start_location_field else "3012 winnie mandela dr"
                destination = self.destination_field.value if self.destination_field else "57 Bok street"
                travel_mode = self.travel_mode_dropdown.value if self.travel_mode_dropdown else "walking"
                time_of_day = self.time_dropdown.value if self.time_dropdown else "now"

                # First try to find a route using the find_safe_route method
                self._find_safe_route()

                # If still no route, create a default one
                if not self.current_route:
                    # Create a default route with more waypoints for better visualization
                    self.current_route = {
                        "route_type": "safest",
                        "safety_score": 85,
                        "duration_min": 25,
                        "distance_km": 3.5,
                        "start_location": start_location,
                        "destination": destination,
                        "travel_mode": travel_mode,
                        "time_of_day": time_of_day,
                        "route_points": [
                            {"latitude": -26.2041, "longitude": 28.0473},  # Start
                            {"latitude": -26.2046, "longitude": 28.0478},  # Waypoint 1
                            {"latitude": -26.2051, "longitude": 28.0483},  # Waypoint 2
                            {"latitude": -26.2056, "longitude": 28.0488},  # Waypoint 3
                            {"latitude": -26.2061, "longitude": 28.0493},  # Waypoint 4
                            {"latitude": -26.2066, "longitude": 28.0498},  # Waypoint 5
                            {"latitude": -26.2071, "longitude": 28.0503},  # Waypoint 6
                            {"latitude": -26.2076, "longitude": 28.0508},  # Waypoint 7
                            {"latitude": -26.2081, "longitude": 28.0513}   # End
                        ],
                        "safety_factors": {
                            "crime_rate": 80,
                            "lighting": 90,
                            "foot_traffic": 85,
                            "police_presence": 75,
                            "time_of_day": 85,
                            "surveillance": 80,
                            "road_quality": 90,
                            "emergency_services": 85
                        },
                        "safety_insights": [
                            "This route has good lighting and police presence",
                            "Avoid side streets after dark",
                            "Stay on main roads with higher foot traffic"
                        ],
                        "hotspots": [
                            {
                                "description": "Low lighting area near Park Street",
                                "risk_level": "medium",
                                "latitude": -26.2051,
                                "longitude": 28.0483
                            }
                        ]
                    }

                    # Update the UI to show the route
                    self._display_route(self.current_route)

            # Stop any existing tracking
            self._stop_navigation()

            # Get user ID (in a real app, this would be the logged-in user)
            user_id = "demo_user"

            # Start tracking with the location tracking service
            self.active_tracking_id = self.location_tracking_service.start_tracking(
                user_id,
                self.current_route,
                self._tracking_callback
            )

            if self.active_tracking_id:
                self.tracking_active = True

                # Check if the app has a screens dictionary (newer app structure)
                if hasattr(self.app, 'screens') and isinstance(self.app.screens, dict):
                    # Get the navigation screen from the app
                    navigation_screen = self.app.screens.get("/navigation")
                    if navigation_screen:
                        # Initialize the navigation screen with route data and tracking ID
                        navigation_screen.initialize_navigation(self.current_route, self.active_tracking_id)

                        # Navigate to the navigation screen
                        self.page.go("/navigation")
                        return

                # If we can't find the navigation screen in the screens dictionary,
                # try to create a new instance (older app structure)
                try:
                    from app.screens.navigation_screen import NavigationScreen
                    navigation_screen = NavigationScreen(self.app)
                    navigation_screen.initialize_navigation(self.current_route, self.active_tracking_id)

                    # Add the navigation screen to the page views
                    self.page.views.append(navigation_screen.build())
                    self.page.go("/navigation")
                    return
                except Exception as nav_ex:
                    logger.error(f"Error creating navigation screen: {nav_ex}")

                # Fall back to showing the dialog if navigation screen is not available
                self._show_live_tracking()

                # Show success message
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Navigation started with real-time safety monitoring"),
                )
                self.page.snack_bar.open = True
                self.page.update()

                # Start tracking thread to update UI
                self.tracking_thread = threading.Thread(target=self._tracking_update_loop)
                self.tracking_thread.daemon = True
                self.tracking_thread.start()
            else:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Failed to start navigation"),
                )
                self.page.snack_bar.open = True
                self.page.update()

        except Exception as ex:
            logger.error(f"Error starting navigation: {ex}")
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error: {str(ex)}"),
            )
            self.page.snack_bar.open = True
            self.page.update()

    def _stop_navigation(self, e=None):
        """Stop real-time navigation and safety monitoring."""
        try:
            if self.active_tracking_id:
                # Stop tracking
                self.location_tracking_service.stop_tracking(self.active_tracking_id)
                self.active_tracking_id = None
                self.tracking_active = False

                # Hide navigation UI
                self._hide_navigation_ui()

                # Show message
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Navigation stopped"),
                )
                self.page.snack_bar.open = True
                self.page.update()

        except Exception as ex:
            logger.error(f"Error stopping navigation: {ex}")
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error: {str(ex)}"),
            )
            self.page.snack_bar.open = True
            self.page.update()

    def _tracking_callback(self, tracking_id, event_type, event_data):
        """Callback for tracking events."""
        try:
            logger.info(f"Tracking event: {event_type}")

            if event_type == "safety_warning":
                # Show safety warning
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(event_data.get("advice", "Safety warning: Exercise caution in this area")),
                    bgcolor=colors["warning"],
                    action="OK",
                )
                self.page.snack_bar.open = True
                self.page.update()

            elif event_type == "hotspot_warning":
                # Show hotspot warning
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(event_data.get("advice", "Warning: You are entering a high-risk area")),
                    bgcolor=colors["danger"],
                    action="OK",
                )
                self.page.snack_bar.open = True
                self.page.update()

            elif event_type == "emergency":
                # Show emergency alert
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("EMERGENCY: Contacting emergency services"),
                    bgcolor=colors["danger"],
                    action="OK",
                )
                self.page.snack_bar.open = True
                self.page.update()

        except Exception as ex:
            logger.error(f"Error in tracking callback: {ex}")

    def _tracking_update_loop(self):
        """Background thread to update navigation UI."""
        try:
            while self.tracking_active and self.active_tracking_id:
                # Get current tracking status
                status = self.location_tracking_service.get_tracking_status(self.active_tracking_id)

                if status and self.live_tracking:
                    # Update the live tracking UI
                    position = status.get("position_index", 0)
                    self.live_tracking.update_position(position_index=position)

                    # Add any alerts
                    alerts = status.get("alerts", [])
                    for alert in alerts:
                        self.live_tracking.add_alert(
                            alert.get("text", "Safety alert"),
                            alert.get("level", "info")
                        )

                    # Update the page
                    self.page.update()

                # Sleep to avoid high CPU usage
                time.sleep(1)

        except Exception as ex:
            logger.error(f"Error in tracking update loop: {ex}")

    def _show_navigation_ui(self):
        """Show navigation UI elements."""
        # In a real implementation, this would show turn-by-turn navigation
        # For now, we'll just update the UI to show we're in navigation mode
        pass

    def _hide_navigation_ui(self):
        """Hide navigation UI elements."""
        # In a real implementation, this would hide navigation UI
        pass

    def _trigger_emergency(self, e=None):
        """Trigger emergency response."""
        try:
            if self.active_tracking_id:
                # Trigger emergency
                success = self.location_tracking_service.trigger_emergency(
                    self.active_tracking_id,
                    "sos",
                    {"user_initiated": True}
                )

                if success:
                    self.page.snack_bar = ft.SnackBar(
                        content=ft.Text("Emergency alert sent! Help is on the way."),
                        bgcolor=colors["danger"],
                        action="OK",
                    )
                    self.page.snack_bar.open = True
                    self.page.update()
                else:
                    self.page.snack_bar = ft.SnackBar(
                        content=ft.Text("Failed to send emergency alert"),
                    )
                    self.page.snack_bar.open = True
                    self.page.update()
            else:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Navigation not active"),
                )
                self.page.snack_bar.open = True
                self.page.update()

        except Exception as ex:
            logger.error(f"Error triggering emergency: {ex}")
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error: {str(ex)}"),
            )
            self.page.snack_bar.open = True
            self.page.update()

    def _submit_safety_report(self, e=None):
        """Submit a safety report to the feedback service."""
        try:
            # In a real implementation, this would get values from the form fields
            # For now, we'll use simulated values
            report_type = "hazard"
            description = "Simulated safety report from the app"
            severity = "medium"

            # Get current location (would use GPS in a real implementation)
            latitude = -26.2041
            longitude = 28.0473

            # Get user ID (would be the logged-in user in a real implementation)
            user_id = "demo_user"

            # Submit the report
            report_id = self.feedback_service.add_safety_report(
                user_id,
                report_type,
                description,
                latitude,
                longitude,
                None,  # address
                severity
            )

            if report_id:
                # Show success message
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Safety report submitted. Thank you for helping make routes safer!"),
                    action="OK",
                )
                self.page.snack_bar.open = True
                self.page.update()
            else:
                # Show error message
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Failed to submit safety report"),
                    action="OK",
                )
                self.page.snack_bar.open = True
                self.page.update()

        except Exception as ex:
            logger.error(f"Error submitting safety report: {ex}")
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error: {str(ex)}"),
                action="OK",
            )
            self.page.snack_bar.open = True
            self.page.update()

    # Advanced feature methods

    def _show_safety_analysis(self, e=None):
        """Show the detailed safety analysis panel."""
        try:
            if not self.current_route:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Please find a route first"),
                    action="OK",
                )
                self.page.snack_bar.open = True
                self.page.update()
                return

            # Create safety data for the panel
            safety_data = {
                "overall_score": self.current_route.get("safety_score", 0),
                "factors": self.current_route.get("safety_factors", {}),
                "insights": self.current_route.get("safety_insights", []),
                "time_analysis": {
                    "morning": self.current_route.get("safety_factors", {}).get("time_of_day", 0) + 10,
                    "afternoon": self.current_route.get("safety_factors", {}).get("time_of_day", 0) + 5,
                    "evening": self.current_route.get("safety_factors", {}).get("time_of_day", 0) - 5,
                    "night": self.current_route.get("safety_factors", {}).get("time_of_day", 0) - 15,
                },
                "hotspots": self.current_route.get("hotspots", []),
                "recommendations": [
                    "Stay on well-lit main roads when possible",
                    "Be aware of your surroundings, especially at night",
                    "Share your journey with a trusted contact",
                    "Keep emergency contacts easily accessible"
                ]
            }

            # Create the safety analysis panel
            self.safety_analysis_panel = SafetyAnalysisPanel(
                safety_data=safety_data,
                width=None,
                height=None,
                on_close=self._hide_safety_analysis
            )

            # Show the panel
            self.show_safety_analysis = True

            # Create a container for the panel if it doesn't exist
            if not self.route_container:
                self.route_container = ft.Container(
                    content=ft.Column(
                        controls=[],
                        spacing=10,
                        scroll=ft.ScrollMode.AUTO
                    ),
                    padding=10,
                    border_radius=10,
                )

            # Update the UI
            self.route_container.content.controls.append(self.safety_analysis_panel)
            self.page.update()

        except Exception as ex:
            logger.error(f"Error showing safety analysis: {ex}")
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error: {str(ex)}"),
                action="OK",
            )
            self.page.snack_bar.open = True
            self.page.update()

    def _hide_safety_analysis(self, e=None):
        """Hide the safety analysis panel."""
        try:
            self.show_safety_analysis = False

            # Set the panel to None
            self.safety_analysis_panel = None

            # Update the UI
            if self.route_container and isinstance(self.route_container.content, ft.Column):
                # Remove the panel from the container
                new_controls = []
                for control in self.route_container.content.controls:
                    if not isinstance(control, SafetyAnalysisPanel):
                        new_controls.append(control)
                self.route_container.content.controls = new_controls

            self.page.update()

        except Exception as ex:
            logger.error(f"Error hiding safety analysis: {ex}")

    def _show_route_comparison(self, e=None):
        """Show the route comparison panel."""
        try:
            if not self.routes:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Please find a route first"),
                    action="OK",
                )
                self.page.snack_bar.open = True
                self.page.update()
                return

            # Create sample routes if none exist
            if not self.routes:
                self.routes = [
                    {
                        "type": "safest",
                        "safety_score": 85,
                        "duration_min": 25,
                        "distance_km": 3.5,
                        "route_points": [
                            {"latitude": -26.2041, "longitude": 28.0473},
                            {"latitude": -26.2051, "longitude": 28.0483},
                            {"latitude": -26.2061, "longitude": 28.0493}
                        ],
                        "safety_factors": {
                            "crime_rate": 80,
                            "lighting": 90,
                            "foot_traffic": 85,
                            "police_presence": 75,
                            "time_of_day": 85,
                            "surveillance": 80,
                            "road_quality": 90,
                            "emergency_services": 85
                        }
                    },
                    {
                        "type": "fastest",
                        "safety_score": 70,
                        "duration_min": 18,
                        "distance_km": 2.8,
                        "route_points": [
                            {"latitude": -26.2041, "longitude": 28.0473},
                            {"latitude": -26.2055, "longitude": 28.0490},
                            {"latitude": -26.2061, "longitude": 28.0493}
                        ],
                        "safety_factors": {
                            "crime_rate": 65,
                            "lighting": 75,
                            "foot_traffic": 70,
                            "police_presence": 60,
                            "time_of_day": 85,
                            "surveillance": 65,
                            "road_quality": 80,
                            "emergency_services": 75
                        }
                    },
                    {
                        "type": "balanced",
                        "safety_score": 78,
                        "duration_min": 22,
                        "distance_km": 3.2,
                        "route_points": [
                            {"latitude": -26.2041, "longitude": 28.0473},
                            {"latitude": -26.2053, "longitude": 28.0486},
                            {"latitude": -26.2061, "longitude": 28.0493}
                        ],
                        "safety_factors": {
                            "crime_rate": 75,
                            "lighting": 80,
                            "foot_traffic": 75,
                            "police_presence": 70,
                            "time_of_day": 85,
                            "surveillance": 75,
                            "road_quality": 85,
                            "emergency_services": 80
                        }
                    }
                ]

            # Create the route comparison panel
            self.route_comparison = RouteComparison(
                routes=self.routes,
                width=None,
                height=None,
                on_route_select=self._select_route
            )

            # Show the panel
            self.show_route_comparison = True

            # Create a container for the panel if it doesn't exist
            if not self.route_options_container:
                self.route_options_container = ft.Container(
                    content=ft.Column(
                        controls=[],
                        spacing=10,
                        scroll=ft.ScrollMode.AUTO
                    ),
                    padding=10,
                    border_radius=10,
                )

            # Update the UI
            self.route_options_container.content.controls.append(self.route_comparison)
            self.page.update()

        except Exception as ex:
            logger.error(f"Error showing route comparison: {ex}")
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error: {str(ex)}"),
                action="OK",
            )
            self.page.snack_bar.open = True
            self.page.update()

    def _hide_route_comparison(self, e=None):
        """Hide the route comparison panel."""
        try:
            self.show_route_comparison = False

            # Set the panel to None
            self.route_comparison = None

            # Update the UI
            if self.route_options_container and isinstance(self.route_options_container.content, ft.Column):
                # Remove the panel from the container
                new_controls = []
                for control in self.route_options_container.content.controls:
                    if not isinstance(control, RouteComparison):
                        new_controls.append(control)
                self.route_options_container.content.controls = new_controls

            self.page.update()

        except Exception as ex:
            logger.error(f"Error hiding route comparison: {ex}")

    def _show_live_tracking(self, e=None):
        """Show live tracking UI."""
        try:
            logger.info("Starting _show_live_tracking method")

            # Create a simple live tracking UI
            # Create a column with tracking information
            tracking_info = ft.Column(
                controls=[
                    ft.Text("Live Navigation", size=24, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Route: {self.current_route.get('start_location', 'Current Location')} to {self.current_route.get('destination', 'Destination')}"),
                    ft.Text(f"Safety Score: {self.current_route.get('safety_score', 85)}%"),
                    ft.Text(f"Distance: {self.current_route.get('distance_km', 3.5)} km"),
                    ft.Text(f"Estimated Time: {self.current_route.get('duration_min', 25)} min"),
                    ft.ProgressBar(width=300, value=0.1),  # Progress bar for the journey
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                "Stop Navigation",
                                icon=ft.icons.STOP,
                                on_click=self._stop_navigation
                            ),
                            ft.ElevatedButton(
                                "SOS",
                                icon=ft.icons.EMERGENCY,
                                color=ft.colors.RED,
                                on_click=self._trigger_emergency
                            ),
                            ft.ElevatedButton(
                                "Share Location",
                                icon=ft.icons.SHARE,
                                on_click=self._share_route
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )

            logger.info("Created tracking_info column")

            # Create a container for the tracking info
            tracking_container = ft.Container(
                content=tracking_info,
                padding=20,
                border_radius=10,
                border=ft.border.all(1, ft.colors.GREY_400),
                margin=ft.margin.only(top=20, bottom=20),
                width=None,
            )

            logger.info("Created tracking_container")

            # Create a dialog to show the live tracking
            dialog = ft.AlertDialog(
                title=ft.Text("Live Navigation"),
                content=tracking_container,
                actions=[
                    ft.TextButton("Close", on_click=self._stop_navigation),
                ],
            )
            logger.info("Created dialog")

            self.page.dialog = dialog
            logger.info("Set page.dialog")

            dialog.open = True
            logger.info("Set dialog.open = True")

            self.page.update()
            logger.info("Called page.update()")

            # Show success message
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Live navigation started"),
                action="OK",
            )
            self.page.snack_bar.open = True
            self.page.update()
            logger.info("Showed success message")

        except Exception as ex:
            logger.error(f"Error showing live tracking: {ex}")
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error: {str(ex)}"),
                action="OK",
            )
            self.page.snack_bar.open = True
            self.page.update()

    def _hide_live_tracking(self, e=None):
        """Hide the live tracking panel."""
        try:
            self.show_live_tracking = False

            # Set the panel to None
            self.live_tracking = None

            # Update the UI
            if hasattr(self, 'main_content') and self.main_content:
                # Remove any live tracking containers from main content
                new_controls = []
                for control in self.main_content.controls:
                    if isinstance(control, ft.Container) and hasattr(control, 'content'):
                        if not isinstance(control.content, LiveTracking):
                            new_controls.append(control)
                    else:
                        new_controls.append(control)
                self.main_content.controls = new_controls
            elif self.route_container and isinstance(self.route_container.content, ft.Column):
                # Remove the panel from the container
                new_controls = []
                for control in self.route_container.content.controls:
                    if isinstance(control, ft.Container) and hasattr(control, 'content'):
                        if not isinstance(control.content, LiveTracking):
                            new_controls.append(control)
                    elif not isinstance(control, LiveTracking):
                        new_controls.append(control)
                self.route_container.content.controls = new_controls

            # Show message
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Navigation stopped"),
                action="OK",
            )
            self.page.snack_bar.open = True
            self.page.update()

        except Exception as ex:
            logger.error(f"Error hiding live tracking: {ex}")
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error: {str(ex)}"),
                action="OK",
            )
            self.page.snack_bar.open = True
            self.page.update()

    def _display_route(self, route):
        """Display a route on the map and update UI."""
        try:
            if not route:
                return

            # Store the route as the current route
            self.current_route = route

            # Create alternative routes if needed
            if not hasattr(self, 'alternative_routes') or not self.alternative_routes:
                self.alternative_routes = []

                # Add the current route to the routes list if it's not already there
                if not self.routes:
                    self.routes = [route]
                elif route not in self.routes:
                    self.routes.append(route)

            # Update the UI to show the selected route
            self._update_route_display_with_ai_analysis(route, self.alternative_routes)

        except Exception as ex:
            logger.error(f"Error displaying route: {ex}")

    def _select_route(self, route_index):
        """Select a route from the comparison panel."""
        try:
            if 0 <= route_index < len(self.routes):
                self.current_route = self.routes[route_index]

                # Update the UI to show the selected route
                self._display_route(self.current_route)

                # Hide the comparison panel
                self._hide_route_comparison()

        except Exception as ex:
            logger.error(f"Error selecting route: {ex}")
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error: {str(ex)}"),
                action="OK",
            )
            self.page.snack_bar.open = True
            self.page.update()

    def _handle_map_click(self, lat, lon):
        """Handle map click events."""
        try:
            logger.info(f"Map clicked at: {lat}, {lon}")
            # You can add custom behavior here, like adding a marker
            if self.safety_map:
                self.safety_map.add_marker(lat, lon, "Selected Location")
                self.page.update()
        except Exception as ex:
            logger.error(f"Error handling map click: {ex}")

    def _handle_map_ready(self):
        """Handle map ready events."""
        try:
            logger.info("Map is ready")
            # You can add custom behavior here, like initializing the map
            if self.safety_map:
                self.safety_map.map_ready = True
                self.page.update()
        except Exception as ex:
            logger.error(f"Error handling map ready: {ex}")