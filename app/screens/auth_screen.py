import flet as ft
from typing import Any, Dict, List, Optional

class AuthScreen:
    """Authentication screen for the SafeWayAI application."""

    def __init__(self, app):
        self.app = app
        self.show_register = False
        self.username_field = None
        self.password_field = None

    def build(self) -> ft.View:
        """Build the authentication screen UI."""
        # Create login form
        self.username_field = ft.TextField(
            label="Username",
            hint_text="Enter your username",
            prefix_icon=ft.icons.PERSON,
            autofocus=True,
            expand=True
        )

        self.password_field = ft.TextField(
            label="Password",
            hint_text="Enter your password",
            prefix_icon=ft.icons.LOCK,
            password=True,
            can_reveal_password=True,
            expand=True
        )

        login_form = ft.Column(
            controls=[
                ft.Text("Sign In", size=24, weight=ft.FontWeight.BOLD),
                self.username_field,
                self.password_field,
                ft.ElevatedButton(
                    "Sign In",
                    icon=ft.icons.LOGIN,
                    on_click=self._direct_login,
                    expand=True,
                    data="login_button"
                ),
                ft.Row([
                    ft.Text("Don't have an account?"),
                    ft.TextButton("Register", on_click=self._show_register_form)
                ], alignment=ft.MainAxisAlignment.CENTER)
            ],
            spacing=20,
            width=400,
            visible=not self.show_register
        )

        # Create registration form
        register_form = ft.Column(
            controls=[
                ft.Text("Create Account", size=24, weight=ft.FontWeight.BOLD),
                ft.TextField(
                    label="Full Name",
                    hint_text="Enter your full name",
                    prefix_icon=ft.icons.PERSON,
                    autofocus=True,
                    expand=True
                ),
                ft.TextField(
                    label="Email",
                    hint_text="Enter your email",
                    prefix_icon=ft.icons.EMAIL,
                    keyboard_type=ft.KeyboardType.EMAIL,
                    expand=True
                ),
                ft.TextField(
                    label="Phone",
                    hint_text="Enter your phone number",
                    prefix_icon=ft.icons.PHONE,
                    keyboard_type=ft.KeyboardType.PHONE,
                    expand=True
                ),
                ft.TextField(
                    label="Username",
                    hint_text="Choose a username",
                    prefix_icon=ft.icons.ACCOUNT_CIRCLE,
                    expand=True
                ),
                ft.TextField(
                    label="Password",
                    hint_text="Choose a password",
                    prefix_icon=ft.icons.LOCK,
                    password=True,
                    can_reveal_password=True,
                    expand=True
                ),
                ft.TextField(
                    label="Confirm Password",
                    hint_text="Confirm your password",
                    prefix_icon=ft.icons.LOCK_CLOCK,
                    password=True,
                    can_reveal_password=True,
                    expand=True
                ),
                ft.ElevatedButton(
                    "Register",
                    icon=ft.icons.PERSON_ADD,
                    on_click=self._handle_register,
                    expand=True
                ),
                ft.Row([
                    ft.Text("Already have an account?"),
                    ft.TextButton("Sign In", on_click=self._show_login_form)
                ], alignment=ft.MainAxisAlignment.CENTER)
            ],
            spacing=20,
            width=400,
            visible=self.show_register
        )

        # Create the main content
        content = ft.Container(
            content=ft.Column([
                # Logo and app name
                ft.Container(
                    content=ft.Column([
                        ft.Icon(name=ft.icons.SHIELD, size=64, color=ft.colors.BLUE),
                        ft.Text("SafeWayAI", size=32, weight=ft.FontWeight.BOLD),
                        ft.Text("AI-Powered Safety & Emergency Detection", size=16, color=ft.colors.GREY_700)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    margin=ft.margin.only(bottom=40)
                ),

                # Forms
                login_form,
                register_form,

                # Demo account information
                ft.Container(
                    content=ft.Column([
                        ft.Text("Demo Accounts", weight=ft.FontWeight.BOLD),
                        ft.Text("Admin: admin / admin123"),
                        ft.Text("Responder: responder / respond123"),
                        ft.Text("Viewer: viewer / view123")
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    margin=ft.margin.only(top=40),
                    padding=10,
                    border_radius=5,
                    bgcolor=ft.colors.SURFACE_VARIANT
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            alignment=ft.alignment.center,
            padding=40
        )

        # Create the view
        return ft.View(
            route="/auth",
            controls=[content],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def _handle_login(self, e):
        """Handle login button click."""
        print("Login button clicked")

        # Find username and password fields directly
        username_field = None
        password_field = None

        # Search for the login form in the page structure
        for control in e.page.controls:
            if isinstance(control, ft.View):
                # Look for the container in the view
                for view_control in control.controls:
                    if isinstance(view_control, ft.Container):
                        # Look for the main column in the container
                        for container_control in view_control.content.controls:
                            if isinstance(container_control, ft.Column) and hasattr(container_control, "name") and container_control.name == "content":
                                # Look for the login form column
                                for column_control in container_control.controls:
                                    if isinstance(column_control, ft.Column) and column_control.visible:
                                        # This should be the login form
                                        for form_control in column_control.controls:
                                            if isinstance(form_control, ft.TextField) and form_control.label == "Username":
                                                username_field = form_control
                                                print(f"Found username field: {username_field.value}")
                                            elif isinstance(form_control, ft.TextField) and form_control.label == "Password":
                                                password_field = form_control
                                                print(f"Found password field: {password_field.value}")

        if not username_field or not password_field:
            print("Could not find username or password fields")
            e.page.snack_bar = ft.SnackBar(content=ft.Text("Login form fields not found"))
            e.page.snack_bar.open = True
            e.page.update()
            return

        username = username_field.value
        password = password_field.value

        print(f"Username: {username}, Password: {password}")

        # Validate input
        if not username or not password:
            print("Username or password is empty")
            e.page.snack_bar = ft.SnackBar(content=ft.Text("Please enter username and password"))
            e.page.snack_bar.open = True
            e.page.update()
            return

        # Attempt to login
        print(f"Attempting to login with username: {username}")
        if self.app.auth_service.login(username, password):
            print("Login successful, navigating to home")
            e.page.go("/")
        else:
            print("Login failed")
            e.page.snack_bar = ft.SnackBar(content=ft.Text("Invalid username or password"))
            e.page.snack_bar.open = True
            e.page.update()

    def _handle_register(self, e):
        """Handle register button click."""
        # Find the register form
        register_form = None
        for control in e.page.controls:
            if isinstance(control, ft.Container):
                for inner_control in control.content.controls:
                    if isinstance(inner_control, ft.Column) and not inner_control.visible:
                        continue
                    if isinstance(inner_control, ft.Column) and inner_control.visible:
                        register_form = inner_control
                        break

        if not register_form:
            e.page.snack_bar = ft.SnackBar(content=ft.Text("Register form not found"))
            e.page.snack_bar.open = True
            e.page.update()
            return

        # Get registration fields
        full_name = ""
        email = ""
        phone = ""
        username = ""
        password = ""
        confirm_password = ""

        for control in register_form.controls:
            if isinstance(control, ft.TextField):
                if control.label == "Full Name":
                    full_name = control.value
                elif control.label == "Email":
                    email = control.value
                elif control.label == "Phone":
                    phone = control.value
                elif control.label == "Username":
                    username = control.value
                elif control.label == "Password":
                    password = control.value
                elif control.label == "Confirm Password":
                    confirm_password = control.value

        # Validate input
        if not full_name or not email or not phone or not username or not password:
            e.page.snack_bar = ft.SnackBar(content=ft.Text("Please fill in all fields"))
            e.page.snack_bar.open = True
            e.page.update()
            return

        if password != confirm_password:
            e.page.snack_bar = ft.SnackBar(content=ft.Text("Passwords do not match"))
            e.page.snack_bar.open = True
            e.page.update()
            return

        # Attempt to register
        if self.app.auth_service.register_user(username, password, full_name, email, phone):
            # Auto-login after registration
            self.app.auth_service.login(username, password)
            e.page.go("/")
        else:
            e.page.snack_bar = ft.SnackBar(content=ft.Text("Username already exists"))
            e.page.snack_bar.open = True
            e.page.update()

    def _show_register_form(self, e):
        """Show the registration form."""
        self.show_register = True

        # Find the login and register forms
        login_form = None
        register_form = None

        for control in e.page.controls:
            if isinstance(control, ft.Container):
                for inner_control in control.content.controls:
                    if isinstance(inner_control, ft.Column):
                        if len(inner_control.controls) > 0 and isinstance(inner_control.controls[0], ft.Text):
                            if inner_control.controls[0].value == "Sign In":
                                login_form = inner_control
                            elif inner_control.controls[0].value == "Create Account":
                                register_form = inner_control

        if login_form and register_form:
            login_form.visible = False
            register_form.visible = True
            e.page.update()

    def _show_login_form(self, e):
        """Show the login form."""
        self.show_register = False

        # Find the login and register forms
        login_form = None
        register_form = None

        for control in e.page.controls:
            if isinstance(control, ft.Container):
                for inner_control in control.content.controls:
                    if isinstance(inner_control, ft.Column):
                        if len(inner_control.controls) > 0 and isinstance(inner_control.controls[0], ft.Text):
                            if inner_control.controls[0].value == "Sign In":
                                login_form = inner_control
                            elif inner_control.controls[0].value == "Create Account":
                                register_form = inner_control

        if login_form and register_form:
            login_form.visible = True
            register_form.visible = False
            e.page.update()

    def _debug_login(self, e):
        """Debug login handler."""
        print("Debug login button clicked")

        # Try to find username and password fields directly
        username = ""
        password = ""

        # Find all text fields in the page
        text_fields = []
        for control in e.page.controls:
            if isinstance(control, ft.Container):
                self._find_text_fields(control, text_fields)

        print(f"Found {len(text_fields)} text fields")
        for i, field in enumerate(text_fields):
            print(f"Field {i}: label={field.label}, value={field.value}")
            if field.label == "Username":
                username = field.value
            elif field.label == "Password":
                password = field.value

        print(f"Username: {username}, Password: {password}")

        # Try to login
        if username and password:
            print("Attempting login with found credentials")
            if self.app.auth_service.login(username, password):
                print("Login successful, navigating to home")
                e.page.go("/")
            else:
                print("Login failed")
                e.page.snack_bar = ft.SnackBar(content=ft.Text("Invalid username or password"))
                e.page.snack_bar.open = True
                e.page.update()
        else:
            print("Username or password not found")
            e.page.snack_bar = ft.SnackBar(content=ft.Text("Please enter username and password"))
            e.page.snack_bar.open = True
            e.page.update()

    def _direct_login(self, e):
        """Direct login handler using instance variables."""
        print("Direct login button clicked")

        if not self.username_field or not self.password_field:
            print("Username or password field not initialized")
            e.page.snack_bar = ft.SnackBar(content=ft.Text("Login form not properly initialized"))
            e.page.snack_bar.open = True
            e.page.update()
            return

        username = self.username_field.value
        password = self.password_field.value

        print(f"Username: {username}, Password: {password}")

        # Validate input
        if not username or not password:
            print("Username or password is empty")
            e.page.snack_bar = ft.SnackBar(content=ft.Text("Please enter username and password"))
            e.page.snack_bar.open = True
            e.page.update()
            return

        # Attempt to login
        print(f"Attempting to login with username: {username}")
        if self.app.auth_service.login(username, password):
            print("Login successful, navigating to home")
            e.page.go("/")
        else:
            print("Login failed")
            e.page.snack_bar = ft.SnackBar(content=ft.Text("Invalid username or password"))
            e.page.snack_bar.open = True
            e.page.update()

    def _find_text_fields(self, control, text_fields):
        """Recursively find all text fields in a control."""
        if isinstance(control, ft.TextField):
            text_fields.append(control)
            return

        # Check if the control has controls attribute
        if hasattr(control, "controls"):
            for child in control.controls:
                self._find_text_fields(child, text_fields)

        # Check if the control has content attribute
        if hasattr(control, "content"):
            if control.content is not None:
                self._find_text_fields(control.content, text_fields)
