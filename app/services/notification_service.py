import logging
import time
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime

class NotificationService:
    """
    Service for managing notifications and alerts.
    
    This service handles sending notifications to users, emergency contacts,
    and authorities.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.notification_callbacks = []
        
    def send_notification(self, title: str, message: str, level: str = "info", data: Optional[Dict[str, Any]] = None) -> bool:
        """
        Send a notification to the user.
        
        In a real implementation, this would use push notifications or SMS.
        For the hackathon, we're simulating notifications.
        """
        notification = {
            "title": title,
            "message": message,
            "level": level,
            "timestamp": datetime.now().isoformat(),
            "data": data or {}
        }
        
        # Log the notification
        self.logger.info(f"Notification: {title} - {message}")
        
        # Notify callbacks
        for callback in self.notification_callbacks:
            try:
                callback(notification)
            except Exception as e:
                self.logger.error(f"Error in notification callback: {e}")
                
        return True
        
    def send_emergency_alert(self, emergency_type: str, details: Dict[str, Any]) -> bool:
        """
        Send an emergency alert to the user, emergency contacts, and authorities.
        
        In a real implementation, this would use push notifications, SMS, and
        potentially direct communication with emergency services. For the
        hackathon, we're simulating alerts.
        """
        # Create alert data
        alert = {
            "type": emergency_type,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        
        # Log the alert
        self.logger.info(f"Emergency alert: {emergency_type}")
        
        # Send notification to user
        self.send_notification(
            title="EMERGENCY ALERT",
            message=f"{emergency_type.replace('_', ' ').title()} detected",
            level="emergency",
            data=alert
        )
        
        # In a real implementation, this would also:
        # 1. Send SMS/calls to emergency contacts
        # 2. Contact authorities if configured
        # 3. Trigger IoT device actions (e.g., alarm, lights)
        
        return True
        
    def send_to_emergency_contacts(self, message: str, user_location: Optional[Dict[str, float]] = None) -> bool:
        """
        Send a message to all emergency contacts.
        
        In a real implementation, this would send SMS or calls to the
        user's emergency contacts. For the hackathon, we're simulating
        this functionality.
        """
        # Log the action
        self.logger.info(f"Sending to emergency contacts: {message}")
        
        # In a real implementation, this would iterate through the user's
        # emergency contacts and send messages to each one
        
        return True
        
    def register_notification_callback(self, callback: Callable[[Dict[str, Any]], None]):
        """Register a callback to be notified of new notifications."""
        if callback not in self.notification_callbacks:
            self.notification_callbacks.append(callback)
            
    def unregister_notification_callback(self, callback: Callable[[Dict[str, Any]], None]):
        """Unregister a previously registered callback."""
        if callback in self.notification_callbacks:
            self.notification_callbacks.remove(callback)
