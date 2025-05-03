"""
Route Comparison Component for SafeWayAI application.
This module provides a tabbed interface for comparing multiple route options.
"""

import flet as ft
import logging
from app.utils.enhanced_theme import get_color_scheme

colors = get_color_scheme()
logger = logging.getLogger(__name__)

class RouteComparison(ft.Container):
    """Route comparison component with tabbed interface."""
    
    def __init__(self, 
                 routes=None, 
                 width=None, 
                 height=None,
                 on_route_select=None):
        """
        Initialize the route comparison component.
        
        Args:
            routes (list): List of route data dictionaries
            width (int, optional): Component width
            height (int, optional): Component height
            on_route_select (function, optional): Callback when a route is selected
        """
        self.routes = routes or []
        self.on_route_select = on_route_select
        self.selected_route_index = 0 if self.routes else None
        
        # Create the header
        header = ft.Row(
            controls=[
                ft.Text(
                    value="Route Options",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        
        # Create tabs for each route
        tabs = []
        tab_content = []
        
        for i, route in enumerate(self.routes):
            # Create tab
            route_type = route.get("type", "Unknown")
            safety_score = route.get("safety_score", 0)
            duration = route.get("duration_min", 0)
            distance = route.get("distance_km", 0)
            
            # Determine icon and color based on route type
            icon_name = "shield"
            if route_type.lower() == "safest":
                icon_name = "shield"
                tab_color = self._get_safety_color(safety_score)
            elif route_type.lower() == "fastest":
                icon_name = "speed"
                tab_color = colors["primary"]
            elif route_type.lower() == "balanced":
                icon_name = "balance"
                tab_color = colors["primary"]
            else:
                icon_name = "route"
                tab_color = colors["primary"]
            
            tabs.append(
                ft.Tab(
                    text=route_type.capitalize(),
                    icon=icon_name,
                    content=self._create_route_content(route, i),
                )
            )
        
        # Create tabs view
        if tabs:
            tabs_view = ft.Tabs(
                tabs=tabs,
                selected_index=0,
                on_change=self._handle_tab_change,
            )
        else:
            tabs_view = ft.Text("No route options available")
        
        # Create the main content
        content = ft.Column(
            controls=[
                header,
                tabs_view,
            ],
            spacing=10,
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
    
    def _handle_tab_change(self, e):
        """Handle tab change event."""
        self.selected_route_index = e.control.selected_index
        if self.on_route_select and self.selected_route_index is not None:
            self.on_route_select(self.selected_route_index)
    
    def _create_route_content(self, route, index):
        """Create content for a route tab."""
        # Extract route data
        route_type = route.get("type", "Unknown")
        safety_score = route.get("safety_score", 0)
        duration = route.get("duration_min", 0)
        distance = route.get("distance_km", 0)
        
        # Create route summary
        summary = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(
                                name="shield",
                                color=self._get_safety_color(safety_score),
                                size=20,
                            ),
                            ft.Text(
                                value=f"Safety Score: {safety_score}/100",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=self._get_safety_color(safety_score),
                            ),
                        ],
                        spacing=5,
                    ),
                    ft.Row(
                        controls=[
                            ft.Icon(
                                name="schedule",
                                color=colors["primary"],
                                size=20,
                            ),
                            ft.Text(
                                value=f"Duration: {duration} min",
                                size=16,
                            ),
                        ],
                        spacing=5,
                    ),
                    ft.Row(
                        controls=[
                            ft.Icon(
                                name="straighten",
                                color=colors["primary"],
                                size=20,
                            ),
                            ft.Text(
                                value=f"Distance: {distance:.1f} km",
                                size=16,
                            ),
                        ],
                        spacing=5,
                    ),
                ],
                spacing=10,
            ),
            padding=10,
            border_radius=10,
            bgcolor=ft.colors.BLUE_50,
        )
        
        # Create route explanation
        explanation = self._create_route_explanation(route)
        
        # Create route comparison
        comparison = self._create_route_comparison(route, index)
        
        # Create select button
        select_button = ft.ElevatedButton(
            text=f"Select {route_type.capitalize()} Route",
            icon="check_circle",
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                color=ft.colors.WHITE,
                bgcolor=self._get_safety_color(safety_score),
            ),
            on_click=lambda e, idx=index: self._handle_route_select(e, idx),
        )
        
        # Return the complete content
        return ft.Column(
            controls=[
                summary,
                explanation,
                comparison,
                select_button,
            ],
            spacing=15,
            scroll=ft.ScrollMode.AUTO,
        )
    
    def _create_route_explanation(self, route):
        """Create explanation for why this route was chosen."""
        route_type = route.get("type", "Unknown").lower()
        safety_score = route.get("safety_score", 0)
        
        if route_type == "safest":
            explanation_text = (
                "This route prioritizes your safety above all else. "
                "It may take longer but offers the highest safety score based on "
                "multiple factors including crime rates, lighting, and police presence."
            )
        elif route_type == "fastest":
            explanation_text = (
                "This route prioritizes speed and efficiency. "
                "It's the quickest way to your destination, but may have a lower "
                "safety score compared to other options."
            )
        elif route_type == "balanced":
            explanation_text = (
                "This route offers a balance between safety and speed. "
                "It provides a reasonable travel time while maintaining an acceptable "
                "safety score."
            )
        else:
            explanation_text = "Route explanation not available."
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        value="Why This Route?",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        value=explanation_text,
                        size=14,
                    ),
                ],
                spacing=5,
            ),
            padding=10,
            border_radius=10,
            bgcolor=ft.colors.BLUE_50,
        )
    
    def _create_route_comparison(self, route, index):
        """Create comparison with other routes."""
        # Only create comparison if we have multiple routes
        if len(self.routes) <= 1:
            return ft.Container()
        
        current_route = route
        current_type = current_route.get("type", "").lower()
        current_safety = current_route.get("safety_score", 0)
        current_duration = current_route.get("duration_min", 0)
        
        comparison_items = []
        
        for i, other_route in enumerate(self.routes):
            if i == index:
                continue  # Skip comparing to self
                
            other_type = other_route.get("type", "").lower()
            other_safety = other_route.get("safety_score", 0)
            other_duration = other_route.get("duration_min", 0)
            
            # Calculate differences
            safety_diff = current_safety - other_safety
            duration_diff = other_duration - current_duration  # Positive means current is faster
            
            # Create comparison text
            if current_type == "safest" and other_type == "fastest":
                if duration_diff > 0:
                    comparison_text = (
                        f"{duration_diff} minutes slower than the fastest route, "
                        f"but {abs(safety_diff)} points safer."
                    )
                else:
                    comparison_text = (
                        f"Both safer and faster than the alternative route by "
                        f"{abs(safety_diff)} safety points and {abs(duration_diff)} minutes."
                    )
            elif current_type == "fastest" and other_type == "safest":
                if safety_diff < 0:
                    comparison_text = (
                        f"{abs(duration_diff)} minutes faster than the safest route, "
                        f"but {abs(safety_diff)} points less safe."
                    )
                else:
                    comparison_text = (
                        f"Both faster and safer than the alternative route by "
                        f"{abs(duration_diff)} minutes and {abs(safety_diff)} safety points."
                    )
            else:
                if safety_diff > 0 and duration_diff > 0:
                    comparison_text = (
                        f"{abs(safety_diff)} points safer and {abs(duration_diff)} minutes faster "
                        f"than the {other_type} route."
                    )
                elif safety_diff > 0:
                    comparison_text = (
                        f"{abs(safety_diff)} points safer but {abs(duration_diff)} minutes slower "
                        f"than the {other_type} route."
                    )
                elif duration_diff > 0:
                    comparison_text = (
                        f"{abs(duration_diff)} minutes faster but {abs(safety_diff)} points less safe "
                        f"than the {other_type} route."
                    )
                else:
                    comparison_text = (
                        f"{abs(safety_diff)} points less safe and {abs(duration_diff)} minutes slower "
                        f"than the {other_type} route."
                    )
            
            comparison_items.append(
                ft.Container(
                    content=ft.Text(
                        value=f"Compared to {other_type.capitalize()} route: {comparison_text}",
                        size=14,
                    ),
                    padding=5,
                )
            )
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        value="Route Comparison",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                    ),
                    *comparison_items,
                ],
                spacing=5,
            ),
            padding=10,
            border_radius=10,
            bgcolor=ft.colors.BLUE_50,
        )
    
    def _handle_route_select(self, e, index):
        """Handle route selection."""
        self.selected_route_index = index
        if self.on_route_select:
            self.on_route_select(index)
    
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
    
    def update_routes(self, routes):
        """
        Update the component with new route data.
        
        Args:
            routes (list): New list of route data dictionaries
        """
        self.routes = routes
        self.selected_route_index = 0 if self.routes else None
        # Re-render the component
        # In a real implementation, this would rebuild the tabs
        self.update()
