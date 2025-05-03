import time
import random
import threading
import logging
from typing import Callable, List, Dict, Any, Optional
from datetime import datetime

class PanicDetector:
    """
    Service for detecting emergency situations using AI.
    
    In a real implementation, this would connect to Azure Cognitive Services
    for computer vision, audio analysis, and other AI capabilities.
    For the hackathon, we're simulating these capabilities.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.monitoring = False
        self.monitor_thread = None
        self.callbacks = []
        self.emergency_types = [
            "physical_assault", 
            "fire", 
            "medical_emergency",
            "suspicious_activity",
            "domestic_violence",
            "break_in",
            "weapon_detected"
        ]
        self.last_detection_time = None
        self.detection_threshold = 0.75  # Confidence threshold
        self.detection_interval = 5  # Seconds between checks
        self.sensitivity = 0.1  # Base chance of detection (for simulation)
        
    def start_monitoring(self):
        """Start the emergency monitoring process."""
        if self.monitoring:
            return
            
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitoring_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        self.logger.info("Emergency monitoring started")
        
    def stop_monitoring(self):
        """Stop the emergency monitoring process."""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1.0)
            self.monitor_thread = None
        self.logger.info("Emergency monitoring stopped")
        
    def _monitoring_loop(self):
        """Main monitoring loop that runs in a separate thread."""
        while self.monitoring:
            try:
                # In a real implementation, this would analyze camera feeds,
                # audio, and other sensors using Azure Cognitive Services
                self._check_for_emergencies()
                time.sleep(self.detection_interval)
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(1)  # Prevent tight loop on error
                
    def _check_for_emergencies(self):
        """
        Check for emergency situations.
        
        In a real implementation, this would use Azure Computer Vision,
        Custom Vision, and other AI services to analyze inputs.
        """
        # Simulate emergency detection for the hackathon
        if random.random() < self.sensitivity:
            emergency_type = random.choice(self.emergency_types)
            confidence = random.uniform(0.6, 0.99)
            
            if confidence >= self.detection_threshold:
                self._trigger_emergency(emergency_type, confidence)
                
    def _trigger_emergency(self, emergency_type: str, confidence: float):
        """Trigger an emergency alert."""
        self.last_detection_time = datetime.now()
        
        emergency_data = {
            "type": emergency_type,
            "confidence": confidence,
            "timestamp": self.last_detection_time.isoformat(),
            "location": "Current Location",  # Would be real location in production
            "details": self._get_emergency_details(emergency_type)
        }
        
        # Notify all registered callbacks
        for callback in self.callbacks:
            try:
                callback(emergency_data)
            except Exception as e:
                self.logger.error(f"Error in emergency callback: {e}")
                
    def _get_emergency_details(self, emergency_type: str) -> Dict[str, Any]:
        """Get detailed information about the emergency type."""
        details = {
            "physical_assault": {
                "description": "Physical assault detected",
                "severity": "high",
                "recommended_action": "Contact police immediately",
                "ai_confidence": "high"
            },
            "fire": {
                "description": "Fire or smoke detected",
                "severity": "high",
                "recommended_action": "Evacuate and call fire department",
                "ai_confidence": "high"
            },
            "medical_emergency": {
                "description": "Person in distress detected",
                "severity": "high",
                "recommended_action": "Call emergency medical services",
                "ai_confidence": "medium"
            },
            "suspicious_activity": {
                "description": "Unusual behavior detected",
                "severity": "medium",
                "recommended_action": "Increase vigilance and verify",
                "ai_confidence": "medium"
            },
            "domestic_violence": {
                "description": "Potential domestic violence situation",
                "severity": "high",
                "recommended_action": "Contact authorities immediately",
                "ai_confidence": "medium"
            },
            "break_in": {
                "description": "Unauthorized entry detected",
                "severity": "high",
                "recommended_action": "Contact police and stay safe",
                "ai_confidence": "high"
            },
            "weapon_detected": {
                "description": "Potential weapon detected",
                "severity": "high",
                "recommended_action": "Evacuate area and contact police",
                "ai_confidence": "medium"
            }
        }
        
        return details.get(emergency_type, {
            "description": "Unknown emergency",
            "severity": "unknown",
            "recommended_action": "Use caution and assess situation",
            "ai_confidence": "low"
        })
        
    def register_callback(self, callback: Callable[[Dict[str, Any]], None]):
        """Register a callback to be notified of emergencies."""
        if callback not in self.callbacks:
            self.callbacks.append(callback)
            
    def unregister_callback(self, callback: Callable[[Dict[str, Any]], None]):
        """Unregister a previously registered callback."""
        if callback in self.callbacks:
            self.callbacks.remove(callback)
            
    def set_sensitivity(self, sensitivity: float):
        """Set the detection sensitivity (0.0 to 1.0)."""
        self.sensitivity = max(0.0, min(1.0, sensitivity))
        
    def set_detection_interval(self, interval: int):
        """Set the interval between detection checks in seconds."""
        self.detection_interval = max(1, interval)
        
    def manually_report_emergency(self, emergency_type: str, details: Optional[Dict[str, Any]] = None):
        """Manually report an emergency situation."""
        if emergency_type not in self.emergency_types:
            emergency_type = "suspicious_activity"  # Default
            
        self._trigger_emergency(emergency_type, 1.0)  # Manual reports have 100% confidence
        self.logger.info(f"Manual emergency report: {emergency_type}")
        
    def get_last_detection_time(self) -> Optional[datetime]:
        """Get the timestamp of the last detected emergency."""
        return self.last_detection_time
