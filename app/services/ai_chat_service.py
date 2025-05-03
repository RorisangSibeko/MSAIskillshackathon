"""
AI Chat Service for SafeWayAI application.
This module provides functionality for an AI-powered community chat system.
"""

import logging
import json
import time
import os
import random
from datetime import datetime
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class AIChatService:
    """Service for AI-powered community chat functionality."""

    def __init__(self, service_manager=None):
        """Initialize the AI Chat service."""
        self.service_manager = service_manager
        self.chat_history = []
        self.community_reports = []
        self.alert_keywords = [
            "emergency", "help", "danger", "crime", "suspicious", "attack",
            "robbery", "assault", "weapon", "gun", "knife", "fire", "accident",
            "injured", "bleeding", "unsafe", "threat", "following", "scared"
        ]
        self.safety_keywords = [
            "safe", "route", "directions", "navigate", "path", "way", "road",
            "street", "area", "neighborhood", "location", "place", "destination"
        ]

        # Load existing chat data if available
        self._load_data()

        logger.info("AI Chat service initialized")

    def _load_data(self):
        """Load existing chat data from storage."""
        try:
            # Check for chat history file
            chat_file = os.path.join("data", "chat_history.json")
            if os.path.exists(chat_file):
                with open(chat_file, 'r') as f:
                    self.chat_history = json.load(f)
                logger.info(f"Loaded {len(self.chat_history)} chat messages")

            # Check for community reports file
            reports_file = os.path.join("data", "community_reports.json")
            if os.path.exists(reports_file):
                with open(reports_file, 'r') as f:
                    self.community_reports = json.load(f)
                logger.info(f"Loaded {len(self.community_reports)} community reports")

            # If no data was loaded, generate some sample data
            if not self.chat_history:
                self._generate_sample_data()

        except Exception as e:
            logger.error(f"Error loading chat data: {e}")
            # Generate sample data as fallback
            self._generate_sample_data()

    def _save_data(self):
        """Save chat data to storage."""
        try:
            # Create data directory if it doesn't exist
            os.makedirs("data", exist_ok=True)

            # Save chat history
            with open(os.path.join("data", "chat_history.json"), 'w') as f:
                json.dump(self.chat_history, f, indent=2)

            # Save community reports
            with open(os.path.join("data", "community_reports.json"), 'w') as f:
                json.dump(self.community_reports, f, indent=2)

            logger.info("Chat data saved successfully")

        except Exception as e:
            logger.error(f"Error saving chat data: {e}")

    def _generate_sample_data(self):
        """Generate sample chat data for demonstration."""
        logger.info("Generating sample chat data")

        # Generate sample chat history
        self.chat_history = [
            {
                "id": "msg_1",
                "sender": "system",
                "content": "Welcome to SafeWayAI Community Chat! I'm here to help keep you and your community safe. You can report incidents, ask for safety advice, or check on the safety status of different areas.",
                "timestamp": self._get_past_timestamp(days=2, hours=3),
                "is_alert": False
            },
            {
                "id": "msg_2",
                "sender": "user",
                "content": "Hi there! Is this area safe to walk through at night?",
                "timestamp": self._get_past_timestamp(days=2, hours=2),
                "is_alert": False
            },
            {
                "id": "msg_3",
                "sender": "ai",
                "content": "Based on community reports and safety data, the area around your current location has moderate safety concerns after dark. I recommend using well-lit main roads and avoiding shortcuts through less populated areas. Would you like me to suggest a safer route?",
                "timestamp": self._get_past_timestamp(days=2, hours=2),
                "is_alert": False
            },
            {
                "id": "msg_4",
                "sender": "user",
                "content": "Yes, please suggest a safer route.",
                "timestamp": self._get_past_timestamp(days=2, hours=2),
                "is_alert": False
            },
            {
                "id": "msg_5",
                "sender": "ai",
                "content": "I've analyzed the area and found a safer route that takes approximately 3 minutes longer but has better lighting and more foot traffic. I've sent the route to your navigation screen. Would you like me to notify a trusted contact that you're on your way?",
                "timestamp": self._get_past_timestamp(days=2, hours=2),
                "is_alert": False
            },
            {
                "id": "msg_6",
                "sender": "user",
                "content": "No thanks, I'll be fine with the safer route.",
                "timestamp": self._get_past_timestamp(days=2, hours=1),
                "is_alert": False
            },
            {
                "id": "msg_7",
                "sender": "ai",
                "content": "Understood. Stay safe and feel free to check in with me during your journey if you need anything else. I'm here to help 24/7.",
                "timestamp": self._get_past_timestamp(days=2, hours=1),
                "is_alert": False
            },
            {
                "id": "msg_8",
                "sender": "user",
                "content": "I just saw someone suspicious hanging around the ATM on Main Street. They seem to be watching people withdraw money.",
                "timestamp": self._get_past_timestamp(days=1, hours=5),
                "is_alert": True
            },
            {
                "id": "msg_9",
                "sender": "ai",
                "content": "Thank you for reporting this. I've logged this as a safety alert and notified community moderators. Can you provide any more details about the person or the exact location?",
                "timestamp": self._get_past_timestamp(days=1, hours=5),
                "is_alert": True
            },
            {
                "id": "msg_10",
                "sender": "system",
                "content": "⚠️ ALERT: This report has been logged and shared with local authorities. Other community members in the area have been notified to exercise caution near ATMs on Main Street.",
                "timestamp": self._get_past_timestamp(days=1, hours=5),
                "is_alert": True
            }
        ]

        # Generate sample community reports
        self.community_reports = [
            {
                "id": "report_1",
                "type": "suspicious_activity",
                "description": "Suspicious person watching ATM users on Main Street",
                "location": {
                    "latitude": -26.1052,
                    "longitude": 28.0560,
                    "address": "Main Street, Sandton"
                },
                "timestamp": self._get_past_timestamp(days=1, hours=5),
                "severity": "medium",
                "status": "verified",
                "source": "community_chat"
            },
            {
                "id": "report_2",
                "type": "infrastructure",
                "description": "Street lights not working on Park Avenue",
                "location": {
                    "latitude": -26.1070,
                    "longitude": 28.0567,
                    "address": "Park Avenue, Sandton"
                },
                "timestamp": self._get_past_timestamp(days=3, hours=8),
                "severity": "low",
                "status": "pending",
                "source": "community_chat"
            },
            {
                "id": "report_3",
                "type": "crime",
                "description": "Smartphone theft reported at Central Mall",
                "location": {
                    "latitude": -26.1045,
                    "longitude": 28.0577,
                    "address": "Central Mall, Sandton"
                },
                "timestamp": self._get_past_timestamp(days=2, hours=14),
                "severity": "medium",
                "status": "verified",
                "source": "community_chat"
            }
        ]

        # Save the sample data
        self._save_data()

    def _get_past_timestamp(self, days=0, hours=0, minutes=0):
        """Generate a timestamp in the past."""
        now = datetime.now()
        delta = days * 86400 + hours * 3600 + minutes * 60
        past_time = now.timestamp() - delta
        return datetime.fromtimestamp(past_time).isoformat()

    def get_chat_history(self, limit=50):
        """
        Get recent chat history.

        Args:
            limit (int): Maximum number of messages to return

        Returns:
            list: Recent chat messages
        """
        # Sort by timestamp and return the most recent messages
        sorted_history = sorted(self.chat_history, key=lambda x: x["timestamp"], reverse=True)
        return sorted_history[:limit]

    def send_message(self, message_content, user_location=None, is_emergency=False):
        """
        Send a message to the AI chat.

        Args:
            message_content (str): The message content
            user_location (dict, optional): User's location coordinates
            is_emergency (bool): Whether this is an emergency message

        Returns:
            dict: The AI response message
        """
        try:
            logger.info(f"Received message: '{message_content}', is_emergency: {is_emergency}, has_location: {user_location is not None}")

            # Create user message
            user_message = {
                "id": f"msg_{int(time.time())}",
                "sender": "user",
                "content": message_content,
                "timestamp": datetime.now().isoformat(),
                "is_alert": is_emergency,
                "location": user_location
            }

            # Add to chat history
            self.chat_history.append(user_message)
            logger.info(f"Added user message to chat history: {user_message['id']}")

            # Check if this is an alert/report
            is_alert = is_emergency or self._check_for_alert_keywords(message_content)
            logger.info(f"Message is_alert: {is_alert} (emergency: {is_emergency}, keywords: {self._check_for_alert_keywords(message_content)})")

            # Generate AI response
            ai_response = self._generate_ai_response(message_content, user_location, is_alert)
            logger.info(f"Generated AI response: {ai_response['id']}, content: '{ai_response['content'][:50]}...'")

            # Add AI response to chat history
            self.chat_history.append(ai_response)
            logger.info(f"Added AI response to chat history: {ai_response['id']}")

            # If this is an alert, process it
            if is_alert:
                logger.info(f"Processing alert for message: {user_message['id']}")
                self._process_alert(message_content, user_location, ai_response)

            # Check if this is a safety route question
            if self._check_for_safety_keywords(message_content):
                logger.info(f"Processing safety query for message: {user_message['id']}")
                self._process_safety_query(message_content, user_location)

            # Save updated chat history
            self._save_data()
            logger.info(f"Saved chat data with {len(self.chat_history)} messages")

            return ai_response

        except Exception as e:
            logger.error(f"Error sending message: {e}")

            # Create error response
            error_response = {
                "id": f"msg_error_{int(time.time())}",
                "sender": "ai",
                "content": "I'm sorry, I encountered an error processing your message. Please try again.",
                "timestamp": datetime.now().isoformat(),
                "is_alert": False
            }

            # Add error response to chat history
            self.chat_history.append(error_response)

            return error_response

    def _check_for_alert_keywords(self, message):
        """Check if the message contains alert keywords."""
        message_lower = message.lower()
        for keyword in self.alert_keywords:
            if keyword in message_lower:
                return True
        return False

    def _check_for_safety_keywords(self, message):
        """Check if the message is asking about safe routes."""
        message_lower = message.lower()
        for keyword in self.safety_keywords:
            if keyword in message_lower:
                return True
        return False

    def _generate_ai_response(self, message, user_location, is_alert):
        """
        Generate an AI response to the user message using Azure OpenAI.

        Args:
            message (str): The user's message
            user_location (dict): The user's location data
            is_alert (bool): Whether this is an alert message

        Returns:
            dict: The AI response message
        """
        # Create response ID
        response_id = f"msg_{int(time.time())}"

        try:
            # Try to use Azure OpenAI if available
            if self.service_manager and hasattr(self.service_manager, 'ai_safety_service'):
                # Get recent chat context (last 5 messages)
                recent_messages = sorted(self.chat_history[-5:], key=lambda x: x["timestamp"])
                chat_context = "\n".join([f"{msg['sender']}: {msg['content']}" for msg in recent_messages])

                # Get community context
                community_context = self._get_community_context(user_location)

                # Create prompt for Azure OpenAI
                prompt = f"""
                You are SafeWayAI, an AI safety assistant for South Africa. Your purpose is to help keep people safe by providing safety information, processing incident reports, and offering guidance.

                CURRENT CONTEXT:
                {community_context}

                RECENT CONVERSATION:
                {chat_context}

                USER QUERY:
                {message}

                USER LOCATION:
                {user_location if user_location else 'Unknown'}

                ALERT STATUS:
                {'This appears to be an emergency or safety alert.' if is_alert else 'This is a regular query.'}

                Please respond in a helpful, concise manner. If this is an emergency, acknowledge it and provide appropriate guidance. If it's about safety routes, provide specific safety recommendations. Focus on being practical and supportive.
                """

                # Call Azure OpenAI through the AI safety service
                ai_service_response = self.service_manager.ai_safety_service.get_safety_response(prompt)

                # Extract the content from the response
                if ai_service_response and "content" in ai_service_response:
                    content = ai_service_response["content"]
                else:
                    # Fallback to template responses if Azure call fails
                    if is_alert:
                        content = self._generate_alert_response(message)
                    elif self._check_for_safety_keywords(message):
                        content = self._generate_safety_response(message, user_location)
                    else:
                        content = self._generate_general_response(message)
            else:
                # Fallback to template responses if no AI service is available
                if is_alert:
                    content = self._generate_alert_response(message)
                elif self._check_for_safety_keywords(message):
                    content = self._generate_safety_response(message, user_location)
                else:
                    content = self._generate_general_response(message)
        except Exception as e:
            logger.error(f"Error generating AI response: {e}")
            # Fallback to template responses
            if is_alert:
                content = self._generate_alert_response(message)
            elif self._check_for_safety_keywords(message):
                content = self._generate_safety_response(message, user_location)
            else:
                content = self._generate_general_response(message)

        # Create response object
        response = {
            "id": response_id,
            "sender": "ai",
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "is_alert": is_alert
        }

        return response

    def _get_community_context(self, user_location):
        """
        Get relevant community context based on user location.

        Args:
            user_location (dict): The user's location data

        Returns:
            str: Context information about the area
        """
        # If we don't have location data, return general context
        if not user_location:
            return "No specific location data available. Providing general safety information."

        # Find reports near the user's location
        nearby_reports = []
        if user_location and "latitude" in user_location and "longitude" in user_location:
            for report in self.community_reports:
                if "location" in report and "latitude" in report["location"] and "longitude" in report["location"]:
                    # Calculate rough distance (this is a simplified calculation)
                    lat_diff = abs(user_location["latitude"] - report["location"]["latitude"])
                    lon_diff = abs(user_location["longitude"] - report["location"]["longitude"])

                    # If within approximately 2km (very rough estimate)
                    if lat_diff < 0.02 and lon_diff < 0.02:
                        nearby_reports.append(report)

        # If no nearby reports, return general context
        if not nearby_reports:
            return f"Location: {user_location.get('address', 'Unknown')}. No recent safety reports in this immediate area."

        # Create context from nearby reports
        context_parts = [f"Location: {user_location.get('address', 'Unknown')}. Recent safety reports in this area:"]

        for i, report in enumerate(nearby_reports[:3]):  # Limit to 3 most recent reports
            report_type = report.get("type", "incident").replace("_", " ").title()
            severity = report.get("severity", "medium").title()
            context_parts.append(f"{i+1}. {report_type} ({severity}): {report.get('description', 'No description')} at {report['location'].get('address', 'nearby location')}.")

        return "\n".join(context_parts)

    def _generate_alert_response(self, message):
        """Generate a response to an alert message."""
        templates = [
            "Thank you for reporting this. I've logged this as a safety alert and notified community moderators. Can you provide any more details about the incident?",
            "I've recorded this safety concern and alerted local authorities. Your report helps keep the community safe. Is there anything else you can tell me about what happened?",
            "This has been logged as a safety alert. Community members in the area will be notified. Can you share any additional information that might help authorities respond?",
            "I've registered this incident and notified relevant safety personnel. Any additional details you can provide would be helpful for the response team.",
            "Thank you for bringing this to attention. I've created a safety alert based on your report. Can you confirm your current location so we can direct assistance properly?"
        ]
        return random.choice(templates)

    def _generate_safety_response(self, message, user_location):
        """Generate a response to a safety query."""
        templates = [
            "I've analyzed the safety data for this area. Based on community reports and historical data, this location has a moderate safety rating. Would you like me to suggest a safer route?",
            "According to our safety database, this area has had some reported incidents in the past month. I recommend staying on well-lit main roads. Would you like me to show you the safest path?",
            "The safety score for this location is currently 65/100. There are some concerns about walking here after dark. I can suggest alternative routes if you'd like.",
            "This area has a good safety rating during daylight hours, but exercise caution after sunset. Would you like me to check if there are any recent reports from community members?",
            "Based on community feedback, this route has some sections with safety concerns. I can suggest a slightly longer but safer alternative if you prefer."
        ]
        return random.choice(templates)

    def _generate_general_response(self, message):
        """Generate a response to a general message."""
        templates = [
            "I'm here to help keep you safe. You can ask me about safe routes, report incidents, or get safety tips for specific areas.",
            "How can I assist you with your safety today? I can provide information about safe routes, emergency contacts, or help you report safety concerns.",
            "I'm your AI safety assistant. I can help with finding safe routes, reporting incidents, or connecting you with emergency services if needed.",
            "Is there a specific safety concern I can help you with? I'm here to provide guidance and support for your community safety needs.",
            "Thank you for reaching out. I'm constantly learning from community reports to provide better safety information. How can I assist you today?"
        ]
        return random.choice(templates)

    def _process_alert(self, message, user_location, ai_response):
        """
        Process an alert message.

        This creates a community report, notifies authorities if needed,
        and sends alerts to nearby community members.
        """
        try:
            # Create report ID
            report_id = f"report_{int(time.time())}"

            # Determine report type based on content
            report_type = self._determine_report_type(message)

            # Create the report
            report = {
                "id": report_id,
                "type": report_type,
                "description": message,
                "location": user_location or {"latitude": 0, "longitude": 0, "address": "Unknown location"},
                "timestamp": datetime.now().isoformat(),
                "severity": self._determine_severity(message),
                "status": "pending",
                "source": "community_chat"
            }

            # Add to community reports
            self.community_reports.append(report)

            # Create system alert message
            system_alert = {
                "id": f"msg_alert_{int(time.time())}",
                "sender": "system",
                "content": f"⚠️ ALERT: This report has been logged and shared with local authorities. Other community members in the area have been notified to exercise caution.",
                "timestamp": datetime.now().isoformat(),
                "is_alert": True
            }

            # Add system alert to chat history
            self.chat_history.append(system_alert)

            # Notify authorities if available
            if self.service_manager and hasattr(self.service_manager, 'incident_service'):
                self.service_manager.incident_service.report_incident({
                    "incident_type": report_type,
                    "description": message,
                    "location": user_location,
                    "severity": report["severity"],
                    "source": "community_chat"
                })

            # Send notification to nearby users if available
            if self.service_manager and hasattr(self.service_manager, 'notification_service'):
                self.service_manager.notification_service.send_notification(
                    title="Community Safety Alert",
                    message=f"Safety concern reported near your area: {self._get_short_description(message)}",
                    level="warning",
                    data={"report_id": report_id}
                )

            # Update safety data for route calculations if available
            if self.service_manager and hasattr(self.service_manager, 'safety_prediction_service'):
                # This would update the safety model with new data
                pass

            # Save updated data
            self._save_data()

            logger.info(f"Processed alert: {report_id}")

        except Exception as e:
            logger.error(f"Error processing alert: {e}")

    def _process_safety_query(self, message, user_location):
        """
        Process a safety route query.

        This would integrate with the route finding service to suggest
        safer routes based on community reports and safety data.
        """
        try:
            # In a real implementation, this would extract destination info
            # and call the route finding service

            # For now, we'll just log the query
            logger.info(f"Safety route query: {message}")

            # If we have a route service, we could call it here
            if self.service_manager and hasattr(self.service_manager, 'route_service'):
                # This would call the route service to get safety information
                pass

        except Exception as e:
            logger.error(f"Error processing safety query: {e}")

    def _determine_report_type(self, message):
        """Determine the type of report based on message content."""
        message_lower = message.lower()

        if any(word in message_lower for word in ["robbery", "theft", "stolen", "break-in", "burglary"]):
            return "theft"
        elif any(word in message_lower for word in ["assault", "attack", "violence", "fight", "weapon"]):
            return "assault"
        elif any(word in message_lower for word in ["suspicious", "lurking", "watching", "following"]):
            return "suspicious_activity"
        elif any(word in message_lower for word in ["light", "dark", "lighting", "streetlight"]):
            return "infrastructure"
        else:
            return "other"

    def _determine_severity(self, message):
        """Determine the severity of a report based on message content."""
        message_lower = message.lower()

        # High severity keywords
        high_severity = ["emergency", "weapon", "gun", "knife", "attack", "blood", "injured", "hurt"]
        if any(word in message_lower for word in high_severity):
            return "high"

        # Medium severity keywords
        medium_severity = ["suspicious", "following", "scared", "unsafe", "theft", "stolen"]
        if any(word in message_lower for word in medium_severity):
            return "medium"

        # Default to low severity
        return "low"

    def _get_short_description(self, message, max_length=50):
        """Get a short description of a message for notifications."""
        if len(message) <= max_length:
            return message

        # Truncate and add ellipsis
        return message[:max_length-3] + "..."
