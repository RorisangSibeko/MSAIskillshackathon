import flet as ft
from app.utils.enhanced_theme import get_color_scheme

colors = get_color_scheme()

class Header:
    """
    A consistent header component for all screens in the SafeWayAI app.
    Includes logo, title, and optional actions.
    """
    
    def __init__(self, title="SafeWayAI", show_logo=True, show_back_button=False, on_back=None, actions=None):
        """
        Initialize the header component.
        
        Args:
            title (str): The title to display in the header.
            show_logo (bool): Whether to show the logo.
            show_back_button (bool): Whether to show a back button.
            on_back (callable): Function to call when back button is clicked.
            actions (list): List of action buttons to display on the right.
        """
        self.title = title
        self.show_logo = show_logo
        self.show_back_button = show_back_button
        self.on_back = on_back
        self.actions = actions or []
        
    def build(self):
        """Build the header component."""
        # Create leading widget (back button or logo)
        leading = None
        if self.show_back_button and self.on_back:
            leading = ft.IconButton(
                icon=ft.icons.ARROW_BACK,
                on_click=self.on_back,
                icon_color=ft.colors.WHITE,
            )
        
        # Create title with optional logo
        title_row = []
        
        if self.show_logo:
            title_row.append(
                ft.Image(
                    src="/assets/logo.svg",
                    width=32,
                    height=32,
                    fit=ft.ImageFit.CONTAIN,
                )
            )
            
        title_row.append(
            ft.Text(
                value=self.title,
                color=ft.colors.WHITE,
                weight=ft.FontWeight.BOLD,
                size=20,
            )
        )
        
        title = ft.Row(
            controls=title_row,
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        # Create app bar
        return ft.AppBar(
            leading=leading,
            title=title,
            center_title=True,
            bgcolor=colors["primary"],
            actions=self.actions,
            toolbar_height=60,
        )
