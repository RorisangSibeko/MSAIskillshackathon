import os
import json
import logging
import random
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

class GBVService:
    """
    Service for Gender-Based Violence (GBV) prevention and support.
    
    This service provides resources, safety planning, and emergency response
    specifically tailored to address gender-based violence and femicide.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.resources_file = Path("app/data/gbv_resources.json")
        
        # Ensure the data directory exists
        self.resources_file.parent.mkdir(exist_ok=True)
        
        # Load or create resources file
        if not self.resources_file.exists():
            self._create_default_resources()
            
        # Load resources
        self.resources = self._load_resources()
        
    def _create_default_resources(self):
        """Create default GBV resources and support information."""
        default_resources = {
            "hotlines": [
                {
                    "name": "National Domestic Violence Hotline",
                    "phone": "1-800-799-7233",
                    "sms": "Text START to 88788",
                    "website": "https://www.thehotline.org/",
                    "hours": "24/7",
                    "languages": ["English", "Spanish", "200+ languages through interpretation"]
                },
                {
                    "name": "RAINN (Rape, Abuse & Incest National Network)",
                    "phone": "1-800-656-4673",
                    "website": "https://www.rainn.org/",
                    "hours": "24/7",
                    "languages": ["English", "Spanish"]
                },
                {
                    "name": "StrongHearts Native Helpline",
                    "phone": "1-844-762-8483",
                    "website": "https://strongheartshelpline.org/",
                    "hours": "24/7",
                    "languages": ["English"]
                },
                {
                    "name": "National Human Trafficking Hotline",
                    "phone": "1-888-373-7888",
                    "sms": "Text 233733",
                    "website": "https://humantraffickinghotline.org/",
                    "hours": "24/7",
                    "languages": ["English", "Spanish", "200+ languages through interpretation"]
                }
            ],
            "safety_plans": [
                {
                    "id": "immediate_danger",
                    "name": "Immediate Danger Plan",
                    "steps": [
                        "If you're in immediate danger, call emergency services (911)",
                        "If possible, move to a room with an exit and avoid kitchens or rooms with weapons",
                        "Use your emergency code word with family/friends",
                        "If you can't call safely, use the SafeWayAI silent alert feature",
                        "If you must leave immediately, go to your pre-identified safe location"
                    ]
                },
                {
                    "id": "planning_to_leave",
                    "name": "Planning to Leave",
                    "steps": [
                        "Prepare an emergency bag with essentials (keep in accessible location)",
                        "Gather important documents (ID, birth certificates, financial records)",
                        "Save money in a separate account if possible",
                        "Identify safe places you can go (shelter, friend's home, hotel)",
                        "Plan a safe time to leave when the abuser is not present",
                        "Memorize important phone numbers",
                        "If you have children, include them in your safety planning as appropriate"
                    ]
                },
                {
                    "id": "after_leaving",
                    "name": "After Leaving Safety Plan",
                    "steps": [
                        "Change your phone number and email addresses",
                        "Get a protective/restraining order if appropriate",
                        "Inform trusted people about your situation",
                        "Change your routine and travel routes",
                        "Consider changing locks if you remain in your home",
                        "Use SafeWayAI's location sharing with trusted contacts",
                        "Set up SafeWayAI's GBV monitoring for additional protection"
                    ]
                },
                {
                    "id": "digital_safety",
                    "name": "Digital Safety Plan",
                    "steps": [
                        "Use a secure device that the abuser doesn't have access to",
                        "Change passwords for all accounts",
                        "Check for tracking apps or spyware on your devices",
                        "Turn off location services when not needed",
                        "Use private browsing or incognito mode",
                        "Be cautious about what you share on social media",
                        "Consider getting a new phone with a new number"
                    ]
                }
            ],
            "shelters": [
                {
                    "name": "Example Shelter 1",
                    "phone": "555-123-4567",
                    "location": "Confidential - Call for information",
                    "services": ["Emergency housing", "Counseling", "Legal advocacy"]
                },
                {
                    "name": "Example Shelter 2",
                    "phone": "555-987-6543",
                    "location": "Confidential - Call for information",
                    "services": ["Emergency housing", "Children's programs", "Support groups"]
                }
            ],
            "legal_resources": [
                {
                    "name": "Legal Aid Society",
                    "description": "Free legal services for qualifying individuals",
                    "website": "https://www.legalaidexample.org/",
                    "phone": "555-111-2222"
                },
                {
                    "name": "Protective Order Information",
                    "description": "Information on obtaining protective orders",
                    "website": "https://www.courts.state.example.us/protective-orders",
                    "phone": "555-333-4444"
                }
            ],
            "warning_signs": [
                {
                    "category": "Controlling Behavior",
                    "signs": [
                        "Monitoring your whereabouts and activities",
                        "Controlling who you see and talk to",
                        "Making all decisions without your input",
                        "Isolating you from friends and family",
                        "Controlling finances and access to money"
                    ]
                },
                {
                    "category": "Emotional Abuse",
                    "signs": [
                        "Constant criticism and humiliation",
                        "Name-calling and insults",
                        "Gaslighting (making you question your reality)",
                        "Threatening harm to you, themselves, or others",
                        "Extreme jealousy and accusations"
                    ]
                },
                {
                    "category": "Physical Warning Signs",
                    "signs": [
                        "Destroying your property",
                        "Physical intimidation (blocking doorways, towering over you)",
                        "Driving recklessly with you in the car",
                        "Threatening with weapons",
                        "Any physical violence, no matter how 'minor'"
                    ]
                }
            ],
            "educational_resources": [
                {
                    "title": "Understanding the Cycle of Abuse",
                    "type": "article",
                    "url": "https://example.org/cycle-of-abuse"
                },
                {
                    "title": "Safety Planning Guide",
                    "type": "pdf",
                    "url": "https://example.org/safety-planning.pdf"
                },
                {
                    "title": "Helping a Friend in an Abusive Relationship",
                    "type": "video",
                    "url": "https://example.org/helping-friend-video"
                }
            ]
        }
        
        with open(self.resources_file, 'w') as f:
            json.dump(default_resources, f, indent=2)
            
        self.logger.info("Created default GBV resources file")
        
    def _load_resources(self) -> Dict[str, Any]:
        """Load GBV resources from the JSON file."""
        try:
            with open(self.resources_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading GBV resources: {e}")
            return {}
            
    def get_emergency_hotlines(self) -> List[Dict[str, Any]]:
        """Get emergency hotlines for GBV support."""
        return self.resources.get("hotlines", [])
        
    def get_safety_plans(self) -> List[Dict[str, Any]]:
        """Get safety plans for different GBV scenarios."""
        return self.resources.get("safety_plans", [])
        
    def get_safety_plan_by_id(self, plan_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific safety plan by ID."""
        for plan in self.get_safety_plans():
            if plan.get("id") == plan_id:
                return plan
        return None
        
    def get_shelters(self) -> List[Dict[str, Any]]:
        """Get shelter information for GBV survivors."""
        return self.resources.get("shelters", [])
        
    def get_legal_resources(self) -> List[Dict[str, Any]]:
        """Get legal resources for GBV survivors."""
        return self.resources.get("legal_resources", [])
        
    def get_warning_signs(self) -> List[Dict[str, Any]]:
        """Get warning signs of abusive relationships."""
        return self.resources.get("warning_signs", [])
        
    def get_educational_resources(self) -> List[Dict[str, Any]]:
        """Get educational resources about GBV."""
        return self.resources.get("educational_resources", [])
        
    def create_personalized_safety_plan(self, risk_factors: List[str]) -> Dict[str, Any]:
        """
        Create a personalized safety plan based on specific risk factors.
        
        This uses the provided risk factors to tailor a safety plan to the
        individual's specific situation.
        """
        # Start with the general safety plan steps
        general_plan = self.get_safety_plan_by_id("planning_to_leave")
        if not general_plan:
            return {"name": "Personalized Safety Plan", "steps": []}
            
        personalized_steps = general_plan.get("steps", [])[:]  # Copy the steps
        
        # Add specific steps based on risk factors
        if "children" in risk_factors:
            personalized_steps.append("Prepare children's essential items (clothes, medications, comfort items)")
            personalized_steps.append("Plan for safe childcare and school arrangements")
            
        if "pets" in risk_factors:
            personalized_steps.append("Arrange safe housing for pets (many shelters don't accept pets)")
            personalized_steps.append("Prepare pet essentials (food, medications, records)")
            
        if "firearms" in risk_factors:
            personalized_steps.append("Be especially cautious about timing of leaving")
            personalized_steps.append("Consider legal options for firearm removal")
            
        if "stalking" in risk_factors:
            personalized_steps.append("Document all stalking incidents with dates and details")
            personalized_steps.append("Vary your routes and routines frequently")
            personalized_steps.append("Check for tracking devices on vehicles and belongings")
            
        if "rural" in risk_factors:
            personalized_steps.append("Identify transportation options in advance")
            personalized_steps.append("Consider the longer response time for emergency services")
            
        if "immigration" in risk_factors:
            personalized_steps.append("Secure immigration documents in a safe place")
            personalized_steps.append("Contact immigrant-specific resources for specialized help")
            
        return {
            "name": "Personalized Safety Plan",
            "steps": personalized_steps
        }
        
    def assess_danger_level(self, answers: Dict[str, bool]) -> Dict[str, Any]:
        """
        Assess the danger level based on answers to risk assessment questions.
        
        This uses evidence-based risk factors to evaluate the potential danger
        level in a relationship.
        """
        # These are based on evidence-based risk factors for severe violence
        high_danger_factors = [
            "threatened_weapon",
            "strangled",
            "controlling",
            "jealous",
            "threatened_kill",
            "forced_sex",
            "gun_access",
            "suicide_threats",
            "unemployed",
            "child_not_theirs",
            "spying",
            "pregnant",
            "separated"
        ]
        
        # Count how many high-danger factors are present
        danger_count = sum(1 for factor in high_danger_factors if answers.get(factor, False))
        
        # Determine danger level
        if danger_count >= 7:
            level = "extreme"
            description = "Extreme danger - immediate action recommended"
            recommendations = [
                "Contact a domestic violence hotline immediately",
                "Consider emergency shelter options",
                "Create a safety plan for immediate departure",
                "Consider police involvement and legal protection"
            ]
        elif danger_count >= 4:
            level = "high"
            description = "High danger - urgent safety planning needed"
            recommendations = [
                "Contact a domestic violence advocate",
                "Create a detailed safety plan",
                "Prepare emergency essentials",
                "Consider legal protection options"
            ]
        elif danger_count >= 2:
            level = "elevated"
            description = "Elevated risk - safety planning recommended"
            recommendations = [
                "Begin safety planning",
                "Connect with support resources",
                "Document concerning incidents",
                "Be aware of escalation warning signs"
            ]
        else:
            level = "variable"
            description = "Some risk factors present - continued awareness recommended"
            recommendations = [
                "Learn about healthy relationships",
                "Stay connected with supportive people",
                "Be aware of warning signs of escalation",
                "Know local resources just in case"
            ]
            
        return {
            "level": level,
            "description": description,
            "recommendations": recommendations,
            "factor_count": danger_count,
            "total_factors": len(high_danger_factors)
        }
        
    def get_nearest_resources(self, location: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get resources nearest to the user's location.
        
        In a real implementation, this would use Azure Maps to find the
        nearest resources based on the user's location. For the hackathon,
        we're returning a subset of the available resources.
        """
        # Simulate finding nearby resources
        hotlines = self.get_emergency_hotlines()
        shelters = self.get_shelters()
        legal = self.get_legal_resources()
        
        # In a real implementation, we would filter based on location
        # For the hackathon, we're just returning a random subset
        return {
            "hotlines": hotlines[:2],
            "shelters": shelters[:1],
            "legal": legal[:1]
        }
