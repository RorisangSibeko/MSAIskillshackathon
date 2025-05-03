import os
import logging
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path

# In a production environment, this would use Stripe or another payment processor
# For the hackathon, we're simulating subscription management

class SubscriptionService:
    """
    Service for managing user subscriptions and payments.
    
    This service handles subscription tiers, features, and payment processing.
    It's designed to support the economic viability of SafeWayAI.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.subscriptions_file = Path("app/data/subscriptions.json")
        
        # Ensure the data directory exists
        self.subscriptions_file.parent.mkdir(exist_ok=True)
        
        # Load or create subscriptions file
        if not self.subscriptions_file.exists():
            self._create_default_subscriptions()
            
        # Load subscription tiers and features
        self.subscription_tiers = self._load_subscriptions()
        
    def _create_default_subscriptions(self):
        """Create default subscription tiers and features."""
        default_subscriptions = {
            "tiers": [
                {
                    "id": "basic",
                    "name": "Basic",
                    "price_monthly": 0.00,
                    "price_yearly": 0.00,
                    "description": "Basic safety monitoring for individuals",
                    "features": [
                        "AI monitoring with limited checks",
                        "Manual emergency reporting",
                        "Basic incident history (7 days)",
                        "1 emergency contact"
                    ]
                },
                {
                    "id": "standard",
                    "name": "Standard",
                    "price_monthly": 4.99,
                    "price_yearly": 49.99,
                    "description": "Enhanced safety for individuals and families",
                    "features": [
                        "Advanced AI monitoring with frequent checks",
                        "Manual and voice emergency reporting",
                        "Full incident history",
                        "5 emergency contacts",
                        "Safe route planning",
                        "GBV resources and support",
                        "Emergency services direct contact"
                    ]
                },
                {
                    "id": "premium",
                    "name": "Premium",
                    "price_monthly": 9.99,
                    "price_yearly": 99.99,
                    "description": "Complete safety solution with IoT integration",
                    "features": [
                        "Real-time AI monitoring",
                        "All Standard features",
                        "IoT device integration",
                        "Home security system connection",
                        "Unlimited emergency contacts",
                        "Insurance company integration",
                        "Priority emergency response",
                        "24/7 safety monitoring team access"
                    ]
                },
                {
                    "id": "enterprise",
                    "name": "Enterprise",
                    "price_monthly": 49.99,
                    "price_yearly": 499.99,
                    "description": "Comprehensive safety solution for businesses",
                    "features": [
                        "All Premium features",
                        "Multiple location monitoring",
                        "Employee safety management",
                        "Custom security integrations",
                        "API access for custom solutions",
                        "Dedicated account manager",
                        "Custom reporting and analytics",
                        "On-site security consultation"
                    ]
                }
            ],
            "feature_matrix": {
                "ai_monitoring": {
                    "basic": "limited",
                    "standard": "enhanced",
                    "premium": "real-time",
                    "enterprise": "real-time+"
                },
                "emergency_contacts": {
                    "basic": 1,
                    "standard": 5,
                    "premium": "unlimited",
                    "enterprise": "unlimited"
                },
                "incident_history": {
                    "basic": 7,  # days
                    "standard": 30,
                    "premium": 90,
                    "enterprise": "unlimited"
                },
                "iot_integration": {
                    "basic": False,
                    "standard": False,
                    "premium": True,
                    "enterprise": True
                },
                "insurance_integration": {
                    "basic": False,
                    "standard": False,
                    "premium": True,
                    "enterprise": True
                },
                "gbv_resources": {
                    "basic": "basic",
                    "standard": "enhanced",
                    "premium": "comprehensive",
                    "enterprise": "comprehensive"
                },
                "safe_routes": {
                    "basic": False,
                    "standard": True,
                    "premium": True,
                    "enterprise": True
                },
                "emergency_services": {
                    "basic": "basic",
                    "standard": "direct",
                    "premium": "priority",
                    "enterprise": "dedicated"
                }
            }
        }
        
        with open(self.subscriptions_file, 'w') as f:
            json.dump(default_subscriptions, f, indent=2)
            
        self.logger.info("Created default subscriptions file")
        
    def _load_subscriptions(self) -> Dict[str, Any]:
        """Load subscription information from the JSON file."""
        try:
            with open(self.subscriptions_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading subscriptions: {e}")
            return {"tiers": [], "feature_matrix": {}}
            
    def get_subscription_tiers(self) -> List[Dict[str, Any]]:
        """Get all available subscription tiers."""
        return self.subscription_tiers.get("tiers", [])
        
    def get_tier_details(self, tier_id: str) -> Optional[Dict[str, Any]]:
        """Get details for a specific subscription tier."""
        tiers = self.get_subscription_tiers()
        for tier in tiers:
            if tier["id"] == tier_id:
                return tier
        return None
        
    def get_feature_matrix(self) -> Dict[str, Dict[str, Any]]:
        """Get the feature comparison matrix for all tiers."""
        return self.subscription_tiers.get("feature_matrix", {})
        
    def check_feature_access(self, tier_id: str, feature: str) -> Any:
        """Check if a tier has access to a specific feature and at what level."""
        feature_matrix = self.get_feature_matrix()
        if feature in feature_matrix:
            return feature_matrix[feature].get(tier_id)
        return None
        
    def process_subscription_purchase(self, user_id: str, tier_id: str, 
                                     payment_method: str, is_yearly: bool = False) -> bool:
        """
        Process a subscription purchase.
        
        In a real implementation, this would integrate with Stripe or another
        payment processor. For the hackathon, we're simulating the purchase.
        """
        tier = self.get_tier_details(tier_id)
        if not tier:
            self.logger.error(f"Invalid tier ID: {tier_id}")
            return False
            
        # Simulate payment processing
        price = tier["price_yearly"] if is_yearly else tier["price_monthly"]
        
        # In a real implementation, this would call the payment processor API
        payment_successful = True  # Simulate successful payment
        
        if payment_successful:
            # Record the subscription (in a real app, this would update a database)
            self._record_subscription(user_id, tier_id, is_yearly)
            self.logger.info(f"Subscription purchased: {tier_id} for user {user_id}")
            return True
        else:
            self.logger.warning(f"Payment failed for subscription: {tier_id}, user: {user_id}")
            return False
            
    def _record_subscription(self, user_id: str, tier_id: str, is_yearly: bool):
        """Record a subscription purchase."""
        # In a real implementation, this would update a database
        # For the hackathon, we're just logging it
        duration = "yearly" if is_yearly else "monthly"
        self.logger.info(f"Subscription recorded: {tier_id} ({duration}) for user {user_id}")
        
    def calculate_subscription_savings(self, tier_id: str) -> float:
        """Calculate the savings percentage for yearly vs monthly subscription."""
        tier = self.get_tier_details(tier_id)
        if not tier or tier["price_monthly"] == 0:
            return 0.0
            
        monthly_annual_cost = tier["price_monthly"] * 12
        yearly_cost = tier["price_yearly"]
        
        if monthly_annual_cost == 0:
            return 0.0
            
        savings = (monthly_annual_cost - yearly_cost) / monthly_annual_cost * 100
        return round(savings, 2)
        
    def get_enterprise_contact_info(self) -> Dict[str, str]:
        """Get contact information for enterprise subscription inquiries."""
        return {
            "email": "enterprise@safewayai.com",
            "phone": "+1-800-SAFE-WAY",
            "website": "https://enterprise.safewayai.com"
        }
