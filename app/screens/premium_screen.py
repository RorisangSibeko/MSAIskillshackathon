import flet as ft
from typing import Any, Dict, List, Optional

class PremiumScreen:
    """Premium subscription screen for the SafeWayAI application."""
    
    def __init__(self, app):
        self.app = app
        
    def build(self) -> ft.View:
        """Build the premium subscription screen UI."""
        # Get current subscription tier
        current_tier = self.app.auth_service.get_subscription_tier()
        
        # Get subscription tiers from the subscription service
        tiers = self.app.subscription_service.get_subscription_tiers()
        
        # Create subscription cards
        subscription_cards = []
        for tier in tiers:
            tier_id = tier.get("id")
            is_current = tier_id == current_tier
            
            # Calculate yearly savings
            savings = self.app.subscription_service.calculate_subscription_savings(tier_id)
            
            # Create feature list
            features = []
            for feature in tier.get("features", []):
                features.append(
                    ft.Row([
                        ft.Icon(name=ft.icons.CHECK_CIRCLE, color=ft.colors.GREEN, size=16),
                        ft.Text(feature, size=14)
                    ], vertical_alignment=ft.CrossAxisAlignment.CENTER)
                )
            
            # Create subscription card
            card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        # Tier name and badge
                        ft.Row([
                            ft.Text(tier.get("name", ""), size=20, weight=ft.FontWeight.BOLD),
                            ft.Container(
                                content=ft.Text("Current Plan", size=12, color=ft.colors.WHITE),
                                bgcolor=ft.colors.BLUE,
                                border_radius=15,
                                padding=ft.padding.only(left=10, right=10, top=5, bottom=5),
                                visible=is_current
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        
                        # Description
                        ft.Text(tier.get("description", ""), size=14, color=ft.colors.GREY_700),
                        
                        ft.Divider(),
                        
                        # Pricing
                        ft.Row([
                            ft.Column([
                                ft.Text("Monthly", size=14, color=ft.colors.GREY_700),
                                ft.Row([
                                    ft.Text("$", size=16, color=ft.colors.GREY_800),
                                    ft.Text(f"{tier.get('price_monthly', 0):.2f}", size=24, weight=ft.FontWeight.BOLD)
                                ])
                            ]),
                            ft.Column([
                                ft.Row([
                                    ft.Text("Yearly", size=14, color=ft.colors.GREY_700),
                                    ft.Container(
                                        content=ft.Text(f"Save {savings}%", size=12, color=ft.colors.WHITE),
                                        bgcolor=ft.colors.GREEN,
                                        border_radius=15,
                                        padding=ft.padding.only(left=8, right=8, top=2, bottom=2),
                                        visible=savings > 0
                                    )
                                ]),
                                ft.Row([
                                    ft.Text("$", size=16, color=ft.colors.GREY_800),
                                    ft.Text(f"{tier.get('price_yearly', 0):.2f}", size=24, weight=ft.FontWeight.BOLD)
                                ])
                            ])
                        ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                        
                        ft.Divider(),
                        
                        # Features
                        ft.Column(controls=features, spacing=10),
                        
                        # Subscribe buttons
                        ft.Container(
                            content=ft.Column([
                                ft.ElevatedButton(
                                    "Subscribe Monthly",
                                    icon=ft.icons.PAYMENT,
                                    on_click=lambda e, t=tier_id: self._handle_subscribe(e, t, False),
                                    disabled=is_current
                                ),
                                ft.ElevatedButton(
                                    "Subscribe Yearly",
                                    icon=ft.icons.CALENDAR_TODAY,
                                    on_click=lambda e, t=tier_id: self._handle_subscribe(e, t, True),
                                    disabled=is_current
                                )
                            ], spacing=10),
                            margin=ft.margin.only(top=20),
                            visible=tier_id != "enterprise"  # Hide for enterprise tier
                        ),
                        
                        # Enterprise contact button
                        ft.Container(
                            content=ft.ElevatedButton(
                                "Contact Sales",
                                icon=ft.icons.BUSINESS,
                                on_click=self._handle_enterprise_contact
                            ),
                            margin=ft.margin.only(top=20),
                            visible=tier_id == "enterprise"
                        )
                    ]),
                    padding=20,
                    width=300
                ),
                elevation=5 if is_current else 2
            )
            
            subscription_cards.append(card)
        
        # Create main content
        content = ft.Column(
            controls=[
                # Header
                ft.Container(
                    content=ft.Column([
                        ft.Text("Premium Subscriptions", size=24, weight=ft.FontWeight.BOLD),
                        ft.Text("Enhance your safety with premium features", size=16, color=ft.colors.GREY_700)
                    ]),
                    margin=ft.margin.only(bottom=20),
                    padding=ft.padding.only(left=20, right=20, top=20)
                ),
                
                # Subscription cards
                ft.Container(
                    content=ft.Row(
                        controls=subscription_cards,
                        scroll=ft.ScrollMode.AUTO
                    ),
                    padding=ft.padding.only(left=20, right=20)
                ),
                
                # Insurance integration section
                ft.Container(
                    content=ft.Column([
                        ft.Text("Insurance Discounts", size=20, weight=ft.FontWeight.BOLD),
                        ft.Text("Premium subscribers can qualify for insurance discounts", size=16),
                        
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column([
                                    ft.Row([
                                        ft.Icon(name=ft.icons.SAVINGS, color=ft.colors.GREEN, size=24),
                                        ft.Text("Save on Insurance Premiums", weight=ft.FontWeight.BOLD, size=16)
                                    ]),
                                    ft.Text("Connect your SafeWayAI account with participating insurance providers to receive discounts:"),
                                    ft.Column([
                                        ft.Row([
                                            ft.Icon(name=ft.icons.CHECK_CIRCLE, color=ft.colors.GREEN, size=16),
                                            ft.Text("Up to 15% off home insurance")
                                        ]),
                                        ft.Row([
                                            ft.Icon(name=ft.icons.CHECK_CIRCLE, color=ft.colors.GREEN, size=16),
                                            ft.Text("Up to 10% off renters insurance")
                                        ]),
                                        ft.Row([
                                            ft.Icon(name=ft.icons.CHECK_CIRCLE, color=ft.colors.GREEN, size=16),
                                            ft.Text("Special rates for business insurance")
                                        ])
                                    ], spacing=10),
                                    ft.ElevatedButton(
                                        "View Participating Insurers",
                                        icon=ft.icons.BUSINESS_CENTER,
                                        on_click=self._show_insurance_partners
                                    )
                                ]),
                                padding=20
                            )
                        )
                    ]),
                    margin=ft.margin.only(top=30),
                    padding=ft.padding.only(left=20, right=20)
                ),
                
                # IoT integration section
                ft.Container(
                    content=ft.Column([
                        ft.Text("IoT & Security System Integration", size=20, weight=ft.FontWeight.BOLD),
                        ft.Text("Connect your smart home devices for enhanced safety", size=16),
                        
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column([
                                    ft.Row([
                                        ft.Icon(name=ft.icons.SMART_TOY, color=ft.colors.BLUE, size=24),
                                        ft.Text("Supported Systems & Devices", weight=ft.FontWeight.BOLD, size=16)
                                    ]),
                                    ft.Text("Premium subscribers can connect with these security systems:"),
                                    ft.Wrap(
                                        spacing=10,
                                        run_spacing=10,
                                        controls=[
                                            ft.Chip(label=system.get("name")) 
                                            for system in self.app.iot_service.get_supported_systems()
                                        ]
                                    ),
                                    ft.Text("And these smart home devices:"),
                                    ft.Wrap(
                                        spacing=10,
                                        run_spacing=10,
                                        controls=[
                                            ft.Chip(
                                                label=device.get("name"),
                                                leading=ft.Icon(
                                                    name=self._get_device_icon(device.get("type"))
                                                )
                                            ) 
                                            for device in self.app.iot_service.get_supported_devices()[:5]  # Show first 5
                                        ]
                                    ),
                                    ft.ElevatedButton(
                                        "View All Compatible Devices",
                                        icon=ft.icons.DEVICES,
                                        on_click=lambda _: self.app.page.go("/iot")
                                    )
                                ]),
                                padding=20
                            )
                        )
                    ]),
                    margin=ft.margin.only(top=30, bottom=30),
                    padding=ft.padding.only(left=20, right=20)
                )
            ],
            scroll=ft.ScrollMode.AUTO
        )
        
        # Create the view
        return ft.View(
            route="/premium",
            controls=[content],
            appbar=ft.AppBar(
                title=ft.Text("Premium Features"),
                center_title=True,
                bgcolor=ft.colors.SURFACE_VARIANT,
                leading=ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    on_click=lambda _: self.app.page.go("/")
                )
            ),
            padding=0
        )
        
    def _handle_subscribe(self, e, tier_id, is_yearly):
        """Handle subscription purchase."""
        # In a real app, this would open a payment flow
        # For the hackathon, we'll simulate a successful purchase
        
        # Show confirmation dialog
        plan_type = "yearly" if is_yearly else "monthly"
        tier_details = self.app.subscription_service.get_tier_details(tier_id)
        price = tier_details.get("price_yearly" if is_yearly else "price_monthly", 0)
        
        def confirm_subscription(e):
            # Process the subscription
            success = self.app.subscription_service.process_subscription_purchase(
                self.app.auth_service.get_current_user().get("username"),
                tier_id,
                "credit_card",  # Simulated payment method
                is_yearly
            )
            
            if success:
                # Update the user's subscription tier
                self.app.auth_service.update_subscription(tier_id)
                
                # Show success message
                e.page.show_snack_bar(ft.SnackBar(
                    content=ft.Text(f"Successfully subscribed to {tier_details.get('name')} plan!"),
                    bgcolor=ft.colors.GREEN
                ))
                
                # Refresh the page
                e.page.go("/premium")
            else:
                # Show error message
                e.page.show_snack_bar(ft.SnackBar(
                    content=ft.Text("Subscription failed. Please try again."),
                    bgcolor=ft.colors.RED
                ))
            
            # Close the dialog
            e.page.dialog.open = False
            e.page.update()
        
        # Create and show the dialog
        e.page.dialog = ft.AlertDialog(
            title=ft.Text(f"Subscribe to {tier_details.get('name')}"),
            content=ft.Column([
                ft.Text(f"You are about to subscribe to the {tier_details.get('name')} plan ({plan_type})."),
                ft.Text(f"Price: ${price:.2f}/{plan_type}"),
                ft.Text("In a real app, this would open a payment form.")
            ], tight=True),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: setattr(e.page.dialog, "open", False)),
                ft.ElevatedButton("Subscribe", on_click=confirm_subscription)
            ]
        )
        e.page.dialog.open = True
        e.page.update()
        
    def _handle_enterprise_contact(self, e):
        """Handle enterprise contact request."""
        # Get enterprise contact info
        contact_info = self.app.subscription_service.get_enterprise_contact_info()
        
        # Show contact info dialog
        e.page.dialog = ft.AlertDialog(
            title=ft.Text("Enterprise Solutions"),
            content=ft.Column([
                ft.Text("Contact our enterprise sales team:"),
                ft.Text(f"Email: {contact_info.get('email')}"),
                ft.Text(f"Phone: {contact_info.get('phone')}"),
                ft.Text(f"Website: {contact_info.get('website')}")
            ], tight=True),
            actions=[
                ft.TextButton("Close", on_click=lambda e: setattr(e.page.dialog, "open", False))
            ]
        )
        e.page.dialog.open = True
        e.page.update()
        
    def _show_insurance_partners(self, e):
        """Show insurance partners dialog."""
        # Get insurance integrations
        insurance_integrations = self.app.iot_service.get_insurance_integrations()
        
        # Create list of insurance partners
        partners = []
        for insurance in insurance_integrations:
            partners.append(
                ft.Column([
                    ft.Text(insurance.get("name"), weight=ft.FontWeight.BOLD),
                    ft.Text(f"Discount: Up to {insurance.get('discount_percentage')}%"),
                    ft.Text("Requirements: " + ", ".join(insurance.get("requirements", [])))
                ])
            )
            
        # Show dialog
        e.page.dialog = ft.AlertDialog(
            title=ft.Text("Participating Insurance Partners"),
            content=ft.Column(
                controls=partners,
                spacing=20
            ),
            actions=[
                ft.TextButton("Close", on_click=lambda e: setattr(e.page.dialog, "open", False))
            ]
        )
        e.page.dialog.open = True
        e.page.update()
        
    def _get_device_icon(self, device_type):
        """Get an icon for a device type."""
        icons = {
            "camera": ft.icons.CAMERA_ALT,
            "lock": ft.icons.LOCK,
            "panic_button": ft.icons.EMERGENCY,
            "alarm": ft.icons.ALARM,
            "sensor": ft.icons.SENSORS,
            "speaker": ft.icons.SPEAKER,
            "medical": ft.icons.MEDICAL_SERVICES
        }
        return icons.get(device_type, ft.icons.DEVICE_UNKNOWN)
