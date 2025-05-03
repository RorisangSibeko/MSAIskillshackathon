import flet as ft
from typing import Any, Dict, List, Optional

class ReportScreen:
    """Emergency reporting screen for the SafeWayAI application."""
    
    def __init__(self, app):
        self.app = app
        
    def build(self) -> ft.View:
        """Build the report screen UI."""
        # Create placeholder content
        content = ft.Column(
            controls=[
                ft.Text("Report Emergency", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("This screen would allow reporting emergencies.")
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        # Create the view
        return ft.View(
            route="/report",
            controls=[content],
            appbar=ft.AppBar(
                title=ft.Text("Report Emergency"),
                center_title=True,
                bgcolor=ft.colors.SURFACE_VARIANT,
                leading=ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    on_click=lambda _: self.app.page.go("/")
                )
            )
        )
