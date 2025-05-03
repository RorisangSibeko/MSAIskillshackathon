import flet as ft
import os
import sys
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
env_path = Path(__file__).parent / "assets" / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

# Import app components
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
from app.screens.safe_route_screen import SafeRouteScreen
from app.screens.navigation_screen import NavigationScreen

from app.services.auth_service import AuthService
from app.services.panic_detector import PanicDetector
from app.services.location_service import LocationService
from app.services.notification_service import NotificationService
from app.services.subscription_service import SubscriptionService
from app.services.iot_service import IoTService
from app.services.security_service import SecurityService

from app.utils.theme import get_theme
from app.utils.logger import setup_logger

# Setup logger
logger = setup_logger()

class SafeWayAIApp:
    """Main application class for SafeWayAI."""

    def __init__(self, page: ft.Page):
        self.page = page
        self.init_app()

    def init_app(self):
        """Initialize the application."""
        # Set page properties
        self.page.title = "SafeWayAI - Safety & Emergency Detection"
        self.page.theme = get_theme()
        self.page.theme_mode = ft.ThemeMode.SYSTEM
        self.page.padding = 0
        self.page.window_width = 400
        self.page.window_height = 800
        self.page.window_resizable = True
        self.page.window_maximizable = True

        # Initialize services
        self.auth_service = AuthService()
        self.panic_detector = PanicDetector()
        self.location_service = LocationService()
        self.notification_service = NotificationService()
        self.subscription_service = SubscriptionService()
        self.iot_service = IoTService()
        self.security_service = SecurityService()

        # Initialize screens
        self.screens = {
            "/": HomeScreen(self),
            "/auth": AuthScreen(self),
            "/monitoring": MonitoringScreen(self),
            "/alerts": AlertsScreen(self),
            "/history": HistoryScreen(self),
            "/report": ReportScreen(self),
            "/settings": SettingsScreen(self),
            "/premium": PremiumScreen(self),
            "/iot": IoTScreen(self),
            "/gbv_resources": GBVResourcesScreen(self),
            "/safe_route": SafeRouteScreen(self),
            "/navigation": NavigationScreen(self),
            "/azure_demo": None,  # Will be handled specially in route_change
        }

        # Setup navigation
        self.setup_navigation()

        # Check authentication
        if not self.auth_service.is_authenticated():
            self.page.go("/auth")
        else:
            self.page.go("/")

    def setup_navigation(self):
        """Setup navigation and routing."""
        def route_change(e):
            route = self.page.route

            # Check if route requires authentication
            if route != "/auth" and not self.auth_service.is_authenticated():
                self.page.go("/auth")
                return

            # Special handling for Azure demo screen
            if route == "/azure_demo":
                self.page.views.clear()
                self.page.views.append(
                    ft.View(
                        route="/azure_demo",
                        controls=[azure_demo_screen(self.page)],
                        vertical_alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        padding=0
                    )
                )
                self.page.update()
                return

            # Get the screen for the current route
            screen = self.screens.get(route)
            if screen:
                self.page.views.clear()
                self.page.views.append(screen.build())
                self.page.update()
            else:
                # Handle 404
                self.page.go("/")

        self.page.on_route_change = route_change

        # Initialize with home route
        self.page.go(self.page.route)

def main():
    """Main entry point for the application."""
    ft.app(target=SafeWayAIApp)

if __name__ == "__main__":
    main()
