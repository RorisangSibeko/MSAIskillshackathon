"""
Chat interface component for the SafeWayAI application.
"""

import flet as ft
import time
from datetime import datetime
from typing import Callable, List, Dict, Any, Optional

def create_chat_interface(
    page: ft.Page,
    on_send: Callable[[str, Optional[Dict[str, Any]], bool], None],
    chat_history: List[Dict[str, Any]] = None,
    colors: Dict[str, str] = None,
    enable_location: bool = True,
    enable_media: bool = False,
    placeholder_text: str = "Type a message...",
):
    """
    Create a chat interface component.
    
    Args:
        page: The Flet page
        on_send: Callback function when a message is sent
        chat_history: Initial chat history
        colors: Color scheme to use
        enable_location: Whether to enable location sharing
        enable_media: Whether to enable media attachments
        placeholder_text: Placeholder text for the input field
        
    Returns:
        ft.Control: The chat interface component
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
    )
    
    # State variables
    is_emergency = False
    location_attached = False
    current_location = None
    
    # Create emergency indicator
    emergency_indicator = ft.Container(
        content=ft.Text(
            "EMERGENCY MODE",
            color=ft.colors.WHITE,
            weight=ft.FontWeight.BOLD,
            size=12,
        ),
        bgcolor=colors["alert"],
        padding=ft.padding.symmetric(horizontal=10, vertical=5),
        border_radius=15,
        visible=False,
    )
    
    # Create location indicator
    location_indicator = ft.Container(
        content=ft.Text(
            "Location attached",
            color=ft.colors.WHITE,
            weight=ft.FontWeight.BOLD,
            size=12,
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
        timestamp = message.get("timestamp", datetime.now().isoformat())
        is_alert = message.get("is_alert", False)

        # Convert timestamp to readable format
        try:
            dt = datetime.fromisoformat(timestamp)
            time_str = dt.strftime("%I:%M %p")
        except:
            time_str = "Now"

        # Determine alignment and colors based on sender
        if sender == "user":
            alignment = ft.MainAxisAlignment.END
            bgcolor = colors["user_bubble"]
            text_color = ft.colors.BLACK
        elif sender == "ai":
            alignment = ft.MainAxisAlignment.START
            bgcolor = colors["ai_bubble"]
            text_color = ft.colors.BLACK
        else:  # system
            alignment = ft.MainAxisAlignment.CENTER
            bgcolor = colors["system_bubble"] if not is_alert else colors["alert"]
            text_color = ft.colors.BLACK if not is_alert else ft.colors.WHITE

        # Create the message bubble
        bubble = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        value=content,
                        color=text_color,
                        selectable=True,
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
        row = ft.Row(
            controls=[bubble],
            alignment=alignment,
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
            "id": f"msg_{int(time.time())}",
            "sender": "user",
            "content": message_text,
            "timestamp": datetime.now().isoformat(),
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
    
    def attach_media(_):
        """Attach media to the message."""
        # This would open a file picker in a real implementation
        pass
    
    # Connect event handlers
    message_input.on_submit = send_message
    
    # Create input row with buttons
    input_row = ft.Row(
        controls=[
            # Emergency toggle button
            ft.IconButton(
                icon=ft.icons.WARNING_ROUNDED,
                tooltip="Mark as emergency",
                icon_color=ft.colors.GREY_400,
                selected_icon_color=colors["alert"],
                on_click=toggle_emergency,
            ),
            # Message input field
            message_input,
            # Location button (if enabled)
            ft.IconButton(
                icon=ft.icons.LOCATION_ON,
                tooltip="Share location",
                visible=enable_location,
                icon_color=ft.colors.GREY_400,
                selected_icon_color=colors["primary"],
                on_click=toggle_location,
            ) if enable_location else ft.Container(),
            # Media button (if enabled)
            ft.IconButton(
                icon=ft.icons.ATTACH_FILE,
                tooltip="Attach media",
                visible=enable_media,
                on_click=attach_media,
            ) if enable_media else ft.Container(),
            # Send button
            ft.IconButton(
                icon=ft.icons.SEND_ROUNDED,
                tooltip="Send message",
                on_click=send_message,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
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
            # Chat messages list
            ft.Container(
                content=chat_list,
                expand=True,
                border=ft.border.all(1, ft.colors.GREY_300),
                border_radius=10,
                padding=10,
            ),
            # Status indicators
            status_row,
            # Input area
            ft.Container(
                content=input_row,
                padding=ft.padding.only(top=10, bottom=10),
            ),
        ],
        spacing=10,
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
