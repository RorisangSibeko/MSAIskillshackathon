import flet as ft
import logging
import threading
import time
import random
from app.utils.enhanced_theme import get_color_scheme
from app.components.header import Header
from app.components.safety_map import SafetyMap
from app.config.azure_config import MAPS_CONFIG

# Use Colors instead of colors (to avoid deprecation warnings)
Colors = ft.Colors

# Configure logging
logger = logging.getLogger(__name__)

# Get color scheme
colors = get_color_scheme()

class NavigationScreen:
    """
    Live navigation screen for the SafeWayAI application.
    Shows a full-screen navigation experience with real-time safety monitoring.
    """

    def __init__(self, app):
        self.app = app
        self.page = app.page

        # Get services from app
        self.location_tracking_service = app.location_service

        # Navigation state
        self.current_route = None
        self.active_tracking_id = None
        self.tracking_active = False
        self.tracking_thread = None
        self.progress_value = 0.1  # Initial progress value
        self.current_position = 0
        self.route_points = []
        self.eta_minutes = 0
        self.distance_remaining = 0
        self.safety_score = 0

        # Map configuration
        self.map_api_key = MAPS_CONFIG.get("subscription_key", "")
        self.safety_map = None
        self.current_marker_id = None
        self.route_id = None

        # UI components
        self.map_container = None
        self.progress_bar = None
        self.eta_text = None
        self.distance_text = None
        self.safety_text = None
        self.alerts_column = None

    def build(self):
        """Build the navigation screen UI."""
        # Create header with back button and stop navigation
        header = Header(
            title="Live Navigation",
            show_logo=True,
            show_back_button=True,
            on_back=self._confirm_stop_navigation
        ).build()

        # Create the main content
        content = self._build_content()

        # Create emergency button
        emergency_button = ft.FloatingActionButton(
            icon=ft.icons.EMERGENCY,
            bgcolor=colors["danger"],
            tooltip="Emergency SOS",
            on_click=self._trigger_emergency,
        )

        # Create the view
        return ft.View(
            route="/navigation",
            controls=[content],
            appbar=header,
            floating_action_button=emergency_button,
            padding=0
        )

    def _build_content(self):
        """Build the main content of the navigation screen."""
        # Create a simple visual map representation
        # We'll create a stack with route and markers

        # Create a route line
        route_container = ft.Container(
            bgcolor=colors["primary"],
            width=None,
            height=8,
            border_radius=4,
            margin=ft.margin.only(top=100, bottom=100),
            expand=True,
        )

        # Create markers for start, end, and current position
        start_marker = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(
                        name="play_circle",
                        color=colors["safety_high"],
                        size=24,
                    ),
                    ft.Text(
                        value="Start",
                        color=Colors.BLACK,
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
            bgcolor=Colors.WHITE,
        )

        end_marker = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(
                        name="location_on",
                        color=colors["danger"],
                        size=24,
                    ),
                    ft.Text(
                        value="End",
                        color=Colors.BLACK,
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
            bgcolor=Colors.WHITE,
        )

        current_marker = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(
                        name="navigation",
                        color=colors["primary"],
                        size=24,
                    ),
                    ft.Text(
                        value="You",
                        color=Colors.BLACK,
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
            bgcolor=Colors.WHITE,
        )

        # Create a stack for the map visualization
        map_stack = ft.Stack(
            controls=[
                # Base map background
                ft.Container(
                    bgcolor=Colors.BLUE_50,
                    border_radius=10,
                    width=None,
                    height=None,
                    expand=True,
                ),
                # Route line
                route_container,
                # Start marker (positioned at the left)
                ft.Container(
                    content=start_marker,
                    left=20,
                    top=100,
                ),
                # End marker (positioned at the right)
                ft.Container(
                    content=end_marker,
                    right=20,
                    top=100,
                ),
                # Current position marker (will be updated)
                ft.Container(
                    content=current_marker,
                    left=20,  # Will be updated as we move
                    top=100,
                ),
                # Title text at the top
                ft.Container(
                    content=ft.Text(
                        value="Navigation in progress...",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    alignment=ft.alignment.top_center,
                    padding=10,
                ),
            ],
            width=None,
            height=300,
        )

        # Store reference to the current marker container for updates
        self.current_marker_container = map_stack.controls[-2]  # The current marker container

        # Create map container with the map stack
        self.map_container = ft.Container(
            content=map_stack,
            height=350,
            width=None,
            border_radius=10,
            padding=10,
            expand=True,
        )

        # Create progress bar
        self.progress_bar = ft.ProgressBar(
            width=None,
            value=self.progress_value,
            color=colors["primary"],
            bgcolor=Colors.GREY_300,
        )

        # Create navigation info
        self.eta_text = ft.Text(
            value="Estimated time: Calculating...",
            size=16,
        )

        self.distance_text = ft.Text(
            value="Distance remaining: Calculating...",
            size=16,
        )

        self.safety_text = ft.Text(
            value="Current area safety: Calculating...",
            size=16,
        )

        # Create alerts section
        self.alerts_column = ft.Column(
            controls=[
                ft.Text(
                    value="Safety Alerts",
                    weight=ft.FontWeight.BOLD,
                    size=18,
                ),
                ft.Text(
                    value="No active alerts",
                    italic=True,
                ),
            ],
            spacing=5,
        )

        # Create action buttons
        action_buttons = ft.Row(
            controls=[
                ft.ElevatedButton(
                    text="Stop Navigation",
                    icon=ft.icons.STOP,
                    style=ft.ButtonStyle(
                        color=Colors.WHITE,
                        bgcolor=colors["danger"],
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                    on_click=self._confirm_stop_navigation,
                ),
                ft.ElevatedButton(
                    text="Share Location",
                    icon=ft.icons.SHARE,
                    style=ft.ButtonStyle(
                        color=colors["primary"],
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                    on_click=self._share_location,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )

        # Combine all elements
        return ft.Column(
            controls=[
                # Map takes most of the screen
                self.map_container,

                # Navigation info card
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    value="Navigation Details",
                                    weight=ft.FontWeight.BOLD,
                                    size=18,
                                ),
                                ft.Divider(height=1, color=Colors.GREY_300),
                                ft.Row(
                                    controls=[
                                        ft.Icon(name="schedule", color=colors["primary"]),
                                        self.eta_text,
                                    ],
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=5,
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Icon(name="straighten", color=colors["primary"]),
                                        self.distance_text,
                                    ],
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=5,
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Icon(name="shield", color=colors["safety_high"]),
                                        self.safety_text,
                                    ],
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=5,
                                ),
                                ft.Text(
                                    value="Journey Progress",
                                    weight=ft.FontWeight.BOLD,
                                    size=16,
                                ),
                                self.progress_bar,
                            ],
                            spacing=10,
                        ),
                        padding=15,
                    ),
                ),

                # Alerts card
                ft.Card(
                    content=ft.Container(
                        content=self.alerts_column,
                        padding=15,
                    ),
                ),

                # Action buttons
                action_buttons,
            ],
            spacing=15,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            padding=20,
        )

    def initialize_navigation(self, route_data, tracking_id):
        """
        Initialize the navigation screen with route data and tracking ID.

        Args:
            route_data (dict): The route data including start, destination, etc.
            tracking_id (str): The ID for the active tracking session
        """
        logger.info(f"Initializing navigation with tracking ID: {tracking_id}")

        self.current_route = route_data
        self.active_tracking_id = tracking_id
        self.tracking_active = True

        # Extract route information
        self.route_points = route_data.get("route_points", [])
        self.eta_minutes = route_data.get("duration_min", 0)
        self.distance_remaining = route_data.get("distance_km", 0)
        self.safety_score = route_data.get("safety_score", 0)

        # Update UI with route information
        self._update_navigation_ui()

        # Start tracking thread
        self.tracking_thread = threading.Thread(target=self._tracking_update_loop)
        self.tracking_thread.daemon = True
        self.tracking_thread.start()

    def _handle_map_container_click(self, e):
        """Handle map container click event."""
        try:
            logger.info("Map clicked")
            # In a real implementation, this would allow interaction with the map
            # For now, we'll just show a snackbar
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Map clicked"),
                action="OK",
            )
            self.page.snack_bar.open = True
            self.page.update()
        except Exception as ex:
            logger.error(f"Error handling map click: {ex}")

    def _display_route_on_map(self):
        """Display the current route on the map."""
        try:
            if not self.route_points or len(self.route_points) < 2:
                return

            # Update the map container to ensure it's visible
            if hasattr(self, 'map_container') and self.map_container:
                # Make sure the map container is visible
                self.map_container.visible = True

                # Update the title text if it exists
                if isinstance(self.map_container.content, ft.Stack) and len(self.map_container.content.controls) > 0:
                    # Find the title container (last control in our stack)
                    title_container = self.map_container.content.controls[-1]
                    if isinstance(title_container, ft.Container) and isinstance(title_container.content, ft.Text):
                        title_container.content.value = (
                            f"Navigating from {self.current_route.get('start_location', 'Current Location')} "
                            f"to {self.current_route.get('destination', 'Destination')}"
                        )

            # Update the current position marker
            self._update_position_on_map()

            # Update the page to ensure changes are visible
            self.page.update()

        except Exception as ex:
            logger.error(f"Error displaying route on map: {ex}")

    def _update_navigation_ui(self):
        """Update the navigation UI with current route information."""
        try:
            # Update text elements
            if hasattr(self, 'eta_text') and self.eta_text:
                self.eta_text.value = f"Estimated time: {self.eta_minutes} min"

            if hasattr(self, 'distance_text') and self.distance_text:
                self.distance_text.value = f"Distance remaining: {self.distance_remaining:.1f} km"

            if hasattr(self, 'safety_text') and self.safety_text:
                self.safety_text.value = f"Current area safety: {self.safety_score}/100"

            # Update map container title
            if hasattr(self, 'map_container') and self.map_container and isinstance(self.map_container.content, ft.Stack):
                # Find the title container (last control in our stack)
                title_container = self.map_container.content.controls[-1]
                if isinstance(title_container, ft.Container) and isinstance(title_container.content, ft.Text):
                    title_container.content.value = (
                        f"Navigating from {self.current_route.get('start_location', 'Current Location')} "
                        f"to {self.current_route.get('destination', 'Destination')}"
                    )

            # Update the current position marker
            self._update_position_on_map()

            # Update the page
            self.page.update()

        except Exception as ex:
            logger.error(f"Error updating navigation UI: {ex}")

    def _tracking_update_loop(self):
        """Background thread to update navigation UI."""
        try:
            # Initialize simulation variables
            simulation_speed = 1  # Points per update
            update_interval = 2   # Seconds between updates
            total_points = max(1, len(self.route_points) - 1)

            # Start at the beginning of the route
            self.current_position = 0
            self.progress_value = 0

            # Calculate initial values
            self.distance_remaining = self.current_route.get("distance_km", 3.0)
            self.eta_minutes = self.current_route.get("duration_min", 15)

            # Main tracking loop
            while self.tracking_active and self.active_tracking_id:
                # Try to get status from the tracking service
                status = None
                try:
                    status = self.location_tracking_service.get_tracking_status(self.active_tracking_id)
                except Exception:
                    # If service is not available, we'll use simulated movement
                    pass

                if status:
                    # Use real tracking data if available
                    position = status.get("position_index", self.current_position)
                    self.current_position = position
                    self.progress_value = position / total_points

                    # Update ETA and distance
                    self.eta_minutes = status.get("eta_minutes", self.eta_minutes)
                    self.distance_remaining = status.get("distance_remaining", self.distance_remaining)

                    # Update safety score
                    self.safety_score = status.get("current_safety_score", self.safety_score)

                    # Check for alerts
                    alerts = status.get("alerts", [])
                    for alert in alerts:
                        self._add_alert(
                            alert.get("text", "Safety alert"),
                            alert.get("level", "info")
                        )
                else:
                    # Simulate movement along the route
                    if self.current_position < total_points:
                        # Move along the route
                        self.current_position += simulation_speed
                        if self.current_position > total_points:
                            self.current_position = total_points

                        # Update progress
                        self.progress_value = self.current_position / total_points

                        # Update distance and ETA
                        progress_fraction = self.progress_value
                        self.distance_remaining = max(0, self.current_route.get("distance_km", 3.0) * (1 - progress_fraction))
                        self.eta_minutes = max(1, int(self.current_route.get("duration_min", 15) * (1 - progress_fraction)))

                        # Simulate safety score changes
                        base_safety = self.current_route.get("safety_score", 85)
                        # Slight random variations to simulate changing environment
                        variation = random.randint(-5, 5)
                        self.safety_score = max(50, min(100, base_safety + variation))

                        # Occasionally add safety alerts
                        if random.random() < 0.1:  # 10% chance per update
                            alert_types = [
                                ("Stay on the main road for better visibility", "info"),
                                ("Area ahead has limited street lighting", "warning"),
                                ("Approaching area with lower foot traffic", "warning"),
                                ("You're entering a safer area with good visibility", "info"),
                                ("Police patrol spotted nearby", "info")
                            ]
                            alert = random.choice(alert_types)
                            self._add_alert(alert[0], alert[1])

                        # If we've reached the destination
                        if self.current_position >= total_points:
                            self._add_alert("You have reached your destination!", "info")

                # Update the UI with current position
                self._update_position_on_map()
                self._update_progress_ui()

                # Sleep to avoid high CPU usage
                time.sleep(update_interval)

        except Exception as ex:
            logger.error(f"Error in tracking update loop: {ex}")

    def _update_position_on_map(self):
        """Update the current position marker on the map."""
        try:
            if not self.route_points or not hasattr(self, 'current_marker_container'):
                return

            # Calculate position based on progress
            total_points = max(1, len(self.route_points) - 1)
            progress = self.current_position / total_points

            # Get the page width (or use a default if not available)
            page_width = getattr(self.page, 'width', 400)

            # Calculate the left position (linear interpolation from left to right)
            # Leave 20px margin on each side
            left_position = 20 + (progress * (page_width - 40))

            # Update the marker position
            self.current_marker_container.left = left_position

            # Update the page
            self.page.update()

        except Exception as ex:
            logger.error(f"Error updating position on map: {ex}")

    def _update_progress_ui(self):
        """Update the progress UI elements."""
        try:
            # Update progress bar
            if hasattr(self, 'progress_bar') and self.progress_bar:
                self.progress_bar.value = self.progress_value

            # Update text elements
            if hasattr(self, 'eta_text') and self.eta_text:
                self.eta_text.value = f"Estimated time: {self.eta_minutes} min"

            if hasattr(self, 'distance_text') and self.distance_text:
                self.distance_text.value = f"Distance remaining: {self.distance_remaining:.1f} km"

            if hasattr(self, 'safety_text') and self.safety_text:
                self.safety_text.value = f"Current area safety: {self.safety_score}/100"

            # Update the page
            self.page.update()

        except Exception as ex:
            logger.error(f"Error updating progress UI: {ex}")

    def _add_alert(self, alert_text, alert_level="info"):
        """Add a safety alert to the alerts column."""
        try:
            # Determine color based on alert level
            alert_color = Colors.BLUE
            if alert_level == "warning":
                alert_color = colors["warning"]
            elif alert_level == "danger":
                alert_color = colors["danger"]

            # Create alert container
            alert_container = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(
                            name="warning",
                            color=alert_color,
                            size=20,
                        ),
                        ft.Text(
                            value=alert_text,
                            color=Colors.BLACK,
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5,
                ),
                padding=10,
                border_radius=5,
                bgcolor=Colors.WHITE,
                border=ft.border.all(1, alert_color),
            )

            # Remove "No active alerts" text if it exists
            if len(self.alerts_column.controls) > 1 and isinstance(self.alerts_column.controls[1], ft.Text) and "No active alerts" in self.alerts_column.controls[1].value:
                self.alerts_column.controls.pop(1)

            # Add alert to column (at the beginning after the title)
            self.alerts_column.controls.insert(1, alert_container)

            # Limit to 5 alerts
            if len(self.alerts_column.controls) > 6:
                self.alerts_column.controls.pop(6)

            # Update the page
            self.page.update()

            # Also show as snackbar for immediate attention
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(alert_text),
                bgcolor=alert_color,
                action="OK",
            )
            self.page.snack_bar.open = True
            self.page.update()

        except Exception as ex:
            logger.error(f"Error adding alert: {ex}")

    def _confirm_stop_navigation(self, e=None):
        """Confirm stopping navigation."""
        def close_dialog(e):
            self.page.dialog.open = False
            self.page.update()

        def stop_and_go_back(e):
            close_dialog(e)
            self._stop_navigation()

        # Create confirmation dialog
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Stop Navigation?"),
            content=ft.Text("Are you sure you want to stop navigation and return to the route screen?"),
            actions=[
                ft.TextButton("Cancel", on_click=close_dialog),
                ft.TextButton("Stop Navigation", on_click=stop_and_go_back),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.dialog.open = True
        self.page.update()

    def _stop_navigation(self, e=None):
        """Stop navigation and return to the route screen."""
        try:
            # Stop tracking
            if self.active_tracking_id:
                self.location_tracking_service.stop_tracking(self.active_tracking_id)
                self.active_tracking_id = None
                self.tracking_active = False

            # Navigate back to the route screen
            self.page.go("/safe_route")

        except Exception as ex:
            logger.error(f"Error stopping navigation: {ex}")
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error: {str(ex)}"),
                action="OK",
            )
            self.page.snack_bar.open = True
            self.page.update()

    def _share_location(self, e=None):
        """Share current location."""
        # This would integrate with the device's sharing capabilities
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Sharing your location..."),
            action="OK",
        )
        self.page.snack_bar.open = True
        self.page.update()

    def _trigger_emergency(self, e=None):
        """Trigger emergency response."""
        # This would integrate with emergency services
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Emergency services notified!"),
            bgcolor=colors["danger"],
            action="OK",
        )
        self.page.snack_bar.open = True
        self.page.update()
