"""
Improved navigation components for SafeWayAI application.
This module provides enhanced navigation elements for better organization and accessibility.
"""

import flet as ft
from app.utils.enhanced_theme import get_color_scheme

# Get color scheme
colors = get_color_scheme()

def create_bottom_navigation(page, on_change_callback):
    """
    Create a bottom navigation bar for quick access to key features.
    
    Args:
        page: The Flet page
        on_change_callback: Callback function when navigation changes
        
    Returns:
        ft.Control: The bottom navigation bar
    """
    return ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(
                icon=ft.icons.HOME_ROUNDED,
                selected_icon=ft.icons.HOME,
                label="Home",
            ),
            ft.NavigationDestination(
                icon=ft.icons.MAP_OUTLINED,
                selected_icon=ft.icons.MAP,
                label="Navigation",
            ),
            ft.NavigationDestination(
                icon=ft.icons.CHAT_BUBBLE_OUTLINE_ROUNDED,
                selected_icon=ft.icons.CHAT_ROUNDED,
                label="Safety Chat",
            ),
            ft.NavigationDestination(
                icon=ft.icons.NOTIFICATIONS_OUTLINED,
                selected_icon=ft.icons.NOTIFICATIONS_ACTIVE_ROUNDED,
                label="Alerts",
            ),
            ft.NavigationDestination(
                icon=ft.icons.MENU,
                selected_icon=ft.icons.MENU,
                label="More",
            ),
        ],
        on_change=on_change_callback,
        selected_index=0,
        height=65,
        elevation=10,
        surface_tint_color=ft.colors.SURFACE_VARIANT,
    )

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
                                name=ft.icons.EMERGENCY,
                                color=ft.colors.WHITE,
                            ),
                            ft.Text(
                                "SOS",
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
                    tooltip="Emergency SOS",
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

def create_improved_chat_interface(
    page, 
    on_send, 
    chat_history=None, 
    colors=None, 
    enable_location=True, 
    enable_media=False, 
    placeholder_text="Type a message..."
):
    """
    Create an improved chat interface with better organization and accessibility.
    
    Args:
        page: The Flet page
        on_send: Callback function when a message is sent
        chat_history: Initial chat history
        colors: Color scheme to use
        enable_location: Whether to enable location sharing
        enable_media: Whether to enable media attachments
        placeholder_text: Placeholder text for the input field
        
    Returns:
        ft.Control: The improved chat interface
    """
    # Initialize state
    chat_history = chat_history or []
    colors = colors or {
        "primary": ft.colors.BLUE,
        "user_bubble": ft.colors.BLUE_100,
        "ai_bubble": ft.colors.GREY_100,
        "system_bubble": ft.colors.AMBER_100,
        "alert": ft.colors.RED_400,
    }
    
    # Create UI components
    chat_list = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
        padding=10,
    )
    
    message_input = ft.TextField(
        hint_text=placeholder_text,
        border_radius=30,
        filled=True,
        expand=True,
        autofocus=True,
        prefix_icon=ft.icons.CHAT,
        suffix_icon=ft.icons.SEND,
        on_submit=lambda _: send_message(),
    )
    
    # State variables
    is_emergency = False
    location_attached = False
    current_location = None
    
    # Create emergency indicator
    emergency_indicator = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(
                    name=ft.icons.WARNING_ROUNDED,
                    color=ft.colors.WHITE,
                    size=16,
                ),
                ft.Text(
                    "EMERGENCY MODE",
                    color=ft.colors.WHITE,
                    weight=ft.FontWeight.BOLD,
                    size=12,
                ),
            ],
            spacing=5,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=colors["alert"],
        padding=ft.padding.symmetric(horizontal=10, vertical=5),
        border_radius=15,
        visible=False,
    )
    
    # Create location indicator
    location_indicator = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(
                    name=ft.icons.LOCATION_ON,
                    color=ft.colors.WHITE,
                    size=16,
                ),
                ft.Text(
                    "Location attached",
                    color=ft.colors.WHITE,
                    weight=ft.FontWeight.BOLD,
                    size=12,
                ),
            ],
            spacing=5,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=colors["primary"],
        padding=ft.padding.symmetric(horizontal=10, vertical=5),
        border_radius=15,
        visible=False,
    )
    
    def add_message_bubble(message):
        """Add a message bubble to the chat list."""
        sender = message.get("sender", "user")
        content = message.get("content", "")
        timestamp = message.get("timestamp", "")
        is_alert = message.get("is_alert", False)

        # Convert timestamp to readable format
        try:
            from datetime import datetime
            dt = datetime.fromisoformat(timestamp)
            time_str = dt.strftime("%I:%M %p")
        except:
            time_str = "Now"

        # Determine alignment and colors based on sender
        if sender == "user":
            alignment = ft.MainAxisAlignment.END
            bgcolor = colors["user_bubble"]
            text_color = ft.colors.BLACK
            avatar = ft.CircleAvatar(
                content=ft.Text("You", color=ft.colors.WHITE, size=12),
                bgcolor=colors["primary"],
                radius=15,
            )
        elif sender == "ai":
            alignment = ft.MainAxisAlignment.START
            bgcolor = colors["ai_bubble"]
            text_color = ft.colors.BLACK
            avatar = ft.CircleAvatar(
                content=ft.Icon(ft.icons.SMART_TOY, color=ft.colors.WHITE, size=15),
                bgcolor=colors["primary"],
                radius=15,
            )
        else:  # system
            alignment = ft.MainAxisAlignment.CENTER
            bgcolor = colors["system_bubble"] if not is_alert else colors["alert"]
            text_color = ft.colors.BLACK if not is_alert else ft.colors.WHITE
            avatar = None

        # Create the message bubble
        bubble = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        value=content,
                        color=text_color,
                        selectable=True,
                        size=14,
                    ),
                    ft.Container(
                        content=ft.Text(
                            value=time_str,
                            size=10,
                            color=ft.colors.GREY_700 if not is_alert else ft.colors.WHITE70,
                        ),
                        alignment=ft.alignment.bottom_right,
                    ),
                ],
                spacing=5,
                tight=True,
            ),
            bgcolor=bgcolor,
            border_radius=10,
            padding=10,
            width=None if sender == "system" else 280,
        )

        # Add the bubble to a row with proper alignment
        if sender == "system":
            row = ft.Row(
                controls=[bubble],
                alignment=alignment,
            )
        else:
            row = ft.Row(
                controls=[
                    avatar if sender == "ai" else ft.Container(width=0),
                    bubble,
                    avatar if sender == "user" else ft.Container(width=0),
                ],
                alignment=alignment,
                vertical_alignment=ft.CrossAxisAlignment.START,
            )

        # Add to chat list
        chat_list.controls.append(row)
        page.update()
    
    # Load initial chat history
    for message in chat_history:
        add_message_bubble(message)
    
    def send_message(_=None):
        """Send a message."""
        nonlocal is_emergency, location_attached, current_location
        
        # Get message text
        message_text = message_input.value.strip()

        # Don't send empty messages
        if not message_text:
            return

        # Create message data
        message_data = {
            "id": f"msg_{int(__import__('time').time())}",
            "sender": "user",
            "content": message_text,
            "timestamp": __import__('datetime').datetime.now().isoformat(),
            "is_alert": is_emergency,
        }

        # Add location if attached
        if location_attached and current_location:
            message_data["location"] = current_location

        # Add to chat list
        add_message_bubble(message_data)

        # Clear input
        message_input.value = ""
        page.update()

        # Call the on_send callback
        if on_send:
            on_send(
                message_text,
                current_location if location_attached else None,
                is_emergency
            )

        # Reset emergency and location flags
        is_emergency = False
        location_attached = False
        current_location = None

        # Update indicators
        emergency_indicator.visible = is_emergency
        location_indicator.visible = location_attached
        page.update()
    
    def toggle_emergency(e):
        """Toggle emergency mode."""
        nonlocal is_emergency
        is_emergency = not is_emergency
        e.control.selected = is_emergency
        emergency_indicator.visible = is_emergency
        page.update()
    
    def toggle_location(e):
        """Toggle location attachment."""
        nonlocal location_attached, current_location
        location_attached = not location_attached
        e.control.selected = location_attached

        # In a real app, this would get the actual location
        # For now, we'll use a dummy location
        if location_attached:
            current_location = {
                "latitude": -26.1052,
                "longitude": 28.0560,
                "address": "Sandton, Johannesburg"
            }
        else:
            current_location = None

        location_indicator.visible = location_attached
        page.update()
    
    # Create quick action buttons
    quick_actions = ft.Row(
        controls=[
            ft.IconButton(
                icon=ft.icons.WARNING_ROUNDED,
                tooltip="Mark as emergency",
                icon_color=ft.colors.GREY_400,
                selected_icon_color=colors["alert"],
                on_click=toggle_emergency,
                style=ft.ButtonStyle(
                    shape=ft.CircleBorder(),
                    padding=10,
                ),
            ),
            ft.IconButton(
                icon=ft.icons.LOCATION_ON,
                tooltip="Share location",
                visible=enable_location,
                icon_color=ft.colors.GREY_400,
                selected_icon_color=colors["primary"],
                on_click=toggle_location,
                style=ft.ButtonStyle(
                    shape=ft.CircleBorder(),
                    padding=10,
                ),
            ) if enable_location else ft.Container(),
            ft.IconButton(
                icon=ft.icons.ATTACH_FILE,
                tooltip="Attach media",
                visible=enable_media,
                style=ft.ButtonStyle(
                    shape=ft.CircleBorder(),
                    padding=10,
                ),
            ) if enable_media else ft.Container(),
            ft.IconButton(
                icon=ft.icons.MIC,
                tooltip="Voice message",
                style=ft.ButtonStyle(
                    shape=ft.CircleBorder(),
                    padding=10,
                ),
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_AROUND,
        spacing=5,
    )
    
    # Create input row with buttons
    input_row = ft.Row(
        controls=[
            message_input,
            ft.IconButton(
                icon=ft.icons.SEND_ROUNDED,
                tooltip="Send message",
                on_click=send_message,
                icon_color=colors["primary"],
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=5,
    )
    
    # Create status indicators row
    status_row = ft.Row(
        controls=[
            emergency_indicator,
            location_indicator,
        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.END,
    )
    
    # Create main layout
    main_layout = ft.Column(
        controls=[
            # Chat header
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(
                            name=ft.icons.SHIELD,
                            color=colors["primary"],
                            size=24,
                        ),
                        ft.Text(
                            value="SafeWayAI Assistant",
                            weight=ft.FontWeight.BOLD,
                            size=18,
                        ),
                        ft.Container(
                            content=ft.Text(
                                "ONLINE",
                                color=ft.colors.WHITE,
                                weight=ft.FontWeight.BOLD,
                                size=12,
                            ),
                            bgcolor=ft.colors.GREEN,
                            padding=ft.padding.symmetric(horizontal=10, vertical=5),
                            border_radius=15,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=ft.padding.all(15),
                bgcolor=ft.colors.SURFACE_VARIANT,
                border_radius=ft.border_radius.only(top_left=10, top_right=10),
            ),
            
            # Quick actions
            ft.Container(
                content=quick_actions,
                padding=ft.padding.symmetric(horizontal=15, vertical=10),
                bgcolor=ft.colors.SURFACE,
                border=ft.border.only(bottom=ft.BorderSide(1, ft.colors.GREY_300)),
            ),
            
            # Chat messages list
            ft.Container(
                content=chat_list,
                expand=True,
                padding=10,
            ),
            
            # Status indicators
            ft.Container(
                content=status_row,
                padding=ft.padding.symmetric(horizontal=15, vertical=5),
            ),
            
            # Input area
            ft.Container(
                content=input_row,
                padding=ft.padding.all(15),
                bgcolor=ft.colors.SURFACE,
                border=ft.border.only(top=ft.BorderSide(1, ft.colors.GREY_300)),
            ),
        ],
        spacing=0,
        expand=True,
    )
    
    # Public methods that can be accessed from outside
    def add_message(message):
        """Add a new message to the chat."""
        add_message_bubble(message)
    
    def update_chat_history(new_chat_history):
        """Update the entire chat history."""
        chat_list.controls.clear()
        for message in new_chat_history:
            add_message_bubble(message)
    
    # Attach public methods to the main layout
    main_layout.add_message = add_message
    main_layout.update_chat_history = update_chat_history
    
    return main_layout
