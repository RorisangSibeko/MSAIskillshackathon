import flet as ft

def get_theme():
    """Get the application theme."""
    return ft.Theme(
        color_scheme_seed=ft.colors.BLUE,
        use_material3=True
    )
