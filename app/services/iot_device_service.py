"""
IoT device service for SafeWayAI application.
This module provides functionality to manage IoT devices.
"""

import logging
import json
import time
import threading
from app.services.service_manager import ServiceManager

logger = logging.getLogger(__name__)

class IoTDeviceService:
    """Service for managing IoT devices."""
    
    _instance = None
    
    def __new__(cls):
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super(IoTDeviceService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the IoT device service."""
        if self._initialized:
            return
            
        logger.info("Initializing IoT device service")
        
        # Get service manager
        self.service_manager = ServiceManager()
        
        # Initialize state
        self.connected_devices = {}
        self.device_status_callbacks = []
        
        # Register callbacks for IoT Hub messages
        if hasattr(self.service_manager, 'iot_service') and self.service_manager.iot_service:
            self.service_manager.iot_service.register_message_callback(
                "device_status", self._handle_device_status
            )
            self.service_manager.iot_service.register_message_callback(
                "device_alert", self._handle_device_alert
            )
            
            # Register method callbacks
            self.service_manager.iot_service.register_method_callback(
                "GetDeviceStatus", self._handle_get_device_status
            )
            self.service_manager.iot_service.register_method_callback(
                "ControlDevice", self._handle_control_device
            )
        
        self._initialized = True
    
    def _handle_device_status(self, message_data):
        """
        Handle device status messages from IoT Hub.
        
        Args:
            message_data (dict): The message data
        """
        try:
            logger.info(f"Received device status: {message_data}")
            
            # Extract device ID
            device_id = message_data.get("device_id")
            if not device_id:
                logger.warning("Device status message missing device_id")
                return
            
            # Update device status
            self.connected_devices[device_id] = {
                "status": message_data.get("status", "unknown"),
                "last_updated": time.time(),
                "details": message_data
            }
            
            # Notify callbacks
            for callback in self.device_status_callbacks:
                try:
                    callback(device_id, self.connected_devices[device_id])
                except Exception as e:
                    logger.error(f"Error in device status callback: {e}")
            
        except Exception as e:
            logger.error(f"Error handling device status message: {e}")
    
    def _handle_device_alert(self, message_data):
        """
        Handle device alert messages from IoT Hub.
        
        Args:
            message_data (dict): The message data
        """
        try:
            logger.info(f"Received device alert: {message_data}")
            
            # Extract device ID
            device_id = message_data.get("device_id")
            if not device_id:
                logger.warning("Device alert message missing device_id")
                return
            
            # Update device status
            if device_id in self.connected_devices:
                self.connected_devices[device_id]["last_alert"] = message_data
                self.connected_devices[device_id]["last_updated"] = time.time()
            
            # Process the alert
            alert_type = message_data.get("alert_type")
            
            if alert_type == "intrusion":
                # Handle intrusion alert
                self._handle_intrusion_alert(message_data)
            elif alert_type == "smoke":
                # Handle smoke alert
                self._handle_smoke_alert(message_data)
            elif alert_type == "motion":
                # Handle motion alert
                self._handle_motion_alert(message_data)
            else:
                logger.warning(f"Unknown alert type: {alert_type}")
            
        except Exception as e:
            logger.error(f"Error handling device alert message: {e}")
    
    def _handle_intrusion_alert(self, alert_data):
        """
        Handle an intrusion alert.
        
        Args:
            alert_data (dict): The alert data
        """
        try:
            logger.info(f"Processing intrusion alert: {alert_data}")
            
            # In a real implementation, this would:
            # 1. Notify security personnel
            # 2. Trigger cameras to record
            # 3. Sound alarms
            # 4. Log the incident
            
            # For now, we'll just create an incident
            if hasattr(self.service_manager, 'incident_service'):
                incident_data = {
                    "type": "incident",
                    "incident_type": "intrusion",
                    "severity": 8,  # High severity
                    "status": "active",
                    "location": {
                        "latitude": alert_data.get("latitude"),
                        "longitude": alert_data.get("longitude")
                    },
                    "device_id": alert_data.get("device_id"),
                    "description": f"Intrusion detected by {alert_data.get('device_name', 'unknown device')}",
                    "timestamp": time.time()
                }
                
                self.service_manager.incident_service.report_incident(incident_data)
            
        except Exception as e:
            logger.error(f"Error handling intrusion alert: {e}")
    
    def _handle_smoke_alert(self, alert_data):
        """
        Handle a smoke alert.
        
        Args:
            alert_data (dict): The alert data
        """
        try:
            logger.info(f"Processing smoke alert: {alert_data}")
            
            # In a real implementation, this would:
            # 1. Notify fire department
            # 2. Trigger evacuation procedures
            # 3. Activate sprinklers
            # 4. Log the incident
            
            # For now, we'll just create an incident
            if hasattr(self.service_manager, 'incident_service'):
                incident_data = {
                    "type": "incident",
                    "incident_type": "fire",
                    "severity": 9,  # Very high severity
                    "status": "active",
                    "location": {
                        "latitude": alert_data.get("latitude"),
                        "longitude": alert_data.get("longitude")
                    },
                    "device_id": alert_data.get("device_id"),
                    "description": f"Smoke detected by {alert_data.get('device_name', 'unknown device')}",
                    "timestamp": time.time()
                }
                
                self.service_manager.incident_service.report_incident(incident_data)
            
        except Exception as e:
            logger.error(f"Error handling smoke alert: {e}")
    
    def _handle_motion_alert(self, alert_data):
        """
        Handle a motion alert.
        
        Args:
            alert_data (dict): The alert data
        """
        try:
            logger.info(f"Processing motion alert: {alert_data}")
            
            # In a real implementation, this would:
            # 1. Check if motion is expected
            # 2. Trigger cameras to record
            # 3. Notify if suspicious
            # 4. Log the event
            
            # For now, we'll just log it
            logger.info(f"Motion detected by {alert_data.get('device_name', 'unknown device')}")
            
        except Exception as e:
            logger.error(f"Error handling motion alert: {e}")
    
    def _handle_get_device_status(self, payload):
        """
        Handle a GetDeviceStatus method request.
        
        Args:
            payload (dict): The method payload
            
        Returns:
            dict: The response
        """
        try:
            logger.info(f"Handling GetDeviceStatus method: {payload}")
            
            # Extract device ID
            device_id = payload.get("device_id")
            
            if device_id:
                # Return status for specific device
                if device_id in self.connected_devices:
                    return {
                        "device_id": device_id,
                        "status": self.connected_devices[device_id]
                    }
                else:
                    return {
                        "device_id": device_id,
                        "status": "unknown",
                        "message": "Device not found"
                    }
            else:
                # Return status for all devices
                return {
                    "devices": self.connected_devices
                }
            
        except Exception as e:
            logger.error(f"Error handling GetDeviceStatus method: {e}")
            return {"error": str(e)}
    
    def _handle_control_device(self, payload):
        """
        Handle a ControlDevice method request.
        
        Args:
            payload (dict): The method payload
            
        Returns:
            dict: The response
        """
        try:
            logger.info(f"Handling ControlDevice method: {payload}")
            
            # Extract parameters
            device_id = payload.get("device_id")
            command = payload.get("command")
            
            if not device_id or not command:
                return {
                    "success": False,
                    "message": "Missing device_id or command"
                }
            
            # Check if device exists
            if device_id not in self.connected_devices:
                return {
                    "success": False,
                    "message": f"Device {device_id} not found"
                }
            
            # Process the command
            if command == "arm":
                # Arm the device
                return self._arm_device(device_id, payload.get("parameters", {}))
            elif command == "disarm":
                # Disarm the device
                return self._disarm_device(device_id, payload.get("parameters", {}))
            elif command == "restart":
                # Restart the device
                return self._restart_device(device_id)
            else:
                return {
                    "success": False,
                    "message": f"Unknown command: {command}"
                }
            
        except Exception as e:
            logger.error(f"Error handling ControlDevice method: {e}")
            return {"error": str(e)}
    
    def _arm_device(self, device_id, parameters):
        """
        Arm a device.
        
        Args:
            device_id (str): The device ID
            parameters (dict): Command parameters
            
        Returns:
            dict: The response
        """
        try:
            logger.info(f"Arming device {device_id} with parameters {parameters}")
            
            # In a real implementation, this would send a command to the device
            # For now, we'll just update the status
            if device_id in self.connected_devices:
                self.connected_devices[device_id]["status"] = "armed"
                self.connected_devices[device_id]["last_updated"] = time.time()
                
                # Send a message to the device via IoT Hub
                if hasattr(self.service_manager, 'iot_service') and self.service_manager.iot_service:
                    self.service_manager.iot_service.send_telemetry({
                        "type": "device_command",
                        "device_id": device_id,
                        "command": "arm",
                        "parameters": parameters,
                        "timestamp": time.time()
                    })
                
                return {
                    "success": True,
                    "message": f"Device {device_id} armed successfully"
                }
            else:
                return {
                    "success": False,
                    "message": f"Device {device_id} not found"
                }
            
        except Exception as e:
            logger.error(f"Error arming device {device_id}: {e}")
            return {"error": str(e)}
    
    def _disarm_device(self, device_id, parameters):
        """
        Disarm a device.
        
        Args:
            device_id (str): The device ID
            parameters (dict): Command parameters
            
        Returns:
            dict: The response
        """
        try:
            logger.info(f"Disarming device {device_id} with parameters {parameters}")
            
            # In a real implementation, this would send a command to the device
            # For now, we'll just update the status
            if device_id in self.connected_devices:
                self.connected_devices[device_id]["status"] = "disarmed"
                self.connected_devices[device_id]["last_updated"] = time.time()
                
                # Send a message to the device via IoT Hub
                if hasattr(self.service_manager, 'iot_service') and self.service_manager.iot_service:
                    self.service_manager.iot_service.send_telemetry({
                        "type": "device_command",
                        "device_id": device_id,
                        "command": "disarm",
                        "parameters": parameters,
                        "timestamp": time.time()
                    })
                
                return {
                    "success": True,
                    "message": f"Device {device_id} disarmed successfully"
                }
            else:
                return {
                    "success": False,
                    "message": f"Device {device_id} not found"
                }
            
        except Exception as e:
            logger.error(f"Error disarming device {device_id}: {e}")
            return {"error": str(e)}
    
    def _restart_device(self, device_id):
        """
        Restart a device.
        
        Args:
            device_id (str): The device ID
            
        Returns:
            dict: The response
        """
        try:
            logger.info(f"Restarting device {device_id}")
            
            # In a real implementation, this would send a command to the device
            # For now, we'll just update the status
            if device_id in self.connected_devices:
                self.connected_devices[device_id]["status"] = "restarting"
                self.connected_devices[device_id]["last_updated"] = time.time()
                
                # Send a message to the device via IoT Hub
                if hasattr(self.service_manager, 'iot_service') and self.service_manager.iot_service:
                    self.service_manager.iot_service.send_telemetry({
                        "type": "device_command",
                        "device_id": device_id,
                        "command": "restart",
                        "timestamp": time.time()
                    })
                
                return {
                    "success": True,
                    "message": f"Device {device_id} restart initiated"
                }
            else:
                return {
                    "success": False,
                    "message": f"Device {device_id} not found"
                }
            
        except Exception as e:
            logger.error(f"Error restarting device {device_id}: {e}")
            return {"error": str(e)}
    
    def register_device_status_callback(self, callback):
        """
        Register a callback for device status updates.
        
        Args:
            callback (callable): The callback function
        """
        self.device_status_callbacks.append(callback)
        logger.info(f"Registered device status callback, total callbacks: {len(self.device_status_callbacks)}")
    
    def unregister_device_status_callback(self, callback):
        """
        Unregister a callback for device status updates.
        
        Args:
            callback (callable): The callback function
        """
        if callback in self.device_status_callbacks:
            self.device_status_callbacks.remove(callback)
            logger.info(f"Unregistered device status callback, remaining callbacks: {len(self.device_status_callbacks)}")
    
    def get_connected_devices(self):
        """
        Get all connected devices.
        
        Returns:
            dict: The connected devices
        """
        return self.connected_devices
    
    def get_device_status(self, device_id):
        """
        Get the status of a specific device.
        
        Args:
            device_id (str): The device ID
            
        Returns:
            dict: The device status
        """
        if device_id in self.connected_devices:
            return self.connected_devices[device_id]
        else:
            return {
                "status": "unknown",
                "message": f"Device {device_id} not found"
            }
    
    def arm_device(self, device_id, parameters=None):
        """
        Arm a device.
        
        Args:
            device_id (str): The device ID
            parameters (dict, optional): Command parameters
            
        Returns:
            dict: The response
        """
        if parameters is None:
            parameters = {}
        
        return self._arm_device(device_id, parameters)
    
    def disarm_device(self, device_id, parameters=None):
        """
        Disarm a device.
        
        Args:
            device_id (str): The device ID
            parameters (dict, optional): Command parameters
            
        Returns:
            dict: The response
        """
        if parameters is None:
            parameters = {}
        
        return self._disarm_device(device_id, parameters)
    
    def restart_device(self, device_id):
        """
        Restart a device.
        
        Args:
            device_id (str): The device ID
            
        Returns:
            dict: The response
        """
        return self._restart_device(device_id)
