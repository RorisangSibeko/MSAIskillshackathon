import flet as ft

def get_enhanced_theme():
    """
    Creates an enhanced theme for SafeWayAI with a focus on mobile-first design.

    Returns:
        ft.Theme: A Flet theme object with customized colors and settings.
    """
    # Primary color palette - Blue represents safety and trust
    primary_blue = ft.colors.BLUE
    primary_swatch = {
        50: ft.colors.BLUE_50,
        100: ft.colors.BLUE_100,
        200: ft.colors.BLUE_200,
        300: ft.colors.BLUE_300,
        400: ft.colors.BLUE_400,
        500: ft.colors.BLUE_500,  # Primary color
        600: ft.colors.BLUE_600,
        700: ft.colors.BLUE_700,
        800: ft.colors.BLUE_800,
        900: ft.colors.BLUE_900,
    }

    # Secondary color palette - Teal for a modern feel
    secondary_teal = ft.colors.TEAL
    secondary_swatch = {
        50: ft.colors.TEAL_50,
        100: ft.colors.TEAL_100,
        200: ft.colors.TEAL_200,
        300: ft.colors.TEAL_300,
        400: ft.colors.TEAL_400,
        500: ft.colors.TEAL_500,  # Secondary color
        600: ft.colors.TEAL_600,
        700: ft.colors.TEAL_700,
        800: ft.colors.TEAL_800,
        900: ft.colors.TEAL_900,
    }

    # Alert colors
    warning_color = ft.colors.ORANGE
    danger_color = ft.colors.RED_600
    success_color = ft.colors.GREEN_600
    info_color = ft.colors.LIGHT_BLUE_600

    # Create the theme
    return ft.Theme(
        color_scheme_seed=primary_blue,
        use_material3=True,

        # Custom colors
        primary_swatch=primary_swatch,

        # Custom component themes
        app_bar_theme=ft.AppBarTheme(
            color=primary_swatch[700],
            center_title=True,
            elevation=0,
            title_spacing=0,
        ),

        card_theme=ft.CardTheme(
            elevation=2,
            shape=ft.RoundedRectangleBorder(radius=10),
            color=ft.colors.WHITE,
        ),

        # Button themes removed as they're not supported in this version of Flet

        floating_action_button_theme=ft.FloatingActionButtonTheme(
            foreground_color=ft.colors.WHITE,
            shape=ft.CircleBorder(),
            elevation=4,
        ),

        navigation_bar_theme=ft.NavigationBarTheme(
            background_color=ft.colors.WHITE,
            height=65,  # Taller for better touch targets
            elevation=8,
            indicator_color=primary_swatch[100],
            label_behavior=ft.NavigationDestinationLabelBehavior.ALWAYS_SHOW,
        ),

        # Page transitions for a more polished feel
        page_transitions={
            ft.PageTransitionType.FADE: ft.PageTransitionTheme(duration=200),
            ft.PageTransitionType.CUPERTINO: ft.PageTransitionTheme(duration=300),
        },
    )

def get_color_scheme():
    """
    Returns a dictionary of colors used throughout the app.

    Returns:
        dict: A dictionary of color values.
    """
    return {
        # Base colors
        "primary": ft.colors.BLUE,
        "secondary": ft.colors.TEAL,
        "background": ft.colors.WHITE,
        "surface": ft.colors.WHITE,

        # Text colors
        "text_primary": ft.colors.GREY_900,
        "text_secondary": ft.colors.GREY_700,
        "text_hint": ft.colors.GREY_500,
        "text_disabled": ft.colors.GREY_400,
        "text_on_primary": ft.colors.WHITE,
        "text_on_secondary": ft.colors.WHITE,

        # Status colors
        "success": ft.colors.GREEN_600,
        "warning": ft.colors.ORANGE,
        "danger": ft.colors.RED_600,
        "info": ft.colors.LIGHT_BLUE_600,

        # Safety level colors
        "safety_high": ft.colors.GREEN_600,
        "safety_medium": ft.colors.AMBER_600,
        "safety_low": ft.colors.RED_600,

        # Feature-specific colors
        "route_finder": ft.colors.BLUE_600,
        "monitoring": ft.colors.PURPLE_600,
        "alerts": ft.colors.RED_600,
        "gbv_resources": ft.colors.PINK_600,
        "iot_devices": ft.colors.CYAN_600,
    }

def get_text_styles():
    """
    Returns a dictionary of text styles used throughout the app.

    Returns:
        dict: A dictionary of TextStyle objects.
    """
    colors = get_color_scheme()

    return {
        # Headings
        "heading_1": ft.TextStyle(
            size=32,
            weight=ft.FontWeight.BOLD,
            color=colors["text_primary"],
        ),
        "heading_2": ft.TextStyle(
            size=24,
            weight=ft.FontWeight.BOLD,
            color=colors["text_primary"],
        ),
        "heading_3": ft.TextStyle(
            size=20,
            weight=ft.FontWeight.BOLD,
            color=colors["text_primary"],
        ),

        # Body text
        "body_large": ft.TextStyle(
            size=18,
            weight=ft.FontWeight.NORMAL,
            color=colors["text_primary"],
        ),
        "body_medium": ft.TextStyle(
            size=16,
            weight=ft.FontWeight.NORMAL,
            color=colors["text_primary"],
        ),
        "body_small": ft.TextStyle(
            size=14,
            weight=ft.FontWeight.NORMAL,
            color=colors["text_secondary"],
        ),

        # Special text
        "caption": ft.TextStyle(
            size=12,
            weight=ft.FontWeight.NORMAL,
            color=colors["text_secondary"],
        ),
        "button": ft.TextStyle(
            size=16,
            weight=ft.FontWeight.MEDIUM,
            color=colors["text_on_primary"],
        ),
        "label": ft.TextStyle(
            size=14,
            weight=ft.FontWeight.MEDIUM,
            color=colors["text_secondary"],
        ),
    }

def apply_text_style(text, style_name):
    """
    Applies a predefined text style to a Text control.

    Args:
        text (ft.Text): The text control to style.
        style_name (str): The name of the style to apply.

    Returns:
        ft.Text: The styled text control.
    """
    styles = get_text_styles()
    style = styles.get(style_name)

    if style:
        text.size = style.size
        text.weight = style.weight
        text.color = style.color

    return text
