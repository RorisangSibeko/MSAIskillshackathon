import flet as ft
import logging
from app.utils.enhanced_theme import get_color_scheme
from app.components.header import Header
from app.components.chat_interface import create_chat_interface
from app.components.simple_improved_chat import (
    create_quick_actions_panel,
    create_safety_status_card
)

# Configure logging
logger = logging.getLogger(__name__)

# Get color scheme
colors = get_color_scheme()

class CommunityScreen:
    """
    Community screen for the SafeWayAI application.
    Shows community safety initiatives and allows users to connect with local safety groups.
    Also provides an AI-powered community chat for reporting and safety information.
    """

    def __init__(self, app):
        self.app = app
        self.page = app.page
        self.current_tab_index = 0

        # Initialize AI services if available
        if hasattr(app, 'service_manager'):
            if hasattr(app.service_manager, 'ai_chat_service'):
                self.ai_chat_service = app.service_manager.ai_chat_service
            else:
                self.ai_chat_service = None

            if hasattr(app.service_manager, 'ai_safety_service'):
                self.ai_safety_service = app.service_manager.ai_safety_service
            else:
                self.ai_safety_service = None
        else:
            # If service manager not available, we'll handle this in the build method
            self.ai_chat_service = None
            self.ai_safety_service = None

    def build(self):
        """Build the community screen UI."""
        # Create header with back button
        header = Header(
            title="Community Safety",
            show_logo=True,
            show_back_button=True,
            on_back=lambda _: self.page.go("/")
        ).build()

        # Create tabs for organizing content
        tabs = ft.Tabs(
            selected_index=self.current_tab_index,
            on_change=self._handle_tab_change,
            tabs=[
                # Community Tab
                ft.Tab(
                    text="Community",
                    icon=ft.icons.PEOPLE,
                    content=self._build_community_content()
                ),

                # AI Chat Tab
                ft.Tab(
                    text="Safety Chat",
                    icon=ft.icons.CHAT,
                    content=self._build_chat_content()
                ),

                # Alerts Tab
                ft.Tab(
                    text="Alerts",
                    icon=ft.icons.NOTIFICATIONS,
                    content=self._build_alerts_content()
                ),
            ],
            expand=True,
        )

        # Create main content container
        content = ft.Container(
            content=tabs,
            expand=True,
            padding=0,
        )

        # Create emergency button
        emergency_button = ft.FloatingActionButton(
            icon=ft.icons.EMERGENCY,
            bgcolor=colors["danger"],
            tooltip="Emergency SOS",
            on_click=self._trigger_emergency,
        )

        # Create the view
        return ft.View(
            route="/community",
            controls=[content],
            appbar=header,
            floating_action_button=emergency_button,
            padding=0
        )

    def _handle_tab_change(self, e):
        """Handle tab selection changes."""
        self.current_tab_index = e.control.selected_index

    def _build_community_content(self):
        """Build the community tab content."""
        # Create social impact banner
        banner = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        name="diversity_3",
                        color=ft.colors.WHITE,
                        size=20,
                    ),
                    ft.Text(
                        value="Building safer communities together",
                        color=ft.colors.WHITE,
                        weight=ft.FontWeight.BOLD,
                        size=14,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
            ),
            bgcolor=colors["community"],
            padding=ft.padding.symmetric(horizontal=16, vertical=8),
            border_radius=20,
            margin=ft.margin.only(bottom=15),
        )

        # Create community groups section
        community_groups = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(
                                    name="groups",
                                    color=colors["community"],
                                    size=28,
                                ),
                                ft.Text(
                                    value="Local Safety Groups",
                                    weight=ft.FontWeight.BOLD,
                                    size=18,
                                ),
                            ],
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=10,
                        ),
                        ft.Divider(height=1, color=ft.colors.GREY_300),

                        # Group 1
                        ft.ListTile(
                            leading=ft.Icon(name="group", color=colors["community"]),
                            title=ft.Text("Johannesburg Community Watch"),
                            subtitle=ft.Text("Active members: 1,245"),
                            trailing=ft.IconButton(
                                icon=ft.icons.ADD,
                                tooltip="Join group",
                                icon_color=colors["community"],
                            ),
                        ),

                        # Group 2
                        ft.ListTile(
                            leading=ft.Icon(name="group", color=colors["community"]),
                            title=ft.Text("Sandton Safety Initiative"),
                            subtitle=ft.Text("Active members: 876"),
                            trailing=ft.IconButton(
                                icon=ft.icons.ADD,
                                tooltip="Join group",
                                icon_color=colors["community"],
                            ),
                        ),

                        # Group 3
                        ft.ListTile(
                            leading=ft.Icon(name="group", color=colors["community"]),
                            title=ft.Text("Pretoria Neighborhood Watch"),
                            subtitle=ft.Text("Active members: 932"),
                            trailing=ft.IconButton(
                                icon=ft.icons.ADD,
                                tooltip="Join group",
                                icon_color=colors["community"],
                            ),
                        ),

                        ft.ElevatedButton(
                            text="Find More Groups",
                            icon=ft.icons.SEARCH,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8),
                                padding=ft.padding.all(15),
                            ),
                            on_click=lambda _: self._show_more_groups(),
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

        # Create community events section
        community_events = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(
                                    name="event",
                                    color=colors["community"],
                                    size=28,
                                ),
                                ft.Text(
                                    value="Upcoming Safety Events",
                                    weight=ft.FontWeight.BOLD,
                                    size=18,
                                ),
                            ],
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=10,
                        ),
                        ft.Divider(height=1, color=ft.colors.GREY_300),

                        # Event 1
                        ft.ListTile(
                            leading=ft.Icon(name="calendar_today", color=colors["community"]),
                            title=ft.Text("Safety Awareness Workshop"),
                            subtitle=ft.Text("May 15, 2025 • Sandton Community Center"),
                            trailing=ft.IconButton(
                                icon=ft.icons.ADD_ALERT,
                                tooltip="Set reminder",
                                icon_color=colors["community"],
                            ),
                        ),

                        # Event 2
                        ft.ListTile(
                            leading=ft.Icon(name="calendar_today", color=colors["community"]),
                            title=ft.Text("Community Patrol Training"),
                            subtitle=ft.Text("May 22, 2025 • Johannesburg Central"),
                            trailing=ft.IconButton(
                                icon=ft.icons.ADD_ALERT,
                                tooltip="Set reminder",
                                icon_color=colors["community"],
                            ),
                        ),

                        ft.ElevatedButton(
                            text="View All Events",
                            icon=ft.icons.EVENT,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8),
                                padding=ft.padding.all(15),
                            ),
                            on_click=lambda _: self._show_all_events(),
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

        # Create community reporting section
        community_reporting = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(
                                    name="report",
                                    color=colors["community"],
                                    size=28,
                                ),
                                ft.Text(
                                    value="Community Reporting",
                                    weight=ft.FontWeight.BOLD,
                                    size=18,
                                ),
                            ],
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=10,
                        ),
                        ft.Divider(height=1, color=ft.colors.GREY_300),

                        ft.Text(
                            value="Help make your community safer by reporting safety concerns",
                            size=16,
                        ),

                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    text="Report Incident",
                                    icon=ft.icons.WARNING,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                        padding=ft.padding.all(15),
                                    ),
                                    on_click=lambda _: self.page.go("/report"),
                                ),
                                ft.ElevatedButton(
                                    text="View Reports",
                                    icon=ft.icons.MAP,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                        padding=ft.padding.all(15),
                                    ),
                                    on_click=lambda _: self._view_reports(),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            spacing=10,
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

        # Combine all elements in a scrollable column
        return ft.Container(
            content=ft.Column(
                controls=[
                    # Title section
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    value="Community Safety",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(
                                    value="Connect with local safety initiatives",
                                    size=16,
                                    color=ft.colors.GREY_700,
                                ),
                            ],
                        ),
                        padding=ft.padding.only(left=20, right=20, top=20, bottom=10),
                    ),

                    # Banner
                    ft.Container(
                        content=banner,
                        padding=ft.padding.symmetric(horizontal=20),
                    ),

                    # Community groups
                    ft.Container(
                        content=community_groups,
                        padding=ft.padding.symmetric(horizontal=20),
                    ),

                    # Community events
                    ft.Container(
                        content=community_events,
                        padding=ft.padding.symmetric(horizontal=20),
                    ),

                    # Community reporting
                    ft.Container(
                        content=community_reporting,
                        padding=ft.padding.symmetric(horizontal=20, vertical=10),
                    ),
                ],
                spacing=0,
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
            padding=0,
        )

    def _show_more_groups(self):
        """Show more community groups."""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Finding more community groups in your area..."),
            action="OK",
        )
        self.page.snack_bar.open = True
        self.page.update()

    def _show_all_events(self):
        """Show all community events."""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Loading all community safety events..."),
            action="OK",
        )
        self.page.snack_bar.open = True
        self.page.update()

    def _view_reports(self):
        """View community reports."""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Loading community safety reports..."),
            action="OK",
        )
        self.page.snack_bar.open = True
        self.page.update()

    def _build_chat_content(self):
        """Build the AI chat tab content."""
        # Create title section
        title_section = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        value="Community Safety Chat",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        value="Report incidents and get safety information",
                        size=16,
                        color=ft.colors.GREY_700,
                    ),
                ],
            ),
            padding=ft.padding.only(left=20, right=20, top=20, bottom=10),
        )

        # Create safety status card with visible styling
        safety_status = ft.Container(
            content=create_safety_status_card(),
            padding=ft.padding.symmetric(horizontal=20),
            margin=ft.margin.only(bottom=10),
        )

        # Create quick actions panel with event handlers
        quick_actions_panel = create_quick_actions_panel()

        # Add event handlers to the quick action buttons
        if isinstance(quick_actions_panel, ft.Container) and isinstance(quick_actions_panel.content, ft.Row):
            # Get the buttons from the row
            buttons = quick_actions_panel.content.controls

            # Add event handlers to each button
            if len(buttons) >= 1:  # Emergency button
                buttons[0].on_click = lambda _: self._trigger_emergency()

            if len(buttons) >= 2:  # Report button
                buttons[1].on_click = lambda _: self._show_report_dialog()

            if len(buttons) >= 3:  # Safe Route button
                buttons[2].on_click = lambda _: self._show_safe_route_dialog()

        quick_actions = ft.Container(
            content=quick_actions_panel,
            padding=ft.padding.symmetric(horizontal=20),
            margin=ft.margin.only(bottom=10),
        )

        # Create info banner
        info_banner = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        name="info",
                        color=ft.colors.WHITE,
                        size=20,
                    ),
                    ft.Text(
                        value="Your reports help keep the community safe",
                        color=ft.colors.WHITE,
                        weight=ft.FontWeight.BOLD,
                        size=14,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
            ),
            bgcolor=colors["community"],
            padding=ft.padding.symmetric(horizontal=16, vertical=8),
            border_radius=20,
            margin=ft.margin.only(bottom=15),
        )

        # Create chat interface
        if self.ai_chat_service:
            # Get chat history from service
            chat_history = self.ai_chat_service.get_chat_history()

            # Create chat interface with actual service
            chat_interface = create_chat_interface(
                page=self.page,
                on_send=self._send_chat_message,
                chat_history=chat_history,
                colors={
                    "primary": colors["community"],
                    "user_bubble": colors["community_light"],
                    "ai_bubble": ft.colors.GREY_100,
                    "system_bubble": colors["warning_light"],
                    "alert": colors["danger"],
                },
                enable_location=True,
                enable_media=False,
                placeholder_text="Ask about safety or report an incident...",
            )
        else:
            # Create placeholder chat interface
            chat_interface = ft.Column(
                controls=[
                    ft.Text(
                        value="AI Chat service is not available",
                        size=16,
                        color=ft.colors.GREY_700,
                    ),
                    ft.ElevatedButton(
                        text="Refresh",
                        on_click=lambda _: self.page.go("/community"),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            )

        # Combine all elements in a scrollable column
        return ft.Container(
            content=ft.Column(
                controls=[
                    title_section,
                    safety_status,
                    quick_actions,
                    ft.Container(
                        content=info_banner,
                        padding=ft.padding.symmetric(horizontal=20),
                    ),
                    ft.Container(
                        content=chat_interface,
                        padding=ft.padding.symmetric(horizontal=20),
                        expand=True,
                    ),
                ],
                spacing=10,
                expand=True,
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=0,
        )

    def _build_alerts_content(self):
        """Build the alerts tab content."""
        # Create title section
        title_section = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        value="Community Alerts",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        value="Recent safety alerts in your area",
                        size=16,
                        color=ft.colors.GREY_700,
                    ),
                ],
            ),
            padding=ft.padding.only(left=20, right=20, top=20, bottom=10),
        )

        # Create alerts list
        alerts_list = ft.ListView(
            spacing=10,
            padding=10,
        )

        # Add sample alerts
        sample_alerts = [
            {
                "title": "Suspicious Activity",
                "description": "Suspicious person watching ATM users on Main Street",
                "location": "Main Street, Sandton",
                "timestamp": "2 hours ago",
                "severity": "medium",
            },
            {
                "title": "Infrastructure Issue",
                "description": "Street lights not working on Park Avenue",
                "location": "Park Avenue, Sandton",
                "timestamp": "Yesterday",
                "severity": "low",
            },
            {
                "title": "Theft Report",
                "description": "Smartphone theft reported at Central Mall",
                "location": "Central Mall, Sandton",
                "timestamp": "Yesterday",
                "severity": "medium",
            },
        ]

        for alert in sample_alerts:
            # Determine color based on severity
            if alert["severity"] == "high":
                severity_color = colors["danger"]
            elif alert["severity"] == "medium":
                severity_color = colors["warning"]
            else:
                severity_color = colors["info"]

            # Create alert card
            alert_card = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Container(
                                        width=12,
                                        height=50,
                                        bgcolor=severity_color,
                                        border_radius=ft.border_radius.only(
                                            top_left=5,
                                            bottom_left=5,
                                        ),
                                    ),
                                    ft.Column(
                                        controls=[
                                            ft.Text(
                                                value=alert["title"],
                                                weight=ft.FontWeight.BOLD,
                                                size=16,
                                            ),
                                            ft.Text(
                                                value=alert["description"],
                                                size=14,
                                            ),
                                            ft.Row(
                                                controls=[
                                                    ft.Icon(
                                                        name="location_on",
                                                        color=ft.colors.GREY_600,
                                                        size=14,
                                                    ),
                                                    ft.Text(
                                                        value=alert["location"],
                                                        size=12,
                                                        color=ft.colors.GREY_600,
                                                    ),
                                                ],
                                                spacing=5,
                                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            ),
                                        ],
                                        spacing=5,
                                        expand=True,
                                    ),
                                    ft.Column(
                                        controls=[
                                            ft.Text(
                                                value=alert["timestamp"],
                                                size=12,
                                                color=ft.colors.GREY_600,
                                            ),
                                            ft.IconButton(
                                                icon=ft.icons.MAP,
                                                tooltip="View on map",
                                                icon_color=colors["community"],
                                                icon_size=20,
                                            ),
                                        ],
                                        spacing=5,
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    ),
                                ],
                                spacing=10,
                            ),
                        ],
                    ),
                    padding=ft.padding.only(right=15),
                ),
                elevation=2,
            )

            # Add to list
            alerts_list.controls.append(alert_card)

        # Create filter options
        filter_options = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(
                        value="Filter by:",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Chip(
                        label=ft.Text("All"),
                        selected=True,
                        selected_color=colors["community"],
                    ),
                    ft.Chip(
                        label=ft.Text("High Priority"),
                        selected_color=colors["danger"],
                    ),
                    ft.Chip(
                        label=ft.Text("Recent"),
                        selected_color=colors["community"],
                    ),
                ],
                spacing=10,
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
        )

        # Combine all elements
        return ft.Container(
            content=ft.Column(
                controls=[
                    title_section,
                    filter_options,
                    ft.Container(
                        content=alerts_list,
                        padding=ft.padding.symmetric(horizontal=20),
                        expand=True,
                    ),
                ],
                spacing=0,
                expand=True,
            ),
            padding=0,
        )

    def _send_chat_message(self, message_text, location=None, is_emergency=False):
        """
        Send a message to the AI chat service.

        Args:
            message_text (str): The message text
            location (dict, optional): User's location
            is_emergency (bool): Whether this is an emergency message
        """
        logger.info(f"Sending chat message: '{message_text}', is_emergency: {is_emergency}, has_location: {location is not None}")

        if not self.ai_chat_service:
            # If service is not available, show error message
            logger.error("AI Chat service is not available")
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("AI Chat service is not available"),
                action="OK",
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

        try:
            # Send message to service
            logger.info("Calling AI Chat service send_message method")
            response = self.ai_chat_service.send_message(
                message_text,
                user_location=location,
                is_emergency=is_emergency
            )
            logger.info(f"Received AI response: {response['id']}")

            # Get updated chat history
            logger.info("Getting updated chat history")
            chat_history = self.ai_chat_service.get_chat_history()
            logger.info(f"Retrieved {len(chat_history)} messages from chat history")

            # Find the chat interface in the UI
            logger.info("Updating chat interface with new messages")
            chat_tab = self.page.views[-1].controls[0].content.tabs[1]

            # The chat interface is the last control in the column
            chat_container = chat_tab.content.content.controls[-1]
            chat_interface = chat_container.content

            # Update the chat interface with the new messages
            chat_interface.update_chat_history(chat_history)
            logger.info("Chat interface updated")

            # Update the UI
            self.page.update()
            logger.info("Page updated")

            # If this is an emergency, also trigger emergency response
            if is_emergency:
                logger.info("Triggering emergency response")
                self._trigger_emergency()

                # Show a more prominent emergency notification
                self.page.banner = ft.Banner(
                    bgcolor=colors["danger"],
                    leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.WHITE, size=40),
                    content=ft.Text(
                        "Emergency services have been notified. Stay safe and follow any instructions provided.",
                        color=ft.colors.WHITE,
                    ),
                    actions=[
                        ft.TextButton("DISMISS", on_click=lambda _: setattr(self.page, "banner", None)),
                    ],
                )
                self.page.banner.open = True
                self.page.update()

        except Exception as e:
            logger.error(f"Error sending chat message: {e}")
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error: {str(e)}"),
                action="OK",
            )
            self.page.snack_bar.open = True
            self.page.update()

    def _trigger_emergency(self, _=None):
        """Trigger emergency response."""
        # This would integrate with emergency services

        # Show a more prominent emergency notification with a banner
        self.page.banner = ft.Banner(
            bgcolor=colors["danger"],
            leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.WHITE, size=40),
            content=ft.Column(
                controls=[
                    ft.Text(
                        "EMERGENCY ALERT",
                        color=ft.colors.WHITE,
                        weight=ft.FontWeight.BOLD,
                        size=18,
                    ),
                    ft.Text(
                        "Emergency services have been notified. Stay safe and follow any instructions provided.",
                        color=ft.colors.WHITE,
                    ),
                ],
                spacing=5,
            ),
            actions=[
                ft.TextButton("DISMISS", on_click=lambda _: setattr(self.page, "banner", None)),
                ft.TextButton("CALL EMERGENCY", on_click=lambda _: self._call_emergency()),
            ],
        )
        self.page.banner.open = True

        # Also show a snack bar for immediate notification
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Emergency services have been notified. Stay safe."),
            action="OK",
            bgcolor=colors["danger"],
        )
        self.page.snack_bar.open = True

        # Update the UI
        self.page.update()

    def _call_emergency(self):
        """Call emergency services."""
        # This would integrate with the device's phone system
        # For now, we'll just show a dialog
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Emergency Call"),
            content=ft.Text("This would initiate a call to emergency services (10111 or 112)."),
            actions=[
                ft.TextButton("Cancel", on_click=lambda _: setattr(self.page, "dialog", None)),
                ft.TextButton("Call", on_click=lambda _: self._show_calling_dialog()),
            ],
        )
        self.page.dialog.open = True
        self.page.update()

    def _show_calling_dialog(self):
        """Show a dialog indicating that emergency services are being called."""
        # Close the previous dialog
        self.page.dialog = None

        # Show a new dialog with calling status
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Calling Emergency Services"),
            content=ft.Column(
                controls=[
                    ft.ProgressRing(),
                    ft.Text("Connecting to emergency services..."),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            actions=[
                ft.TextButton("End Call", on_click=lambda _: setattr(self.page, "dialog", None)),
            ],
        )
        self.page.dialog.open = True
        self.page.update()

    def _show_report_dialog(self):
        """Show a dialog for reporting incidents."""
        # Create a dialog with a form for reporting incidents
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Report Incident"),
            content=ft.Column(
                controls=[
                    ft.Text("Please provide details about the incident:"),
                    ft.Dropdown(
                        label="Incident Type",
                        options=[
                            ft.dropdown.Option("Suspicious Activity"),
                            ft.dropdown.Option("Infrastructure Issue"),
                            ft.dropdown.Option("Theft"),
                            ft.dropdown.Option("Assault"),
                            ft.dropdown.Option("Other"),
                        ],
                        width=300,
                    ),
                    ft.TextField(
                        label="Location",
                        hint_text="Where did this happen?",
                        width=300,
                    ),
                    ft.TextField(
                        label="Description",
                        hint_text="Provide details about what happened",
                        multiline=True,
                        min_lines=3,
                        max_lines=5,
                        width=300,
                    ),
                    ft.Row(
                        controls=[
                            ft.Checkbox(label="Share my location"),
                            ft.Checkbox(label="Report anonymously"),
                        ],
                    ),
                ],
                spacing=15,
                width=300,
                height=400,
                scroll=ft.ScrollMode.AUTO,
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda _: setattr(self.page, "dialog", None)),
                ft.TextButton("Submit", on_click=lambda _: self._submit_report()),
            ],
        )
        self.page.dialog.open = True
        self.page.update()

    def _submit_report(self):
        """Submit an incident report."""
        # Close the dialog
        self.page.dialog = None

        # Show a confirmation message
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Your report has been submitted. Thank you for helping keep the community safe."),
            action="OK",
            bgcolor=colors["success"],
        )
        self.page.snack_bar.open = True
        self.page.update()

    def _show_safe_route_dialog(self):
        """Show a dialog for finding safe routes."""
        # Create a dialog with a form for finding safe routes
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Find Safe Route"),
            content=ft.Column(
                controls=[
                    ft.Text("Please provide your destination:"),
                    ft.TextField(
                        label="Starting Point",
                        hint_text="Your current location",
                        width=300,
                    ),
                    ft.TextField(
                        label="Destination",
                        hint_text="Where are you going?",
                        width=300,
                    ),
                    ft.Dropdown(
                        label="Travel Mode",
                        options=[
                            ft.dropdown.Option("Walking"),
                            ft.dropdown.Option("Public Transport"),
                            ft.dropdown.Option("Driving"),
                        ],
                        width=300,
                    ),
                    ft.Dropdown(
                        label="Safety Priority",
                        options=[
                            ft.dropdown.Option("Balanced (Default)"),
                            ft.dropdown.Option("Maximum Safety"),
                            ft.dropdown.Option("Fastest Route"),
                        ],
                        width=300,
                    ),
                    ft.Row(
                        controls=[
                            ft.Checkbox(label="Avoid high-crime areas"),
                            ft.Checkbox(label="Prefer well-lit routes"),
                        ],
                    ),
                ],
                spacing=15,
                width=300,
                height=400,
                scroll=ft.ScrollMode.AUTO,
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda _: setattr(self.page, "dialog", None)),
                ft.TextButton("Find Route", on_click=lambda _: self._find_safe_route()),
            ],
        )
        self.page.dialog.open = True
        self.page.update()

    def _find_safe_route(self):
        """Find a safe route."""
        # Close the dialog
        self.page.dialog = None

        # Show a loading message
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Finding the safest route to your destination..."),
            action="OK",
        )
        self.page.snack_bar.open = True
        self.page.update()

        # Navigate to the navigation screen
        self.page.go("/navigation")
