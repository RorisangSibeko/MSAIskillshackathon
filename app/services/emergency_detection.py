"""
Emergency detection service for SafeWayAI application.
This module provides functionality to detect emergencies using Azure AI services.
"""

import logging
import threading
import time
from app.services.service_manager import ServiceManager

logger = logging.getLogger(__name__)

class EmergencyDetectionService:
    """Service for detecting emergencies."""
    
    _instance = None
    
    def __new__(cls):
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super(EmergencyDetectionService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the emergency detection service."""
        if self._initialized:
            return
            
        logger.info("Initializing emergency detection service")
        
        # Get service manager
        self.service_manager = ServiceManager()
        
        # Initialize state
        self.monitoring_active = False
        self.monitoring_thread = None
        self.emergency_callbacks = []
        
        self._initialized = True
    
    def start_monitoring(self, interval_seconds=5):
        """
        Start monitoring for emergencies.
        
        Args:
            interval_seconds (int, optional): The monitoring interval in seconds
        """
        if self.monitoring_active:
            logger.warning("Emergency monitoring is already active")
            return
        
        logger.info(f"Starting emergency monitoring with interval {interval_seconds} seconds")
        
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop,
            args=(interval_seconds,)
        )
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()
    
    def stop_monitoring(self):
        """Stop monitoring for emergencies."""
        if not self.monitoring_active:
            logger.warning("Emergency monitoring is not active")
            return
        
        logger.info("Stopping emergency monitoring")
        self.monitoring_active = False
        
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=2.0)
            self.monitoring_thread = None
    
    def _monitoring_loop(self, interval_seconds):
        """
        The main monitoring loop.
        
        Args:
            interval_seconds (int): The monitoring interval in seconds
        """
        while self.monitoring_active:
            try:
                # Check for emergencies
                self._check_for_emergencies()
                
                # Sleep for the specified interval
                time.sleep(interval_seconds)
                
            except Exception as e:
                logger.error(f"Error in emergency monitoring loop: {e}")
                time.sleep(interval_seconds)
    
    def _check_for_emergencies(self):
        """Check for emergencies using various methods."""
        # This would integrate with various sensors and AI services
        # For now, we'll just log that we're checking
        logger.debug("Checking for emergencies")
        
        # In a real implementation, this would:
        # 1. Check audio for emergency keywords
        # 2. Analyze camera feeds for emergency situations
        # 3. Monitor IoT sensors for unusual readings
        # 4. Check for panic button activations
        # 5. Monitor location for entry into high-risk areas
    
    def register_emergency_callback(self, callback):
        """
        Register a callback for emergency notifications.
        
        Args:
            callback (callable): The callback function
        """
        self.emergency_callbacks.append(callback)
        logger.info(f"Registered emergency callback, total callbacks: {len(self.emergency_callbacks)}")
    
    def unregister_emergency_callback(self, callback):
        """
        Unregister a callback for emergency notifications.
        
        Args:
            callback (callable): The callback function
        """
        if callback in self.emergency_callbacks:
            self.emergency_callbacks.remove(callback)
            logger.info(f"Unregistered emergency callback, remaining callbacks: {len(self.emergency_callbacks)}")
    
    def _notify_emergency(self, emergency_data):
        """
        Notify all registered callbacks of an emergency.
        
        Args:
            emergency_data (dict): The emergency data
        """
        logger.info(f"Notifying {len(self.emergency_callbacks)} callbacks of emergency: {emergency_data}")
        
        for callback in self.emergency_callbacks:
            try:
                callback(emergency_data)
            except Exception as e:
                logger.error(f"Error in emergency callback: {e}")
    
    def detect_emergency_from_audio(self, audio_file=None):
        """
        Detect emergency from audio.
        
        Args:
            audio_file (str, optional): Path to the audio file
            
        Returns:
            dict: Emergency detection results
        """
        try:
            # Use the AI service to detect emergency from audio
            result = self.service_manager.ai_service.detect_emergency_from_audio(audio_file)
            
            # If emergency detected, notify callbacks
            if result.get("emergency_detected", False):
                self._notify_emergency({
                    "type": "audio_emergency",
                    "confidence": result.get("confidence", 0),
                    "details": result
                })
            
            return result
            
        except Exception as e:
            logger.error(f"Error detecting emergency from audio: {e}")
            return {
                "emergency_detected": False,
                "confidence": 0,
                "message": f"Error: {str(e)}"
            }
    
    def detect_emergency_from_image(self, image_path=None, image_url=None):
        """
        Detect emergency from image.
        
        Args:
            image_path (str, optional): Path to the image file
            image_url (str, optional): URL of the image
            
        Returns:
            dict: Emergency detection results
        """
        try:
            # Use the AI service to detect emergency from image
            result = self.service_manager.ai_service.detect_emergency_from_image(
                image_path=image_path,
                image_url=image_url
            )
            
            # If emergency detected, notify callbacks
            if result.get("emergency_detected", False):
                self._notify_emergency({
                    "type": "image_emergency",
                    "confidence": result.get("confidence", 0),
                    "details": result
                })
            
            return result
            
        except Exception as e:
            logger.error(f"Error detecting emergency from image: {e}")
            return {
                "emergency_detected": False,
                "confidence": 0,
                "message": f"Error: {str(e)}"
            }
    
    def report_emergency(self, emergency_data):
        """
        Report an emergency manually.
        
        Args:
            emergency_data (dict): The emergency data
            
        Returns:
            dict: The result of reporting the emergency
        """
        try:
            # Ensure required fields
            if "type" not in emergency_data:
                emergency_data["type"] = "manual_emergency"
            
            if "timestamp" not in emergency_data:
                emergency_data["timestamp"] = time.time()
            
            # Notify callbacks
            self._notify_emergency(emergency_data)
            
            # Report to IoT Hub if connected
            if hasattr(self.service_manager, 'iot_service') and self.service_manager.iot_service:
                self.service_manager.iot_service.send_emergency_alert(emergency_data)
            
            # Report to Azure Functions
            if hasattr(self.service_manager, 'functions_service') and self.service_manager.functions_service:
                result = self.service_manager.functions_service.process_emergency_alert(emergency_data)
                return result
            
            return {"status": "reported", "message": "Emergency reported successfully"}
            
        except Exception as e:
            logger.error(f"Error reporting emergency: {e}")
            return {"error": str(e)}
