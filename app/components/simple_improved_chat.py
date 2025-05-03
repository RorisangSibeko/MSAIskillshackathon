"""
Simple improved chat interface for SafeWayAI application.
"""

import flet as ft
import logging
from app.utils.enhanced_theme import get_color_scheme

# Configure logging
logger = logging.getLogger(__name__)

# Get color scheme
colors = get_color_scheme()

def create_quick_actions_panel():
    """
    Create a panel with quick action buttons for emergency and safety features.
    
    Returns:
        ft.Control: The quick actions panel
    """
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.ElevatedButton(
                    content=ft.Row(
                        controls=[
                            ft.Icon(
                                name=ft.icons.WARNING_ROUNDED,
                                color=ft.colors.WHITE,
                            ),
                            ft.Text(
                                "Emergency",
                                color=ft.colors.WHITE,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                        spacing=5,
                    ),
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        padding=ft.padding.all(15),
                        bgcolor=colors["danger"],
                    ),
                    tooltip="Report Emergency",
                ),
                ft.ElevatedButton(
                    content=ft.Row(
                        controls=[
                            ft.Icon(
                                name=ft.icons.REPORT_PROBLEM,
                                color=ft.colors.WHITE,
                            ),
                            ft.Text(
                                "Report",
                                color=ft.colors.WHITE,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                        spacing=5,
                    ),
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        padding=ft.padding.all(15),
                        bgcolor=colors["warning"],
                    ),
                    tooltip="Report Incident",
                ),
                ft.ElevatedButton(
                    content=ft.Row(
                        controls=[
                            ft.Icon(
                                name=ft.icons.DIRECTIONS,
                                color=ft.colors.WHITE,
                            ),
                            ft.Text(
                                "Safe Route",
                                color=ft.colors.WHITE,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                        spacing=5,
                    ),
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        padding=ft.padding.all(15),
                        bgcolor=colors["primary"],
                    ),
                    tooltip="Find Safe Route",
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing=10,
        ),
        padding=ft.padding.all(15),
        border_radius=10,
        bgcolor=ft.colors.SURFACE_VARIANT,
        margin=ft.margin.only(bottom=15),
    )

def create_safety_status_card():
    """
    Create a card showing the current safety status and key metrics.
    
    Returns:
        ft.Control: The safety status card
    """
    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(
                                name=ft.icons.SHIELD,
                                color=colors["primary"],
                                size=28,
                            ),
                            ft.Text(
                                value="Safety Status",
                                weight=ft.FontWeight.BOLD,
                                size=18,
                            ),
                            ft.Container(
                                content=ft.Text(
                                    "MODERATE",
                                    color=ft.colors.WHITE,
                                    weight=ft.FontWeight.BOLD,
                                    size=12,
                                ),
                                bgcolor=colors["warning"],
                                padding=ft.padding.symmetric(horizontal=10, vertical=5),
                                border_radius=15,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Divider(height=1, color=ft.colors.GREY_300),
                    ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        "3",
                                        size=24,
                                        weight=ft.FontWeight.BOLD,
                                        color=colors["primary"],
                                    ),
                                    ft.Text(
                                        "Recent Alerts",
                                        size=12,
                                    ),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=5,
                            ),
                            ft.VerticalDivider(
                                width=1,
                                color=ft.colors.GREY_300,
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        "72%",
                                        size=24,
                                        weight=ft.FontWeight.BOLD,
                                        color=colors["primary"],
                                    ),
                                    ft.Text(
                                        "Safety Score",
                                        size=12,
                                    ),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=5,
                            ),
                            ft.VerticalDivider(
                                width=1,
                                color=ft.colors.GREY_300,
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        "5",
                                        size=24,
                                        weight=ft.FontWeight.BOLD,
                                        color=colors["primary"],
                                    ),
                                    ft.Text(
                                        "Safe Routes",
                                        size=12,
                                    ),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=5,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        spacing=10,
                    ),
                ],
                spacing=15,
            ),
            padding=20,
            border_radius=10,
        ),
        elevation=3,
        margin=ft.margin.only(bottom=15),
    )
