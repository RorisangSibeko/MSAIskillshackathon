"""
Azure IoT Hub service for SafeWayAI application.
This module provides functionality to interact with Azure IoT Hub.
"""

import logging
import json
import time
import threading
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse
from app.config.azure_config import IOT_HUB_CONFIG

logger = logging.getLogger(__name__)

class AzureIoTService:
    """Service for interacting with Azure IoT Hub."""
    
    def __init__(self):
        """Initialize the Azure IoT Hub service."""
        self.connection_string = IOT_HUB_CONFIG["connection_string"]
        self.device_id = IOT_HUB_CONFIG["device_id"]
        self.client = None
        self.connected = False
        self.message_callbacks = {}
        self.method_callbacks = {}
        
        # Start the connection in a separate thread to avoid blocking
        self._connect_thread = threading.Thread(target=self._connect)
        self._connect_thread.daemon = True
        self._connect_thread.start()
        
        logger.info("Azure IoT Hub service initialized")
    
    def _connect(self):
        """Connect to Azure IoT Hub."""
        try:
            # Create the client
            self.client = IoTHubDeviceClient.create_from_connection_string(
                self.connection_string
            )
            
            # Set up message received handler
            self.client.on_message_received = self._on_message_received
            
            # Set up method request handler
            self.client.on_method_request_received = self._on_method_request_received
            
            # Connect to the hub
            self.client.connect()
            self.connected = True
            
            logger.info("Connected to Azure IoT Hub")
            
        except Exception as e:
            logger.error(f"Error connecting to Azure IoT Hub: {e}")
            self.connected = False
    
    def _on_message_received(self, message):
        """
        Handle messages received from IoT Hub.
        
        Args:
            message: The received message
        """
        try:
            # Parse the message
            message_text = message.data.decode('utf-8')
            message_data = json.loads(message_text)
            
            logger.info(f"Message received: {message_data}")
            
            # Check if there's a callback for this message type
            message_type = message_data.get("type", "unknown")
            if message_type in self.message_callbacks:
                # Call the registered callback
                self.message_callbacks[message_type](message_data)
            else:
                logger.warning(f"No callback registered for message type: {message_type}")
                
        except Exception as e:
            logger.error(f"Error processing received message: {e}")
    
    def _on_method_request_received(self, method_request):
        """
        Handle method requests received from IoT Hub.
        
        Args:
            method_request: The received method request
        """
        try:
            # Get the method name
            method_name = method_request.name
            logger.info(f"Method request received: {method_name}")
            
            # Check if there's a callback for this method
            if method_name in self.method_callbacks:
                # Call the registered callback
                result = self.method_callbacks[method_name](method_request.payload)
                
                # Send the response
                response = MethodResponse.create_from_method_request(
                    method_request, 200, json.dumps(result)
                )
                self.client.send_method_response(response)
            else:
                logger.warning(f"No callback registered for method: {method_name}")
                
                # Send error response
                response = MethodResponse.create_from_method_request(
                    method_request, 404, json.dumps({"error": "Method not found"})
                )
                self.client.send_method_response(response)
                
        except Exception as e:
            logger.error(f"Error processing method request: {e}")
            
            # Send error response
            response = MethodResponse.create_from_method_request(
                method_request, 500, json.dumps({"error": str(e)})
            )
            self.client.send_method_response(response)
    
    def send_telemetry(self, data):
        """
        Send telemetry data to IoT Hub.
        
        Args:
            data (dict): The telemetry data
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        try:
            if not self.connected:
                logger.warning("Cannot send telemetry: not connected to IoT Hub")
                return False
            
            # Create the message
            message = Message(json.dumps(data))
            
            # Add properties
            message.content_type = "application/json"
            message.content_encoding = "utf-8"
            
            # Add custom properties
            if "type" in data:
                message.custom_properties["type"] = data["type"]
            
            # Send the message
            self.client.send_message(message)
            logger.info(f"Telemetry sent: {data}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error sending telemetry to IoT Hub: {e}")
            return False
    
    def register_message_callback(self, message_type, callback):
        """
        Register a callback for a specific message type.
        
        Args:
            message_type (str): The message type
            callback (callable): The callback function
        """
        self.message_callbacks[message_type] = callback
        logger.info(f"Registered callback for message type: {message_type}")
    
    def register_method_callback(self, method_name, callback):
        """
        Register a callback for a specific method.
        
        Args:
            method_name (str): The method name
            callback (callable): The callback function
        """
        self.method_callbacks[method_name] = callback
        logger.info(f"Registered callback for method: {method_name}")
    
    def send_emergency_alert(self, alert_data):
        """
        Send an emergency alert to IoT Hub.
        
        Args:
            alert_data (dict): The alert data
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        try:
            # Ensure required fields
            if "type" not in alert_data:
                alert_data["type"] = "emergency_alert"
            
            # Add timestamp if not present
            if "timestamp" not in alert_data:
                alert_data["timestamp"] = time.time()
            
            # Send as telemetry
            return self.send_telemetry(alert_data)
            
        except Exception as e:
            logger.error(f"Error sending emergency alert to IoT Hub: {e}")
            return False
    
    def send_location_update(self, latitude, longitude, accuracy=None):
        """
        Send a location update to IoT Hub.
        
        Args:
            latitude (float): The latitude
            longitude (float): The longitude
            accuracy (float, optional): The accuracy in meters
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        try:
            # Create the location data
            location_data = {
                "type": "location_update",
                "latitude": latitude,
                "longitude": longitude,
                "timestamp": time.time()
            }
            
            # Add accuracy if provided
            if accuracy is not None:
                location_data["accuracy"] = accuracy
            
            # Send as telemetry
            return self.send_telemetry(location_data)
            
        except Exception as e:
            logger.error(f"Error sending location update to IoT Hub: {e}")
            return False
    
    def send_device_status(self, status_data):
        """
        Send device status to IoT Hub.
        
        Args:
            status_data (dict): The status data
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        try:
            # Ensure required fields
            if "type" not in status_data:
                status_data["type"] = "device_status"
            
            # Add timestamp if not present
            if "timestamp" not in status_data:
                status_data["timestamp"] = time.time()
            
            # Send as telemetry
            return self.send_telemetry(status_data)
            
        except Exception as e:
            logger.error(f"Error sending device status to IoT Hub: {e}")
            return False
    
    def close(self):
        """Close the connection to IoT Hub."""
        try:
            if self.client:
                self.client.disconnect()
                self.connected = False
                logger.info("Disconnected from Azure IoT Hub")
                
        except Exception as e:
            logger.error(f"Error disconnecting from Azure IoT Hub: {e}")
            
    def __del__(self):
        """Destructor to ensure the connection is closed."""
        self.close()
