import flet as ft
from app.utils.enhanced_theme import get_color_scheme

colors = get_color_scheme()

def feature_card(title, description, icon, color, button_text, on_click=None):
    """
    Creates a consistent feature card with icon, title, description, and action button.

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
                            ft.Icon(name=icon, color=color, size=28),
                            ft.Text(
                                value=title,
                                weight=ft.FontWeight.BOLD,
                                size=18,
                            ),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    ft.Divider(height=1, color=ft.colors.GREY_300),
                    ft.Text(
                        value=description,
                        size=16,
                    ),
                    ft.Container(height=10),
                    ft.ElevatedButton(
                        text=button_text,
                        icon=icon,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=ft.padding.all(15),
                        ),
                        on_click=on_click,
                        expand=True,
                    ),
                ],
                spacing=10,
            ),
            padding=20,
            border_radius=10,
        ),
        elevation=3,
        margin=ft.margin.only(bottom=15),
    )

def status_card(status="All systems operational", last_check="Just now", icon="shield", color=colors["safety_high"], on_click=None):
    """
    Creates a status card showing the current safety status.

    Args:
        status (str): The current status message.
        last_check (str): When the status was last checked.
        icon (str): Icon name to display.
        color (str): Color for the icon.
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
                                name=icon,
                                color=color,
                                size=28,
                            ),
                            ft.Text(
                                value="Safety Status",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
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
            border_radius=10,
            on_click=on_click,
        ),
        elevation=2,
        margin=ft.margin.only(bottom=15),
    )

def action_button(icon, label, color=None, on_click=None):
    """
    Creates a large, touch-friendly action button with icon and label.

    Args:
        icon (str): Icon name to display.
        label (str): Text label for the button.
        color (str, optional): Color for the icon.
        on_click (callable, optional): Function to call when button is clicked.

    Returns:
        ft.Container: A container with the button and label.
    """
    if color is None:
        color = colors["primary"]

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Icon(
                        name=icon,
                        color=ft.colors.WHITE,
                        size=28,
                    ),
                    width=56,
                    height=56,
                    border_radius=28,
                    bgcolor=color,
                    alignment=ft.alignment.center,
                ),
                ft.Text(
                    value=label,
                    size=14,
                    text_align=ft.TextAlign.CENTER,
                    weight=ft.FontWeight.BOLD,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
        ),
        on_click=on_click,
        padding=10,
    )

def social_impact_banner(message="AI for social good", icon="favorite", color=colors["primary"]):
    """
    Creates a banner highlighting the social impact of SafeWayAI.

    Args:
        message (str): The message to display.
        icon (str): Icon name to display.
        color (str): Color for the banner.

    Returns:
        ft.Container: A styled banner.
    """
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(
                    name=icon,
                    color=ft.colors.WHITE,
                    size=20,
                ),
                ft.Text(
                    value=message,
                    color=ft.colors.WHITE,
                    weight=ft.FontWeight.BOLD,
                    size=14,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
        ),
        bgcolor=color,
        padding=ft.padding.symmetric(horizontal=16, vertical=8),
        border_radius=20,
        margin=ft.margin.only(bottom=15),
    )
