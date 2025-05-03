import flet as ft
from app.utils.enhanced_theme import get_color_scheme, get_text_styles, apply_text_style

colors = get_color_scheme()
text_styles = get_text_styles()

def create_responsive_row(controls, alignment="center", spacing=10, wrap=True, mobile_column=True):
    """
    Creates a row that converts to a column on smaller screens.

    Args:
        controls (list): List of controls to include in the row.
        alignment (str): Horizontal alignment of controls.
        spacing (int): Spacing between controls.
        wrap (bool): Whether the row should wrap.
        mobile_column (bool): Whether to convert to column on mobile.

    Returns:
        ft.ResponsiveRow: A responsive row control.
    """
    return ft.ResponsiveRow(
        controls=controls,
        alignment=alignment,
        spacing=spacing,
        wrap=wrap,
        run_spacing=spacing,
        vertical_alignment="center",
    )

def create_card(title, content, icon=None, color=None, on_click=None):
    """
    Creates a styled card with title, content, and optional icon.

    Args:
        title (str): The card title.
        content (str): The card content.
        icon (str, optional): Icon name to display.
        color (str, optional): Color for the icon and accent.
        on_click (callable, optional): Function to call when card is clicked.

    Returns:
        ft.Card: A styled card control.
    """
    if color is None:
        color = colors["primary"]

    title_row = [ft.Text(value=title, weight=ft.FontWeight.BOLD)]

    if icon:
        title_row.insert(0, ft.Icon(name=icon, color=color, size=24))

    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(controls=title_row),
                    ft.Divider(height=1, color=ft.colors.GREY_300),
                    ft.Text(value=content),
                ],
                spacing=10,
            ),
            padding=15,
        ),
        elevation=2,
        margin=ft.margin.only(bottom=10),
        on_click=on_click,
    )

def create_action_button(icon, label, color=None, on_click=None, size=64):
    """
    Creates a large, touch-friendly action button with icon and label.

    Args:
        icon (str): Icon name to display.
        label (str): Text label for the button.
        color (str, optional): Color for the icon.
        on_click (callable, optional): Function to call when button is clicked.
        size (int, optional): Size of the button.

    Returns:
        ft.Column: A column containing the button and label.
    """
    if color is None:
        color = colors["primary"]

    return ft.Column(
        controls=[
            ft.IconButton(
                icon=icon,
                icon_color=color,
                icon_size=32,
                tooltip=label,
                on_click=on_click,
            ),
            ft.Text(
                value=label,
                size=12,
                text_align=ft.TextAlign.CENTER,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=5,
    )

def create_quick_actions_row(actions):
    """
    Creates a row of quick action buttons.

    Args:
        actions (list): List of dictionaries with 'icon', 'label', 'color', and 'on_click' keys.

    Returns:
        ft.Row: A row of action buttons.
    """
    action_buttons = [
        create_action_button(
            action["icon"],
            action["label"],
            action.get("color", colors["primary"]),
            action.get("on_click"),
        )
        for action in actions
    ]

    return ft.Row(
        controls=action_buttons,
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        spacing=0,
    )

def create_safe_route_card(on_click=None):
    """
    Creates a prominent card for the safe route finder feature.

    Args:
        on_click (callable, optional): Function to call when card is clicked.

    Returns:
        ft.Card: A styled card for the safe route finder.
    """
    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(
                                name="route",
                                color=colors["route_finder"],
                                size=32,
                            ),
                            ft.Text(
                                value="Find Safest Route",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Divider(height=1, color=ft.colors.GREY_300),
                    ft.Text(
                        value="Let AI determine the safest route to your destination",
                        size=16,
                    ),
                    ft.Container(height=10),
                    ft.ElevatedButton(
                        text="Find Safe Route",
                        icon="directions",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=ft.padding.all(15),
                        ),
                        expand=True,
                    ),
                ],
                spacing=10,
            ),
            padding=20,
        ),
        elevation=3,
        margin=ft.margin.only(bottom=15),
        on_click=on_click,
    )

def create_status_card(status="All systems operational", last_check="Just now", on_click=None):
    """
    Creates a status card showing the current safety status.

    Args:
        status (str): The current status message.
        last_check (str): When the status was last checked.
        on_click (callable, optional): Function to call when card is clicked.

    Returns:
        ft.Card: A styled status card.
    """
    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(
                                name="shield",
                                color=colors["safety_high"],
                                size=24,
                            ),
                            ft.Text(
                                value="Safety Status",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                    ),
                    ft.Divider(height=1, color=ft.colors.GREY_300),
                    ft.Text(value=status, size=16),
                    ft.Text(
                        value=f"Last check: {last_check}",
                        size=14,
                        color=colors["text_secondary"],
                    ),
                ],
                spacing=10,
            ),
            padding=20,
        ),
        elevation=2,
        margin=ft.margin.only(bottom=15),
        on_click=on_click,
    )

def create_feature_card(title, description, icon, color, button_text, on_click=None):
    """
    Creates a feature card with icon, description, and action button.

    Args:
        title (str): The feature title.
        description (str): Description of the feature.
        icon (str): Icon name to display.
        color (str): Color for the icon.
        button_text (str): Text for the action button.
        on_click (callable, optional): Function to call when button is clicked.

    Returns:
        ft.Card: A styled feature card.
    """
    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(name=icon, color=color, size=24),
                            ft.Text(
                                value=title,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                    ),
                    ft.Text(value=description),
                    ft.ElevatedButton(
                        text=button_text,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                        ),
                        on_click=on_click,
                    ),
                ],
                spacing=10,
            ),
            padding=15,
        ),
    )

def create_mobile_app_bar(title, leading=None, actions=None, color=None):
    """
    Creates a mobile-optimized app bar.

    Args:
        title (str): The app bar title.
        leading (ft.Control, optional): Control to display at the start of the app bar.
        actions (list, optional): List of controls to display at the end of the app bar.
        color (str, optional): Background color for the app bar.

    Returns:
        ft.AppBar: A styled app bar.
    """
    if color is None:
        color = colors["primary"]

    return ft.AppBar(
        leading=leading,
        title=ft.Text(value=title),
        center_title=True,
        bgcolor=color,
        actions=actions or [],
    )

def create_bottom_navigation_bar(selected_index=0, on_change=None):
    """
    Creates a mobile-optimized bottom navigation bar.

    Args:
        selected_index (int): The index of the initially selected item.
        on_change (callable, optional): Function to call when selection changes.

    Returns:
        ft.NavigationBar: A styled navigation bar.
    """
    return ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon="home", label="Home"),
            ft.NavigationDestination(icon="route", label="Routes"),
            ft.NavigationDestination(icon="report_problem", label="Report"),
            ft.NavigationDestination(icon="notifications", label="Alerts"),
            ft.NavigationDestination(icon="settings", label="Settings"),
        ],
        selected_index=selected_index,
        on_change=on_change,
        height=65,
    )

def create_floating_action_button(icon, on_click=None, text=None):
    """
    Creates a floating action button.

    Args:
        icon (str): Icon name to display.
        on_click (callable, optional): Function to call when button is clicked.
        text (str, optional): Text to display on extended FAB.

    Returns:
        ft.FloatingActionButton: A styled floating action button.
    """
    return ft.FloatingActionButton(
        icon=icon,
        text=text,
        on_click=on_click,
        bgcolor=colors["primary"],
    )
