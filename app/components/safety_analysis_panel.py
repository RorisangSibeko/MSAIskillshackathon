"""
Safety Analysis Panel Component for SafeWayAI application.
This module provides a detailed breakdown of safety factors for routes.
"""

import flet as ft
import logging
from app.utils.enhanced_theme import get_color_scheme

colors = get_color_scheme()
logger = logging.getLogger(__name__)

class SafetyAnalysisPanel(ft.Container):
    """Detailed safety analysis panel component."""
    
    def __init__(self, 
                 safety_data=None, 
                 width=None, 
                 height=None,
                 on_close=None):
        """
        Initialize the safety analysis panel.
        
        Args:
            safety_data (dict): Safety analysis data
            width (int, optional): Panel width
            height (int, optional): Panel height
            on_close (function, optional): Callback when panel is closed
        """
        self.safety_data = safety_data or {}
        self.on_close = on_close
        
        # Create the header
        header = ft.Row(
            controls=[
                ft.Text(
                    value="Detailed Safety Analysis",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.IconButton(
                    icon=ft.icons.CLOSE,
                    tooltip="Close",
                    on_click=self._handle_close,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        
        # Create the overall safety score display
        safety_score = self.safety_data.get("overall_score", 0)
        overall_score = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        value="Overall Safety Score",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Text(
                                    value=f"{safety_score}",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=self._get_safety_color(safety_score),
                                ),
                                padding=10,
                            ),
                            ft.Column(
                                controls=[
                                    ft.Container(
                                        content=ft.ProgressBar(
                                            width=200,
                                            value=safety_score / 100,
                                            color=self._get_safety_color(safety_score),
                                            bgcolor=ft.colors.GREY_300,
                                        ),
                                    ),
                                    ft.Text(
                                        value=self._get_safety_description(safety_score),
                                        size=14,
                                        italic=True,
                                    ),
                                ],
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                ],
                spacing=5,
            ),
            padding=10,
            border_radius=10,
            bgcolor=ft.colors.BLUE_50,
        )
        
        # Create the safety factors breakdown
        factors = self.safety_data.get("factors", {})
        factors_list = ft.ListView(
            controls=self._create_factor_items(factors),
            spacing=2,
            height=200,
        )
        
        # Create the safety insights section
        insights = self.safety_data.get("insights", [])
        insights_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        value="AI Safety Insights",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.ListView(
                        controls=[
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Icon(
                                            name="lightbulb",
                                            color=colors["primary"],
                                            size=16,
                                        ),
                                        ft.Text(
                                            value=insight,
                                            size=14,
                                        ),
                                    ],
                                    spacing=10,
                                ),
                                padding=5,
                            )
                            for insight in insights
                        ],
                        spacing=2,
                        height=100,
                    ),
                ],
                spacing=5,
            ),
            padding=10,
            border_radius=10,
            bgcolor=ft.colors.BLUE_50,
        )
        
        # Create the time-of-day analysis
        time_analysis = self.safety_data.get("time_analysis", {})
        time_chart = self._create_time_chart(time_analysis)
        
        # Create the hotspots section
        hotspots = self.safety_data.get("hotspots", [])
        hotspots_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        value="Safety Hotspots",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.ListView(
                        controls=[
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Icon(
                                            name="warning",
                                            color=colors["warning"] if hotspot.get("risk_level") == "medium" else colors["danger"],
                                            size=16,
                                        ),
                                        ft.Text(
                                            value=hotspot.get("description", "Unknown hotspot"),
                                            size=14,
                                        ),
                                    ],
                                    spacing=10,
                                ),
                                padding=5,
                            )
                            for hotspot in hotspots
                        ],
                        spacing=2,
                        height=100,
                    ) if hotspots else ft.Text("No safety hotspots detected on this route"),
                ],
                spacing=5,
            ),
            padding=10,
            border_radius=10,
            bgcolor=ft.colors.BLUE_50,
        )
        
        # Create the recommendations section
        recommendations = self.safety_data.get("recommendations", [])
        recommendations_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        value="Safety Recommendations",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.ListView(
                        controls=[
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Icon(
                                            name="check_circle",
                                            color=colors["safety_high"],
                                            size=16,
                                        ),
                                        ft.Text(
                                            value=recommendation,
                                            size=14,
                                        ),
                                    ],
                                    spacing=10,
                                ),
                                padding=5,
                            )
                            for recommendation in recommendations
                        ],
                        spacing=2,
                        height=100,
                    ) if recommendations else ft.Text("No specific safety recommendations for this route"),
                ],
                spacing=5,
            ),
            padding=10,
            border_radius=10,
            bgcolor=ft.colors.BLUE_50,
        )
        
        # Create the main content
        content = ft.Column(
            controls=[
                header,
                overall_score,
                ft.Text(
                    value="Safety Factors Breakdown",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                ),
                factors_list,
                insights_container,
                time_chart,
                hotspots_container,
                recommendations_container,
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
        )
        
        # Initialize the container
        super().__init__(
            content=content,
            width=width,
            height=height,
            border_radius=10,
            bgcolor=ft.colors.WHITE,
            padding=15,
            border=ft.border.all(1, ft.colors.GREY_400),
        )
    
    def _handle_close(self, e):
        """Handle close button click."""
        if self.on_close:
            self.on_close(e)
    
    def _get_safety_color(self, score):
        """Get color based on safety score."""
        if score >= 85:
            return colors["safety_high"]
        elif score >= 70:
            return colors["safety_medium"]
        elif score >= 50:
            return colors["warning"]
        else:
            return colors["danger"]
    
    def _get_safety_description(self, score):
        """Get description based on safety score."""
        if score >= 85:
            return "Very Safe Route"
        elif score >= 70:
            return "Generally Safe Route"
        elif score >= 50:
            return "Use Caution on This Route"
        else:
            return "High Risk Route - Consider Alternatives"
    
    def _create_factor_items(self, factors):
        """Create list items for safety factors."""
        factor_items = []
        
        # Define factor weights and icons
        factor_info = {
            "crime_rate": {"weight": 0.30, "icon": "security", "title": "Crime Rate"},
            "lighting": {"weight": 0.15, "icon": "lightbulb", "title": "Street Lighting"},
            "foot_traffic": {"weight": 0.15, "icon": "people", "title": "Pedestrian Density"},
            "police_presence": {"weight": 0.10, "icon": "local_police", "title": "Police Presence"},
            "time_of_day": {"weight": 0.10, "icon": "access_time", "title": "Time of Day Risk"},
            "surveillance": {"weight": 0.05, "icon": "videocam", "title": "Surveillance Coverage"},
            "road_quality": {"weight": 0.05, "icon": "road", "title": "Road Quality"},
            "emergency_services": {"weight": 0.10, "icon": "emergency", "title": "Emergency Services Proximity"}
        }
        
        # Create items for each factor
        for factor, value in factors.items():
            if factor in factor_info:
                info = factor_info[factor]
                factor_items.append(
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(
                                            name=info["icon"],
                                            color=colors["primary"],
                                            size=16,
                                        ),
                                        ft.Text(
                                            value=f"{info['title']} ({int(info['weight'] * 100)}%)",
                                            size=14,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        ft.Text(
                                            value=f"{value}/100",
                                            size=14,
                                            color=self._get_safety_color(value),
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                ft.ProgressBar(
                                    value=value / 100,
                                    width=None,
                                    color=self._get_safety_color(value),
                                    bgcolor=ft.colors.GREY_300,
                                ),
                            ],
                        ),
                        padding=ft.padding.only(bottom=5),
                    )
                )
        
        return factor_items
    
    def _create_time_chart(self, time_analysis):
        """Create time-of-day safety chart."""
        # In a real implementation, this would be a proper chart
        # For now, we'll create a simple visualization
        
        time_periods = ["Morning", "Afternoon", "Evening", "Night"]
        time_scores = [
            time_analysis.get("morning", 80),
            time_analysis.get("afternoon", 85),
            time_analysis.get("evening", 70),
            time_analysis.get("night", 50),
        ]
        
        time_bars = []
        for i, period in enumerate(time_periods):
            score = time_scores[i]
            time_bars.append(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(
                                content=ft.Text(
                                    value=f"{score}",
                                    size=12,
                                    color=ft.colors.WHITE,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                bgcolor=self._get_safety_color(score),
                                border_radius=ft.border_radius.only(top_left=5, top_right=5),
                                height=30,
                                width=40,
                                alignment=ft.alignment.center,
                            ),
                            ft.Container(
                                content=ft.Text(
                                    value=period,
                                    size=12,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                width=40,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                )
            )
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        value="Safety by Time of Day",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Row(
                        controls=time_bars,
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    ),
                ],
                spacing=10,
            ),
            padding=10,
            border_radius=10,
            bgcolor=ft.colors.BLUE_50,
        )
    
    def update_data(self, safety_data):
        """
        Update the panel with new safety data.
        
        Args:
            safety_data (dict): New safety analysis data
        """
        self.safety_data = safety_data
        # Re-render the panel
        # In a real implementation, this would update all sections
        # For now, we'll just update the overall score
        safety_score = self.safety_data.get("overall_score", 0)
        # Update UI elements
        self.update()
