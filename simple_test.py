import flet as ft

# Use Colors instead of colors (to avoid deprecation warnings)
Colors = ft.Colors

def main(page: ft.Page):
    page.title = "Simple Navigation Test"
    page.padding = 20

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

    # Create a visual representation of the route
    route_container = ft.Container(
        bgcolor=Colors.BLUE,
        width=None,
        height=8,
        border_radius=4,
        margin=ft.margin.only(top=100, bottom=100),
        expand=True,
    )

    # Create markers for start, end, and current position
    start_marker = ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(
                    name="play_circle",
                    color=Colors.GREEN,
                    size=24,
                ),
                ft.Text(
                    value="Start",
                    color=Colors.BLACK,
                    size=10,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=2,
        ),
        padding=5,
        border_radius=15,
        bgcolor=Colors.WHITE,
    )

    end_marker = ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(
                    name="location_on",
                    color=Colors.RED,
                    size=24,
                ),
                ft.Text(
                    value="End",
                    color=Colors.BLACK,
                    size=10,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=2,
        ),
        padding=5,
        border_radius=15,
        bgcolor=Colors.WHITE,
    )

    current_marker = ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(
                    name="navigation",
                    color=Colors.BLUE,
                    size=24,
                ),
                ft.Text(
                    value="You",
                    color=Colors.BLACK,
                    size=10,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=2,
        ),
        padding=5,
        border_radius=15,
        bgcolor=Colors.WHITE,
    )

    # Create a stack for the map visualization
    map_stack = ft.Stack(
        controls=[
            # Base map background
            ft.Container(
                bgcolor=Colors.BLUE_50,
                border_radius=10,
                width=None,
                height=None,
                expand=True,
            ),
            # Route line
            route_container,
            # Start marker (positioned at the left)
            ft.Container(
                content=start_marker,
                left=20,
                top=100,
            ),
            # End marker (positioned at the right)
            ft.Container(
                content=end_marker,
                right=20,
                top=100,
            ),
            # Current position marker (will be updated)
            ft.Container(
                content=current_marker,
                left=20,  # Will be updated
                top=100,
            ),
        ],
        width=None,
        height=300,
    )

    # Progress bar
    progress_bar = ft.ProgressBar(width=None, value=0)

    # Navigation info
    eta_text = ft.Text("Estimated time: 25 min")
    distance_text = ft.Text("Distance remaining: 3.5 km")
    safety_text = ft.Text("Current area safety: 85/100")

    # Function to move along the route
    def move_forward(e):
        nonlocal current_position

        # Move to next position
        if current_position < len(route_points) - 1:
            current_position += 1

            # Update progress
            progress_bar.value = current_position / (len(route_points) - 1)

            # Update ETA and distance
            remaining = 1 - progress_bar.value
            eta_text.value = f"Estimated time: {int(25 * remaining)} min"
            distance_text.value = f"Distance remaining: {3.5 * remaining:.1f} km"

            # Update current marker position
            # Calculate position based on progress (linear interpolation)
            left_position = 20 + (progress_bar.value * (page.width - 40))
            map_stack.controls[-1].left = left_position

            # Update the page
            page.update()

    # Create buttons
    move_button = ft.ElevatedButton("Move Forward", on_click=move_forward)

    # Add everything to the page
    page.add(
        ft.Text("Navigation Test", size=24, weight=ft.FontWeight.BOLD),
        map_stack,
        ft.Container(height=20),
        ft.Text("Journey Progress", weight=ft.FontWeight.BOLD),
        progress_bar,
        ft.Container(height=10),
        ft.Column([eta_text, distance_text, safety_text]),
        ft.Container(height=20),
        move_button
    )

ft.app(target=main)
import logging

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler and a stream handler
file_handler = logging.FileHandler('navigation_test.log')
stream_handler = logging.StreamHandler()

# Create a formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# ...

# Function to move along the route
def move_forward(e):
    nonlocal current_position

    # Move to next position
    if current_position < len(route_points) - 1:
        current_position += 1

        # Update progress
        progress_bar.value = current_position / (len(route_points) - 1)

        # Update ETA and distance
        remaining = 1 - progress_bar.value
        eta_text.value = f"Estimated time: {int(25 * remaining)} min"
        distance_text.value = f"Distance remaining: {3.5 * remaining:.1f} km"

        # Update current marker position
        # Calculate position based on progress (linear interpolation)
        left_position = 20 + (progress_bar.value * (page.width - 40))
        map_stack.controls[-1].left = left_position

        # Log the move
        logger.info(f"Moved to position {current_position + 1} of {len(route_points)}")

        # Update the page
        page.update()

# ...

# Add a log message when the app starts
logger.info("Navigation test app started")