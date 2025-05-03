import flet as ft
from app.utils.enhanced_theme import get_color_scheme

colors = get_color_scheme()

class Footer:
    """
    A consistent footer component for all screens in the SafeWayAI app.
    Includes navigation bar and optional floating action button.
    """

    def __init__(self, selected_index=0, on_change=None, fab=None):
        """
        Initialize the footer component.

        Args:
            selected_index (int): The index of the selected navigation item.
            on_change (callable): Function to call when navigation changes.
            fab (ft.FloatingActionButton): Optional floating action button.
        """
        self.selected_index = selected_index
        self.on_change = on_change
        self.fab = fab

    def build_navigation_bar(self):
        """Build the navigation bar."""
        return ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(
                    icon=ft.icons.HOME_OUTLINED,
                    selected_icon=ft.icons.HOME,
                    label="Home"
                ),
                ft.NavigationBarDestination(
                    icon=ft.icons.ROUTE_OUTLINED,
                    selected_icon=ft.icons.ROUTE,
                    label="Routes"
                ),
                ft.NavigationBarDestination(
                    icon=ft.icons.REPORT_PROBLEM_OUTLINED,
                    selected_icon=ft.icons.REPORT_PROBLEM,
                    label="Report"
                ),
                ft.NavigationBarDestination(
                    icon=ft.icons.NOTIFICATIONS_OUTLINED,
                    selected_icon=ft.icons.NOTIFICATIONS,
                    label="Alerts"
                ),
                ft.NavigationBarDestination(
                    icon=ft.icons.SETTINGS_OUTLINED,
                    selected_icon=ft.icons.SETTINGS,
                    label="Settings"
                ),
            ],
            selected_index=self.selected_index,
            on_change=self.on_change,
            height=65,
            bgcolor=ft.colors.WHITE,
            elevation=8,
        )

    def build_fab(self):
        """Build the floating action button."""
        if not self.fab:
            return ft.FloatingActionButton(
                icon=ft.icons.EMERGENCY,
                bgcolor=colors["danger"],
                tooltip="Emergency",
            )
        return self.fab
