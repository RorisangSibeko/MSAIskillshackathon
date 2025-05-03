import flet as ft
from app.components.safety_map import SafetyMap

def main(page: ft.Page):
    page.title = "Navigation Test"
    page.padding = 20
    
    # Create a safety map
    safety_map = SafetyMap(
        width=None,
        height=300,
        on_map_click=lambda lat, lon: print(f"Map clicked at: {lat}, {lon}"),
        on_map_ready=lambda: print("Map is ready")
    )
    
    # Define a route
    route_points = [
        {"latitude": -26.2041, "longitude": 28.0473},  # Start
        {"latitude": -26.2046, "longitude": 28.0478},  # Waypoint 1
        {"latitude": -26.2051, "longitude": 28.0483},  # Waypoint 2
        {"latitude": -26.2056, "longitude": 28.0488},  # Waypoint 3
        {"latitude": -26.2061, "longitude": 28.0493},  # Waypoint 4
        {"latitude": -26.2066, "longitude": 28.0498},  # Waypoint 5
        {"latitude": -26.2071, "longitude": 28.0503},  # Waypoint 6
        {"latitude": -26.2076, "longitude": 28.0508},  # Waypoint 7
        {"latitude": -26.2081, "longitude": 28.0513}   # End
    ]
    
    # Current position
    current_position = 0
    current_marker_id = None
    
    # Add the route to the map
    safety_map.add_route(route_points, safety_score=85)
    
    # Add start and end markers
    safety_map.add_marker(
        route_points[0]["latitude"],
        route_points[0]["longitude"],
        title="Start",
        icon="play_circle"
    )
    
    safety_map.add_marker(
        route_points[-1]["latitude"],
        route_points[-1]["longitude"],
        title="Destination",
        icon="location_on"
    )
    
    # Add current position marker
    current_marker_id = safety_map.add_marker(
        route_points[0]["latitude"],
        route_points[0]["longitude"],
        title="Current Position",
        icon="navigation"
    )
    
    # Add safety overlay
    safety_map.add_safety_overlay("heatmap")
    
    # Progress bar
    progress_bar = ft.ProgressBar(width=None, value=0)
    
    # Navigation info
    eta_text = ft.Text("Estimated time: 25 min")
    distance_text = ft.Text("Distance remaining: 3.5 km")
    safety_text = ft.Text("Current area safety: 85/100")
    
    # Function to move along the route
    def move_forward(e):
        nonlocal current_position, current_marker_id
        
        # Move to next position
        if current_position < len(route_points) - 1:
            current_position += 1
            
            # Update progress
            progress_bar.value = current_position / (len(route_points) - 1)
            
            # Update ETA and distance
            remaining = 1 - progress_bar.value
            eta_text.value = f"Estimated time: {int(25 * remaining)} min"
            distance_text.value = f"Distance remaining: {3.5 * remaining:.1f} km"
            
            # Remove old marker and add new one
            safety_map.remove_marker(current_marker_id)
            current_marker_id = safety_map.add_marker(
                route_points[current_position]["latitude"],
                route_points[current_position]["longitude"],
                title="Current Position",
                icon="navigation"
            )
            
            # Update the page
            page.update()
    
    # Create buttons
    move_button = ft.ElevatedButton("Move Forward", on_click=move_forward)
    
    # Add everything to the page
    page.add(
        ft.Text("Navigation Test", size=24, weight=ft.FontWeight.BOLD),
        safety_map,
        ft.Container(height=20),
        ft.Text("Journey Progress", weight=ft.FontWeight.BOLD),
        progress_bar,
        ft.Container(height=10),
        ft.Column([eta_text, distance_text, safety_text]),
        ft.Container(height=20),
        move_button
    )

ft.app(target=main)
