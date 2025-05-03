import flet as ft
from typing import Any, Dict, List, Optional
from app.utils.enhanced_theme import get_color_scheme, apply_text_style
from app.components.header import Header
from app.components.footer import Footer
from app.components.card_templates import feature_card, status_card, action_button, social_impact_banner

class HomeScreen:
    """Home screen for the SafeWayAI application."""

    def __init__(self, app):
        self.app = app
        self.colors = get_color_scheme()

    def build(self) -> ft.View:
        """Build the home screen UI."""
        # Get user information
        user = self.app.auth_service.get_current_user()
        user_name = user.get("full_name", "User") if user else "User"
        subscription_tier = self.app.auth_service.get_subscription_tier()

        # Create main content
        content = ft.Column(
            spacing=20,
            controls=[
                # Header with welcome message
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"Welcome, {user_name}", size=24, weight=ft.FontWeight.BOLD),
                        ft.Text("Stay safe with SafeWayAI", size=16, color=ft.colors.GREY_700)
                    ]),
                    padding=ft.padding.only(left=20, right=20, top=20, bottom=10)
                ),

                # Social impact banner
                social_impact_banner(
                    message="AI for social good - Making communities safer together",
                    icon="favorite",
                    color=self.colors["primary"]
                ),

                # Safe Route Finder Card
                feature_card(
                    title="Find Safest Route",
                    description="Let AI determine the safest route to your destination based on real-time safety data",
                    icon=ft.icons.ROUTE,
                    color=self.colors["route_finder"],
                    button_text="Find Safe Route",
                    on_click=lambda _: self.app.page.go("/safe_route")
                ),

                # Safety status card
                status_card(
                    status="All systems operational",
                    last_check="Just now",
                    icon=ft.icons.SHIELD,
                    color=self.colors["safety_high"]
                ),

                # Quick action buttons
                ft.Container(
                    content=ft.Column([
                        ft.Text("Quick Actions", weight=ft.FontWeight.BOLD, size=18),
                        ft.Row([
                            action_button(
                                "visibility",
                                "Monitor",
                                self.colors["monitoring"],
                                lambda _: self.app.page.go("/monitoring")
                            ),
                            action_button(
                                "report_problem",
                                "Report",
                                self.colors["warning"],
                                lambda _: self.app.page.go("/report")
                            ),
                            action_button(
                                "notifications_active",
                                "Alerts",
                                self.colors["alerts"],
                                lambda _: self.app.page.go("/alerts")
                            ),
                            action_button(
                                "history",
                                "History",
                                self.colors["secondary"],
                                lambda _: self.app.page.go("/history")
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    ]),
                    padding=ft.padding.only(left=20, right=20)
                ),

                # Azure Demo Card
                ft.Container(
                    content=feature_card(
                        title="Azure AI Services Demo",
                        description="Experience the power of Azure AI services for safety and emergency detection",
                        icon=ft.icons.CLOUD,
                        color=self.colors["primary"],
                        button_text="Try Azure Demo",
                        on_click=lambda _: self.app.page.go("/azure_demo")
                    ),
                    padding=ft.padding.only(left=20, right=20)
                ),

                # GBV Resources (if available in subscription)
                ft.Container(
                    content=ft.Column([
                        ft.Text("Safety Resources", weight=ft.FontWeight.BOLD, size=18),
                        feature_card(
                            title="Gender-Based Violence Resources",
                            description="Access safety plans, hotlines, and support resources for GBV prevention",
                            icon=ft.icons.HEALTH_AND_SAFETY,
                            color=self.colors["gbv_resources"],
                            button_text="Access Resources",
                            on_click=lambda _: self.app.page.go("/gbv_resources")
                        )
                    ]),
                    padding=ft.padding.only(left=20, right=20),
                    visible=subscription_tier in ["standard", "premium", "enterprise"]
                ),

                # IoT Integration (if available in subscription)
                ft.Container(
                    content=ft.Column([
                        ft.Text("Smart Home Integration", weight=ft.FontWeight.BOLD, size=18),
                        feature_card(
                            title="IoT Device Management",
                            description="Manage connected security devices and systems for enhanced protection",
                            icon=ft.icons.SMART_TOY,
                            color=self.colors["iot_devices"],
                            button_text="Manage Devices",
                            on_click=lambda _: self.app.page.go("/iot")
                        )
                    ]),
                    padding=ft.padding.only(left=20, right=20),
                    visible=subscription_tier in ["premium", "enterprise"]
                ),

                # Upgrade banner (if not on premium)
                ft.Container(
                    content=feature_card(
                        title="Upgrade for Enhanced Protection",
                        description="Get IoT integration, insurance benefits, and more safety features",
                        icon=ft.icons.WORKSPACE_PREMIUM,
                        color=self.colors["secondary"],
                        button_text="View Premium Features",
                        on_click=lambda _: self.app.page.go("/premium")
                    ),
                    padding=ft.padding.only(left=20, right=20, bottom=20),
                    visible=subscription_tier not in ["premium", "enterprise"]
                )
            ],
            scroll=ft.ScrollMode.AUTO
        )

        # Create header with logo
        header = Header(
            title="SafeWayAI",
            show_logo=True,
            actions=[
                ft.IconButton(
                    icon=ft.icons.ACCOUNT_CIRCLE,
                    tooltip="Profile",
                    icon_color=ft.colors.WHITE,
                ),
            ]
        ).build()

        # Create footer with navigation bar
        footer = Footer(
            selected_index=0,
            on_change=self._handle_nav_change,
        )

        # Create emergency button
        emergency_button = ft.FloatingActionButton(
            icon=ft.icons.EMERGENCY,
            bgcolor=self.colors["danger"],
            tooltip="Emergency",
            on_click=self._handle_emergency,
        )

        # Create the view
        return ft.View(
            route="/",
            controls=[content],
            appbar=header,
            navigation_bar=footer.build_navigation_bar(),
            floating_action_button=emergency_button,
            padding=0
        )



    def _handle_nav_change(self, e):
        """Handle navigation bar selection changes."""
        index = e.control.selected_index

        if index == 0:
            self.app.page.go("/")
        elif index == 1:
            self.app.page.go("/safe_route")
        elif index == 2:
            self.app.page.go("/report")
        elif index == 3:
            self.app.page.go("/alerts")
        elif index == 4:
            self.app.page.go("/settings")

    def _handle_emergency(self, e):
        """Handle emergency button press."""
        self.app.page.dialog = ft.AlertDialog(
            title=ft.Text("Emergency Alert"),
            content=ft.Text("Emergency services have been notified. Stay calm and follow safety instructions."),
            actions=[
                ft.TextButton("Cancel Alert", on_click=self._close_dialog),
                ft.TextButton("Call Emergency Services", on_click=self._call_emergency),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.app.page.dialog.open = True
        self.app.page.update()

    def _close_dialog(self, e):
        """Close the dialog."""
        self.app.page.dialog.open = False
        self.app.page.update()

    def _call_emergency(self, e):
        """Call emergency services."""
        # This would initiate a call in a real implementation
        self.app.page.dialog.open = False
        self.app.page.update()
