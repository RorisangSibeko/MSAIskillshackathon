"""
Azure services demo screen for SafeWayAI application.
This module provides a demonstration of the Azure services integration.
"""

import logging
import time
import flet as ft
from app.services.ui_integration import UIIntegrationService
from app.components.header import Header
from app.components.footer import Footer

logger = logging.getLogger(__name__)

def azure_demo_screen(page: ft.Page):
    """
    Create the Azure services demo screen.

    Args:
        page: The Flet page

    Returns:
        The screen content
    """
    # Initialize UI integration service
    ui_service = UIIntegrationService()
    ui_service.set_page(page)

    # Create safety status card
    safety_status = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(
                        name=ft.icons.SHIELD,
                        color=ft.colors.BLUE_GREY,
                        size=40
                    ),
                    ft.Text(
                        value="Safety Status",
                        weight=ft.FontWeight.BOLD,
                        size=20
                    )
                ]),
                ft.Text(
                    value="Checking safety...",
                    size=16
                ),
                ft.ProgressBar(
                    value=0.5,
                    width=300
                )
            ]),
            padding=20
        )
    )

    # Register safety status card for updates
    ui_service.register_safety_status_control(safety_status.content.content.controls[1])  # Text
    ui_service.register_safety_status_control(safety_status.content.content.controls[0].controls[0])  # Icon

    # Create emergency alert card
    emergency_alert = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(
                        name=ft.icons.WARNING_AMBER_ROUNDED,
                        color=ft.colors.RED,
                        size=40
                    ),
                    ft.Text(
                        value="EMERGENCY ALERT",
                        weight=ft.FontWeight.BOLD,
                        size=20,
                        color=ft.colors.RED
                    )
                ]),
                ft.Text(
                    value="Emergency detected",
                    size=16
                ),
                ft.ElevatedButton(
                    text="Dismiss",
                    on_click=lambda e: setattr(emergency_alert, "visible", False)
                )
            ]),
            padding=20,
            bgcolor=ft.colors.RED_50
        ),
        visible=False
    )

    # Register emergency alert card for updates
    ui_service.register_emergency_alert_control(emergency_alert)
    ui_service.register_emergency_alert_control(emergency_alert.content.content.controls[1])  # Text

    # Create route finder
    start_location = ft.TextField(
        label="Start Location",
        hint_text="Enter start location",
        value="Current Location"
    )

    end_location = ft.TextField(
        label="Destination",
        hint_text="Enter destination"
    )

    route_map = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text(
                    value="Route Information",
                    weight=ft.FontWeight.BOLD,
                    size=18
                ),
                ft.Text(
                    value="Enter start and destination to find a safe route",
                    size=14
                )
            ]),
            padding=20,
            width=300,
            height=200
        )
    )

    # Register route map for updates
    ui_service.register_route_map_control(route_map)

    def find_route(e):
        """Find a safe route."""
        try:
            # Get start and end locations
            if start_location.value == "Current Location":
                start = ui_service.location_service.get_current_location()
            else:
                # In a real implementation, this would geocode the address
                start = {"latitude": 37.7749, "longitude": -122.4194}

            # For the demo, we'll use a fixed end location
            end = {"latitude": 37.7833, "longitude": -122.4167}

            # Update route map
            ui_service.update_route_map(start, end)

        except Exception as ex:
            logger.error(f"Error finding route: {ex}")
            page.show_snack_bar(ft.SnackBar(content=ft.Text(f"Error: {str(ex)}")))

    # Create incident list
    incident_list = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text(
                    value="Recent Incidents",
                    weight=ft.FontWeight.BOLD,
                    size=18
                ),
                ft.Column([
                    ft.Text(
                        value="No incidents to display",
                        size=14,
                        italic=True
                    )
                ])
            ]),
            padding=20,
            width=300,
            height=300,
            scroll=ft.ScrollMode.AUTO
        )
    )

    # Register incident list for updates
    ui_service.register_incident_list_control(incident_list.content.content.controls[1])

    def report_incident(e):
        """Report a new incident."""
        try:
            # Create incident data
            incident_data = {
                "type": "incident",
                "incident_type": "suspicious_activity",
                "severity": 6,
                "status": "reported",
                "description": "Suspicious person loitering in the area",
                "latitude": 37.7749,
                "longitude": -122.4194,
                "timestamp": time.time()
            }

            # Report the incident
            result = ui_service.report_incident(incident_data)

            if "error" in result:
                raise Exception(result["error"])

            # Show success message
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Incident reported successfully")))

        except Exception as ex:
            logger.error(f"Error reporting incident: {ex}")
            page.show_snack_bar(ft.SnackBar(content=ft.Text(f"Error: {str(ex)}")))

    def report_emergency(e):
        """Report an emergency."""
        try:
            # Create emergency data
            emergency_data = {
                "type": "manual_emergency",
                "emergency_type": "personal_safety",
                "description": "I feel unsafe and need assistance",
                "latitude": 37.7749,
                "longitude": -122.4194,
                "timestamp": time.time()
            }

            # Report the emergency
            result = ui_service.report_emergency(emergency_data)

            if "error" in result:
                raise Exception(result["error"])

            # Show success message
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Emergency reported successfully")))

            # Make emergency alert visible
            emergency_alert.visible = True
            page.update()

        except Exception as ex:
            logger.error(f"Error reporting emergency: {ex}")
            page.show_snack_bar(ft.SnackBar(content=ft.Text(f"Error: {str(ex)}")))

    def get_safe_places(e):
        """Get nearby safe places."""
        try:
            # Get nearby safe places
            safe_places = ui_service.get_nearby_safe_places()

            # Show in a dialog
            safe_places_list = ft.Column([
                ft.Text(
                    value="Nearby Safe Places",
                    weight=ft.FontWeight.BOLD,
                    size=18
                )
            ])

            for place in safe_places:
                safe_places_list.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Text(
                                value=place["name"],
                                weight=ft.FontWeight.BOLD,
                                size=16
                            ),
                            ft.Text(
                                value=f"Type: {place['type']}",
                                size=14
                            ),
                            ft.Text(
                                value=f"Distance: {place['distance']:.1f} km",
                                size=14
                            )
                        ]),
                        padding=10,
                        margin=ft.margin.only(bottom=5),
                        border=ft.border.all(1, ft.colors.GREY_300),
                        border_radius=5
                    )
                )

            # Show dialog
            page.dialog = ft.AlertDialog(
                title=ft.Text("Nearby Safe Places"),
                content=ft.Container(
                    content=safe_places_list,
                    width=300,
                    height=400,
                    scroll=ft.ScrollMode.AUTO
                ),
                actions=[
                    ft.TextButton("Close", on_click=lambda e: setattr(page.dialog, "open", False))
                ]
            )
            page.dialog.open = True
            page.update()

        except Exception as ex:
            logger.error(f"Error getting safe places: {ex}")
            page.show_snack_bar(ft.SnackBar(content=ft.Text(f"Error: {str(ex)}")))

    # Start safety monitoring
    ui_service.start_safety_monitoring()

    # Create the screen content
    content = ft.Column([
        # Header
        Header(title="Azure Services Demo").build(),

        # Main content
        ft.Container(
            content=ft.Column([
                # Title
                ft.Text(
                    value="Azure Services Demo",
                    weight=ft.FontWeight.BOLD,
                    size=24,
                    text_align=ft.TextAlign.CENTER
                ),

                # Emergency alert
                emergency_alert,

                # Safety status
                safety_status,

                # Route finder
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(
                                value="Safe Route Finder",
                                weight=ft.FontWeight.BOLD,
                                size=18
                            ),
                            start_location,
                            end_location,
                            ft.ElevatedButton(
                                text="Find Safe Route",
                                on_click=find_route
                            ),
                            route_map
                        ]),
                        padding=20
                    )
                ),

                # Incident reporting
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(
                                value="Safety Actions",
                                weight=ft.FontWeight.BOLD,
                                size=18
                            ),
                            ft.Row([
                                ft.ElevatedButton(
                                    text="Report Incident",
                                    icon=ft.icons.REPORT_PROBLEM,
                                    on_click=report_incident
                                ),
                                ft.ElevatedButton(
                                    text="Emergency Alert",
                                    icon=ft.icons.WARNING,
                                    color=ft.colors.WHITE,
                                    bgcolor=ft.colors.RED,
                                    on_click=report_emergency
                                )
                            ]),
                            ft.Row([
                                ft.ElevatedButton(
                                    text="Find Safe Places",
                                    icon=ft.icons.LOCATION_ON,
                                    on_click=get_safe_places
                                ),
                                ft.ElevatedButton(
                                    text="Share Location",
                                    icon=ft.icons.SHARE_LOCATION,
                                    on_click=lambda e: page.show_snack_bar(
                                        ft.SnackBar(content=ft.Text("Location shared with emergency contacts"))
                                    )
                                )
                            ])
                        ]),
                        padding=20
                    )
                ),

                # Incident list
                incident_list
            ]),
            padding=20,
            scroll=ft.ScrollMode.AUTO
        ),

        # Footer
        Footer().build_navigation_bar()
    ])

    return content
