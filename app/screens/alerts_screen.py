import flet as ft
from typing import Any, Dict, List, Optional

class AlertsScreen:
    """Alerts screen for the SafeWayAI application."""
    
    def __init__(self, app):
        self.app = app
        
    def build(self) -> ft.View:
        """Build the alerts screen UI."""
        # Create placeholder content
        content = ft.Column(
            controls=[
                ft.Text("Emergency Alerts", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("This screen would show emergency alerts.")
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        # Create the view
        return ft.View(
            route="/alerts",
            controls=[content],
            appbar=ft.AppBar(
                title=ft.Text("Emergency Alerts"),
                center_title=True,
                bgcolor=ft.colors.SURFACE_VARIANT,
                leading=ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    on_click=lambda _: self.app.page.go("/")
                )
            )
        )
