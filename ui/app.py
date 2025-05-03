import flet as ft
import os
import sys
from pathlib import Path
from app.screens.home_screen import HomeScreen
from app.screens.monitoring_screen import MonitoringScreen
from app.screens.alerts_screen import AlertsScreen
from app.screens.history_screen import HistoryScreen
from app.screens.report_screen import ReportScreen
from app.screens.settings_screen import SettingsScreen
from app.screens.auth_screen import AuthScreen
from app.screens.premium_screen import PremiumScreen
from app.screens.iot_screen import IoTScreen
from app.screens.gbv_resources_screen import GBVResourcesScreen
from app.screens.azure_demo import azure_demo_screen

from app.services.auth_service import AuthService
from app.services.panic_detector import PanicDetector
from app.services.location_service import LocationService
from app.services.notification_service import NotificationService
from app.services.subscription_service import SubscriptionService
from app.services.iot_service import IoTService
from app.services.security_service import SecurityService
from app.services.gbv_service import GBVService
from app.services.ui_integration import UIIntegrationService

from app.utils.theme import get_theme

class SafeWayAIApp:
    """Main UI class for SafeWayAI application."""

    def __init__(self, page: ft.Page):
        self.page = page
        self.init_app()

    def init_app(self):
        """Initialize the application UI."""
        # Set page properties
        self.page.title = "SafeWayAI - Safety & Emergency Detection"
        self.page.theme = get_theme()
        self.page.theme_mode = ft.ThemeMode.SYSTEM
        self.page.padding = 0

        # Set mobile-friendly window settings
        self.page.window_width = 400  # Simulate mobile width for development
        self.page.window_min_width = 350
        self.page.window_max_width = 500  # Limit max width for mobile-like experience

        # Initialize services
        self.auth_service = AuthService()
        self.panic_detector = PanicDetector()
        self.location_service = LocationService()
        self.notification_service = NotificationService()
        self.subscription_service = SubscriptionService()
        self.iot_service = IoTService()
        self.security_service = SecurityService()
        self.gbv_service = GBVService()

        # Setup navigation
        self.setup_navigation()

        # Initialize with auth route
        self.page.go("/auth")

    def setup_navigation(self):
        """Setup navigation and routing."""
        def route_change(e):
            self.page.views.clear()

            if self.page.route == "/":
                self.page.views.append(HomeScreen(self).build())
            elif self.page.route == "/auth":
                self.page.views.append(AuthScreen(self).build())
            elif self.page.route == "/monitoring":
                self.page.views.append(MonitoringScreen(self).build())
            elif self.page.route == "/alerts":
                self.page.views.append(AlertsScreen(self).build())
            elif self.page.route == "/history":
                self.page.views.append(HistoryScreen(self).build())
            elif self.page.route == "/report":
                self.page.views.append(ReportScreen(self).build())
            elif self.page.route == "/settings":
                self.page.views.append(SettingsScreen(self).build())
            elif self.page.route == "/premium":
                self.page.views.append(PremiumScreen(self).build())
            elif self.page.route == "/iot":
                self.page.views.append(IoTScreen(self).build())
            elif self.page.route == "/gbv_resources":
                self.page.views.append(GBVResourcesScreen(self).build())
            elif self.page.route == "/safe_route":
                # Import here to avoid circular imports
                from app.screens.safe_route_screen import SafeRouteScreen
                self.page.views.append(SafeRouteScreen(self).build())
            elif self.page.route == "/navigation":
                # Import here to avoid circular imports
                from app.screens.navigation_screen import NavigationScreen
                self.page.views.append(NavigationScreen(self).build())
            elif self.page.route == "/azure_demo":
                # Azure services demo screen
                self.page.views.append(
                    ft.View(
                        route="/azure_demo",
                        controls=[azure_demo_screen(self.page)],
                        vertical_alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        padding=0
                    )
                )
            else:
                # Handle 404
                self.page.views.append(HomeScreen(self).build())

            self.page.update()

        self.page.on_route_change = route_change
