import flet as ft
from typing import Any, Dict, List, Optional

class GBVResourcesScreen:
    """Gender-Based Violence resources screen for the SafeWayAI application."""
    
    def __init__(self, app):
        self.app = app
        self.current_tab = "hotlines"
        
    def build(self) -> ft.View:
        """Build the GBV resources screen UI."""
        # Create tabs
        tabs = ft.Tabs(
            selected_index=0,
            on_change=self._handle_tab_change,
            tabs=[
                ft.Tab(
                    text="Emergency Hotlines",
                    icon=ft.icons.PHONE
                ),
                ft.Tab(
                    text="Safety Plans",
                    icon=ft.icons.SHIELD
                ),
                ft.Tab(
                    text="Warning Signs",
                    icon=ft.icons.WARNING
                ),
                ft.Tab(
                    text="Risk Assessment",
                    icon=ft.icons.ASSESSMENT
                ),
                ft.Tab(
                    text="Resources",
                    icon=ft.icons.LIBRARY_BOOKS
                )
            ]
        )
        
        # Create tab content
        tab_content = ft.Container(
            content=self._get_tab_content(0),
            padding=ft.padding.only(left=20, right=20, top=10, bottom=20)
        )
        
        # Create emergency button
        emergency_button = ft.Container(
            content=ft.ElevatedButton(
                "Emergency Help",
                icon=ft.icons.EMERGENCY,
                color=ft.colors.WHITE,
                bgcolor=ft.colors.RED,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10)
                ),
                on_click=self._handle_emergency
            ),
            padding=ft.padding.only(left=20, right=20, bottom=20)
        )
        
        # Create main content
        content = ft.Column(
            controls=[
                # Header
                ft.Container(
                    content=ft.Column([
                        ft.Text("Gender-Based Violence Resources", size=24, weight=ft.FontWeight.BOLD),
                        ft.Text("Access support, safety plans, and emergency resources", size=16, color=ft.colors.GREY_700)
                    ]),
                    padding=ft.padding.only(left=20, right=20, top=20, bottom=10)
                ),
                
                # Safety notice
                ft.Container(
                    content=ft.Row([
                        ft.Icon(name=ft.icons.INFO, color=ft.colors.BLUE, size=24),
                        ft.Column([
                            ft.Text("Safety Notice", weight=ft.FontWeight.BOLD),
                            ft.Text("If you're concerned someone might monitor your device, consider using a safer device or clearing your browser history after viewing.")
                        ])
                    ]),
                    padding=15,
                    margin=ft.margin.only(left=20, right=20, bottom=20),
                    border_radius=10,
                    bgcolor=ft.colors.BLUE_50
                ),
                
                # Tabs
                tabs,
                
                # Tab content
                tab_content,
                
                # Emergency button
                emergency_button
            ],
            scroll=ft.ScrollMode.AUTO
        )
        
        # Create the view
        return ft.View(
            route="/gbv_resources",
            controls=[content],
            appbar=ft.AppBar(
                title=ft.Text("GBV Resources"),
                center_title=True,
                bgcolor=ft.colors.SURFACE_VARIANT,
                leading=ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    on_click=lambda _: self.app.page.go("/")
                ),
                actions=[
                    ft.IconButton(
                        icon=ft.icons.EXIT_TO_APP,
                        tooltip="Quick Exit",
                        on_click=self._quick_exit
                    )
                ]
            ),
            padding=0
        )
        
    def _handle_tab_change(self, e):
        """Handle tab change."""
        # Update the tab content
        tab_content = self._get_tab_content(e.control.selected_index)
        e.page.controls[0].controls[3].content = tab_content
        e.page.update()
        
    def _get_tab_content(self, tab_index):
        """Get content for the selected tab."""
        if tab_index == 0:
            # Hotlines tab
            return self._build_hotlines_tab()
        elif tab_index == 1:
            # Safety plans tab
            return self._build_safety_plans_tab()
        elif tab_index == 2:
            # Warning signs tab
            return self._build_warning_signs_tab()
        elif tab_index == 3:
            # Risk assessment tab
            return self._build_risk_assessment_tab()
        elif tab_index == 4:
            # Resources tab
            return self._build_resources_tab()
        else:
            return ft.Text("Content not available")
            
    def _build_hotlines_tab(self):
        """Build the hotlines tab content."""
        # Get hotlines from the GBV service
        hotlines = self.app.gbv_service.get_emergency_hotlines()
        
        # Create hotline cards
        hotline_cards = []
        for hotline in hotlines:
            card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(hotline.get("name", ""), size=18, weight=ft.FontWeight.BOLD),
                        ft.Divider(),
                        ft.Row([
                            ft.Icon(name=ft.icons.PHONE, color=ft.colors.BLUE),
                            ft.Text(f"Phone: {hotline.get('phone', '')}", selectable=True)
                        ]),
                        ft.Row([
                            ft.Icon(name=ft.icons.ACCESS_TIME, color=ft.colors.BLUE),
                            ft.Text(f"Hours: {hotline.get('hours', '')}")
                        ]),
                        ft.Row([
                            ft.Icon(name=ft.icons.LANGUAGE, color=ft.colors.BLUE),
                            ft.Text(f"Languages: {', '.join(hotline.get('languages', []))}")
                        ]),
                        ft.Row([
                            ft.Icon(name=ft.icons.LINK, color=ft.colors.BLUE),
                            ft.TextButton(
                                "Visit Website",
                                url=hotline.get("website", "")
                            )
                        ]) if "website" in hotline else ft.Container(),
                        ft.Row([
                            ft.Icon(name=ft.icons.SMS, color=ft.colors.BLUE),
                            ft.Text(f"SMS: {hotline.get('sms', '')}", selectable=True)
                        ]) if "sms" in hotline else ft.Container(),
                        ft.ElevatedButton(
                            "Call Now",
                            icon=ft.icons.CALL,
                            on_click=lambda _, phone=hotline.get("phone"): self._handle_call(phone)
                        )
                    ]),
                    padding=15
                )
            )
            hotline_cards.append(card)
            
        return ft.Column(
            controls=hotline_cards,
            spacing=20
        )
        
    def _build_safety_plans_tab(self):
        """Build the safety plans tab content."""
        # Get safety plans from the GBV service
        safety_plans = self.app.gbv_service.get_safety_plans()
        
        # Create safety plan cards
        safety_plan_cards = []
        for plan in safety_plans:
            # Create steps list
            steps = []
            for i, step in enumerate(plan.get("steps", [])):
                steps.append(
                    ft.Row([
                        ft.Container(
                            content=ft.Text(str(i + 1), color=ft.colors.WHITE),
                            width=24,
                            height=24,
                            border_radius=12,
                            bgcolor=ft.colors.BLUE,
                            alignment=ft.alignment.center
                        ),
                        ft.Text(step)
                    ], vertical_alignment=ft.CrossAxisAlignment.CENTER)
                )
                
            # Create card
            card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(plan.get("name", ""), size=18, weight=ft.FontWeight.BOLD),
                        ft.Divider(),
                        ft.Column(controls=steps, spacing=10),
                        ft.ElevatedButton(
                            "Save Plan",
                            icon=ft.icons.SAVE,
                            on_click=lambda _, plan_id=plan.get("id"): self._handle_save_plan(plan_id)
                        )
                    ]),
                    padding=15
                )
            )
            safety_plan_cards.append(card)
            
        # Add personalized safety plan button
        personalized_button = ft.Container(
            content=ft.ElevatedButton(
                "Create Personalized Safety Plan",
                icon=ft.icons.PERSON,
                on_click=self._handle_personalized_plan
            ),
            margin=ft.margin.only(bottom=20)
        )
            
        return ft.Column(
            controls=[personalized_button] + safety_plan_cards,
            spacing=20
        )
        
    def _build_warning_signs_tab(self):
        """Build the warning signs tab content."""
        # Get warning signs from the GBV service
        warning_signs = self.app.gbv_service.get_warning_signs()
        
        # Create warning sign cards
        warning_sign_cards = []
        for category in warning_signs:
            # Create signs list
            signs = []
            for sign in category.get("signs", []):
                signs.append(
                    ft.Row([
                        ft.Icon(name=ft.icons.WARNING, color=ft.colors.ORANGE, size=16),
                        ft.Text(sign)
                    ], vertical_alignment=ft.CrossAxisAlignment.CENTER)
                )
                
            # Create card
            card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(category.get("category", ""), size=18, weight=ft.FontWeight.BOLD),
                        ft.Divider(),
                        ft.Column(controls=signs, spacing=10)
                    ]),
                    padding=15
                )
            )
            warning_sign_cards.append(card)
            
        return ft.Column(
            controls=warning_sign_cards,
            spacing=20
        )
        
    def _build_risk_assessment_tab(self):
        """Build the risk assessment tab content."""
        # Create risk assessment form
        assessment_questions = [
            {"id": "threatened_weapon", "text": "Has your partner ever threatened you with a weapon?"},
            {"id": "strangled", "text": "Has your partner ever tried to choke/strangle you?"},
            {"id": "controlling", "text": "Is your partner very controlling of your daily activities?"},
            {"id": "jealous", "text": "Is your partner extremely jealous?"},
            {"id": "threatened_kill", "text": "Has your partner ever threatened to kill you?"},
            {"id": "forced_sex", "text": "Has your partner forced you into sexual activities?"},
            {"id": "gun_access", "text": "Does your partner have access to guns?"},
            {"id": "suicide_threats", "text": "Has your partner threatened suicide?"},
            {"id": "unemployed", "text": "Is your partner unemployed?"},
            {"id": "child_not_theirs", "text": "Do you have children that are not your partner's?"},
            {"id": "spying", "text": "Does your partner spy on you or stalk you?"},
            {"id": "pregnant", "text": "Are you currently pregnant?"},
            {"id": "separated", "text": "Have you recently separated or tried to separate?"}
        ]
        
        question_controls = []
        for question in assessment_questions:
            question_controls.append(
                ft.Row([
                    ft.Text(question["text"], expand=True),
                    ft.Switch(value=False, data=question["id"])
                ])
            )
            
        assessment_form = ft.Column(
            controls=[
                ft.Text("Risk Assessment", size=18, weight=ft.FontWeight.BOLD),
                ft.Text("This assessment helps identify potential risk factors. Your answers are not stored."),
                ft.Divider(),
                ft.Column(controls=question_controls, spacing=10),
                ft.ElevatedButton(
                    "Assess Risk",
                    icon=ft.icons.ASSESSMENT,
                    on_click=self._handle_risk_assessment
                )
            ],
            spacing=15
        )
        
        return assessment_form
        
    def _build_resources_tab(self):
        """Build the resources tab content."""
        # Get educational resources from the GBV service
        resources = self.app.gbv_service.get_educational_resources()
        
        # Create resource list
        resource_items = []
        for resource in resources:
            icon = ft.icons.ARTICLE
            if resource.get("type") == "pdf":
                icon = ft.icons.PICTURE_AS_PDF
            elif resource.get("type") == "video":
                icon = ft.icons.VIDEO_LIBRARY
                
            resource_items.append(
                ft.ListTile(
                    leading=ft.Icon(name=icon),
                    title=ft.Text(resource.get("title", "")),
                    subtitle=ft.Text(f"Type: {resource.get('type', '')}"),
                    trailing=ft.IconButton(
                        icon=ft.icons.OPEN_IN_NEW,
                        tooltip="Open",
                        on_click=lambda _, url=resource.get("url"): self._handle_open_resource(url)
                    )
                )
            )
            
        # Get legal resources
        legal_resources = self.app.gbv_service.get_legal_resources()
        
        # Create legal resource list
        legal_items = []
        for resource in legal_resources:
            legal_items.append(
                ft.ListTile(
                    leading=ft.Icon(name=ft.icons.GAVEL),
                    title=ft.Text(resource.get("name", "")),
                    subtitle=ft.Text(resource.get("description", "")),
                    trailing=ft.IconButton(
                        icon=ft.icons.OPEN_IN_NEW,
                        tooltip="Open",
                        on_click=lambda _, url=resource.get("website"): self._handle_open_resource(url)
                    )
                )
            )
            
        return ft.Column(
            controls=[
                ft.Text("Educational Resources", size=18, weight=ft.FontWeight.BOLD),
                ft.Column(controls=resource_items),
                ft.Divider(),
                ft.Text("Legal Resources", size=18, weight=ft.FontWeight.BOLD),
                ft.Column(controls=legal_items)
            ],
            spacing=15
        )
        
    def _handle_call(self, phone):
        """Handle call button click."""
        # In a real app, this would initiate a phone call
        # For the hackathon, we'll show a dialog
        
        def confirm_call(e):
            # Close the dialog
            e.page.dialog.open = False
            e.page.update()
            
            # Show confirmation
            e.page.show_snack_bar(ft.SnackBar(
                content=ft.Text(f"Initiating call to {phone}...")
            ))
        
        # Create and show the dialog
        self.app.page.dialog = ft.AlertDialog(
            title=ft.Text("Confirm Call"),
            content=ft.Text(f"Would you like to call {phone}?"),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: setattr(e.page.dialog, "open", False)),
                ft.ElevatedButton("Call", on_click=confirm_call)
            ]
        )
        self.app.page.dialog.open = True
        self.app.page.update()
        
    def _handle_save_plan(self, plan_id):
        """Handle save plan button click."""
        # In a real app, this would save the plan to the user's account
        # For the hackathon, we'll show a dialog
        
        # Get the plan
        plan = self.app.gbv_service.get_safety_plan_by_id(plan_id)
        if not plan:
            return
            
        # Show confirmation
        self.app.page.show_snack_bar(ft.SnackBar(
            content=ft.Text(f"Safety plan '{plan.get('name')}' saved")
        ))
        
    def _handle_personalized_plan(self, e):
        """Handle personalized safety plan button click."""
        # Create risk factor checkboxes
        risk_factors = [
            {"id": "children", "text": "I have children"},
            {"id": "pets", "text": "I have pets"},
            {"id": "firearms", "text": "My partner has access to firearms"},
            {"id": "stalking", "text": "My partner has stalked or followed me"},
            {"id": "rural", "text": "I live in a rural/isolated area"},
            {"id": "immigration", "text": "I have immigration concerns"}
        ]
        
        checkboxes = []
        for factor in risk_factors:
            checkboxes.append(
                ft.Checkbox(label=factor["text"], value=False, data=factor["id"])
            )
            
        def create_plan(e):
            # Get selected risk factors
            selected_factors = []
            for checkbox in checkboxes:
                if checkbox.value:
                    selected_factors.append(checkbox.data)
                    
            # Create personalized plan
            plan = self.app.gbv_service.create_personalized_safety_plan(selected_factors)
            
            # Close the dialog
            e.page.dialog.open = False
            e.page.update()
            
            # Show the plan in a new dialog
            steps = []
            for i, step in enumerate(plan.get("steps", [])):
                steps.append(
                    ft.Row([
                        ft.Container(
                            content=ft.Text(str(i + 1), color=ft.colors.WHITE),
                            width=24,
                            height=24,
                            border_radius=12,
                            bgcolor=ft.colors.BLUE,
                            alignment=ft.alignment.center
                        ),
                        ft.Text(step)
                    ], vertical_alignment=ft.CrossAxisAlignment.CENTER)
                )
                
            e.page.dialog = ft.AlertDialog(
                title=ft.Text("Your Personalized Safety Plan"),
                content=ft.Column(
                    controls=[
                        ft.Text("This plan has been customized based on your specific situation:"),
                        ft.Container(
                            content=ft.Column(controls=steps, spacing=10),
                            margin=ft.margin.only(top=10)
                        )
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    height=400
                ),
                actions=[
                    ft.TextButton("Close", on_click=lambda e: setattr(e.page.dialog, "open", False)),
                    ft.ElevatedButton("Save Plan", on_click=lambda e: self.app.page.show_snack_bar(
                        ft.SnackBar(content=ft.Text("Personalized safety plan saved"))
                    ))
                ]
            )
            e.page.dialog.open = True
            e.page.update()
        
        # Create and show the dialog
        e.page.dialog = ft.AlertDialog(
            title=ft.Text("Create Personalized Safety Plan"),
            content=ft.Column(
                controls=[
                    ft.Text("Select all that apply to your situation:"),
                    ft.Column(controls=checkboxes)
                ]
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: setattr(e.page.dialog, "open", False)),
                ft.ElevatedButton("Create Plan", on_click=create_plan)
            ]
        )
        e.page.dialog.open = True
        e.page.update()
        
    def _handle_risk_assessment(self, e):
        """Handle risk assessment button click."""
        # Get answers from the form
        answers = {}
        for control in e.page.controls[0].controls[3].content.controls[3].controls:
            question_id = control.controls[1].data
            answer = control.controls[1].value
            answers[question_id] = answer
            
        # Assess danger level
        assessment = self.app.gbv_service.assess_danger_level(answers)
        
        # Create recommendation list
        recommendations = []
        for rec in assessment.get("recommendations", []):
            recommendations.append(
                ft.Row([
                    ft.Icon(name=ft.icons.ARROW_RIGHT, color=ft.colors.BLUE),
                    ft.Text(rec)
                ])
            )
            
        # Create and show the dialog
        e.page.dialog = ft.AlertDialog(
            title=ft.Text("Risk Assessment Results"),
            content=ft.Column(
                controls=[
                    ft.Text(assessment.get("description", ""), weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=ft.Text(
                            f"Based on your answers, {assessment.get('factor_count')} out of {assessment.get('total_factors')} risk factors are present.",
                            color=ft.colors.GREY_700
                        ),
                        margin=ft.margin.only(top=10, bottom=10)
                    ),
                    ft.Text("Recommendations:", weight=ft.FontWeight.BOLD),
                    ft.Column(controls=recommendations, spacing=10),
                    ft.Container(
                        content=ft.Text(
                            "This assessment is for informational purposes only and does not guarantee safety. Always trust your instincts and seek professional help if you feel unsafe.",
                            color=ft.colors.GREY_700,
                            size=12
                        ),
                        margin=ft.margin.only(top=20)
                    )
                ],
                scroll=ft.ScrollMode.AUTO,
                height=300
            ),
            actions=[
                ft.TextButton("Close", on_click=lambda e: setattr(e.page.dialog, "open", False)),
                ft.ElevatedButton(
                    "Get Help Now",
                    on_click=lambda e: self.app.page.go("/gbv_resources")
                )
            ]
        )
        e.page.dialog.open = True
        e.page.update()
        
    def _handle_open_resource(self, url):
        """Handle opening a resource."""
        # In a real app, this would open the URL
        # For the hackathon, we'll show a dialog
        
        # Show confirmation
        self.app.page.show_snack_bar(ft.SnackBar(
            content=ft.Text(f"Opening resource: {url}")
        ))
        
    def _handle_emergency(self, e):
        """Handle emergency button click."""
        # Create and show the dialog
        e.page.dialog = ft.AlertDialog(
            title=ft.Text("Emergency Help"),
            content=ft.Column(
                controls=[
                    ft.Text("What type of emergency are you experiencing?"),
                    ft.ElevatedButton(
                        "Immediate Danger - Call 911",
                        icon=ft.icons.EMERGENCY,
                        bgcolor=ft.colors.RED,
                        color=ft.colors.WHITE,
                        on_click=lambda e: self._handle_call("911")
                    ),
                    ft.ElevatedButton(
                        "Domestic Violence Hotline",
                        icon=ft.icons.PHONE,
                        on_click=lambda e: self._handle_call("1-800-799-7233")
                    ),
                    ft.ElevatedButton(
                        "Crisis Text Line",
                        icon=ft.icons.SMS,
                        on_click=lambda e: self.app.page.show_snack_bar(
                            ft.SnackBar(content=ft.Text("Text HOME to 741741"))
                        )
                    ),
                    ft.ElevatedButton(
                        "Silent Alarm",
                        icon=ft.icons.NOTIFICATIONS_ACTIVE,
                        on_click=self._trigger_silent_alarm
                    )
                ],
                spacing=10
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: setattr(e.page.dialog, "open", False))
            ]
        )
        e.page.dialog.open = True
        e.page.update()
        
    def _trigger_silent_alarm(self, e):
        """Trigger a silent alarm."""
        # Close the dialog
        e.page.dialog.open = False
        e.page.update()
        
        # In a real app, this would trigger a silent alarm
        # For the hackathon, we'll simulate it
        
        # Show a subtle confirmation
        e.page.show_snack_bar(ft.SnackBar(
            content=ft.Text("Silent alarm activated. Help is on the way."),
            bgcolor=ft.colors.BLUE
        ))
        
        # Simulate triggering the panic detector
        self.app.panic_detector.manually_report_emergency("domestic_violence")
        
    def _quick_exit(self, e):
        """Handle quick exit button click."""
        # In a real app, this would immediately redirect to a neutral website
        # For the hackathon, we'll show a dialog
        
        # Create and show the dialog
        e.page.dialog = ft.AlertDialog(
            title=ft.Text("Quick Exit"),
            content=ft.Text("In a real app, this would immediately redirect you to a neutral website like weather.com or google.com to help protect your privacy."),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: setattr(e.page.dialog, "open", False)),
                ft.ElevatedButton("Exit Now", on_click=lambda e: self.app.page.go("/"))
            ]
        )
        e.page.dialog.open = True
        e.page.update()
