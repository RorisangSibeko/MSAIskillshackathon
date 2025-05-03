import os
import json
import logging
import threading
import time
import random
from typing import Dict, List, Any, Optional, Callable
from pathlib import Path

class IoTService:
    """
    Service for managing IoT device integrations.
    
    This service handles connections to smart home devices, security systems,
    and other IoT devices for enhanced safety monitoring and response.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.devices_file = Path("app/data/iot_devices.json")
        self.connected_devices = {}
        self.device_callbacks = {}
        self.monitoring = False
        self.monitor_thread = None
        
        # Ensure the data directory exists
        self.devices_file.parent.mkdir(exist_ok=True)
        
        # Load or create devices file
        if not self.devices_file.exists():
            self._create_default_devices()
            
        # Load devices
        self.available_devices = self._load_devices()
        
    def _create_default_devices(self):
        """Create default IoT devices for demonstration."""
        default_devices = {
            "supported_devices": [
                {
                    "id": "smart_camera_1",
                    "name": "Smart Security Camera",
                    "type": "camera",
                    "manufacturer": "SafeCam",
                    "capabilities": ["video", "motion", "audio"],
                    "connection_types": ["wifi", "bluetooth"],
                    "description": "Indoor/outdoor security camera with motion detection"
                },
                {
                    "id": "smart_lock_1",
                    "name": "Smart Door Lock",
                    "type": "lock",
                    "manufacturer": "SecureLock",
                    "capabilities": ["lock", "unlock", "status"],
                    "connection_types": ["wifi", "zigbee"],
                    "description": "Smart door lock with remote control and status monitoring"
                },
                {
                    "id": "panic_button_1",
                    "name": "Wearable Panic Button",
                    "type": "panic_button",
                    "manufacturer": "SafeWear",
                    "capabilities": ["alert", "location"],
                    "connection_types": ["bluetooth", "cellular"],
                    "description": "Wearable panic button with GPS location tracking"
                },
                {
                    "id": "alarm_system_1",
                    "name": "Home Security System",
                    "type": "alarm",
                    "manufacturer": "SecureHome",
                    "capabilities": ["arm", "disarm", "alert", "zones"],
                    "connection_types": ["wifi", "cellular"],
                    "description": "Complete home security system with multiple sensors"
                },
                {
                    "id": "smoke_detector_1",
                    "name": "Smart Smoke Detector",
                    "type": "sensor",
                    "manufacturer": "SafeSense",
                    "capabilities": ["smoke", "co", "temperature"],
                    "connection_types": ["wifi", "zigbee"],
                    "description": "Smart smoke and carbon monoxide detector"
                },
                {
                    "id": "motion_sensor_1",
                    "name": "Motion Sensor",
                    "type": "sensor",
                    "manufacturer": "SafeSense",
                    "capabilities": ["motion", "temperature", "light"],
                    "connection_types": ["wifi", "zigbee"],
                    "description": "Multi-function motion sensor for security monitoring"
                },
                {
                    "id": "smart_speaker_1",
                    "name": "Smart Speaker",
                    "type": "speaker",
                    "manufacturer": "EchoTech",
                    "capabilities": ["voice", "audio", "assistant"],
                    "connection_types": ["wifi", "bluetooth"],
                    "description": "Smart speaker with voice assistant for emergency commands"
                },
                {
                    "id": "medical_alert_1",
                    "name": "Medical Alert Pendant",
                    "type": "medical",
                    "manufacturer": "MediSafe",
                    "capabilities": ["alert", "fall_detection", "location"],
                    "connection_types": ["cellular", "bluetooth"],
                    "description": "Medical alert pendant with fall detection"
                }
            ],
            "supported_systems": [
                {
                    "id": "adt_security",
                    "name": "ADT Security",
                    "type": "security_system",
                    "integration_level": "full",
                    "capabilities": ["arm", "disarm", "alerts", "sensors", "cameras"]
                },
                {
                    "id": "ring_security",
                    "name": "Ring Security",
                    "type": "security_system",
                    "integration_level": "full",
                    "capabilities": ["arm", "disarm", "alerts", "sensors", "cameras"]
                },
                {
                    "id": "simplisafe",
                    "name": "SimpliSafe",
                    "type": "security_system",
                    "integration_level": "partial",
                    "capabilities": ["alerts", "status"]
                },
                {
                    "id": "nest_secure",
                    "name": "Nest Secure",
                    "type": "security_system",
                    "integration_level": "full",
                    "capabilities": ["arm", "disarm", "alerts", "sensors", "cameras"]
                },
                {
                    "id": "honeywell_security",
                    "name": "Honeywell Security",
                    "type": "security_system",
                    "integration_level": "partial",
                    "capabilities": ["alerts", "status"]
                }
            ],
            "insurance_integrations": [
                {
                    "id": "state_farm",
                    "name": "State Farm",
                    "discount_available": True,
                    "discount_percentage": 10,
                    "requirements": ["security_system", "smoke_detector"]
                },
                {
                    "id": "allstate",
                    "name": "Allstate",
                    "discount_available": True,
                    "discount_percentage": 15,
                    "requirements": ["security_system", "smart_locks", "cameras"]
                },
                {
                    "id": "geico",
                    "name": "GEICO",
                    "discount_available": True,
                    "discount_percentage": 5,
                    "requirements": ["security_system"]
                },
                {
                    "id": "liberty_mutual",
                    "name": "Liberty Mutual",
                    "discount_available": True,
                    "discount_percentage": 12,
                    "requirements": ["security_system", "smoke_detector", "water_sensor"]
                }
            ]
        }
        
        with open(self.devices_file, 'w') as f:
            json.dump(default_devices, f, indent=2)
            
        self.logger.info("Created default IoT devices file")
        
    def _load_devices(self) -> Dict[str, Any]:
        """Load IoT device information from the JSON file."""
        try:
            with open(self.devices_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading IoT devices: {e}")
            return {"supported_devices": [], "supported_systems": [], "insurance_integrations": []}
            
    def get_supported_devices(self) -> List[Dict[str, Any]]:
        """Get all supported IoT devices."""
        return self.available_devices.get("supported_devices", [])
        
    def get_supported_systems(self) -> List[Dict[str, Any]]:
        """Get all supported security systems."""
        return self.available_devices.get("supported_systems", [])
        
    def get_insurance_integrations(self) -> List[Dict[str, Any]]:
        """Get all supported insurance integrations."""
        return self.available_devices.get("insurance_integrations", [])
        
    def connect_device(self, device_id: str) -> bool:
        """
        Connect to an IoT device.
        
        In a real implementation, this would use the appropriate protocol
        to connect to the physical device. For the hackathon, we're simulating
        the connection.
        """
        # Find the device in the supported devices list
        device = None
        for d in self.get_supported_devices():
            if d["id"] == device_id:
                device = d
                break
                
        if not device:
            self.logger.error(f"Device not found: {device_id}")
            return False
            
        # Simulate connection
        self.connected_devices[device_id] = {
            **device,
            "connected": True,
            "status": "online",
            "last_updated": time.time(),
            "battery": random.randint(60, 100) if "battery" in device.get("capabilities", []) else None
        }
        
        self.logger.info(f"Connected to device: {device_id}")
        return True
        
    def disconnect_device(self, device_id: str) -> bool:
        """Disconnect from an IoT device."""
        if device_id in self.connected_devices:
            del self.connected_devices[device_id]
            self.logger.info(f"Disconnected from device: {device_id}")
            return True
        return False
        
    def get_connected_devices(self) -> Dict[str, Dict[str, Any]]:
        """Get all currently connected devices."""
        return self.connected_devices
        
    def get_device_status(self, device_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of a connected device."""
        return self.connected_devices.get(device_id)
        
    def send_command(self, device_id: str, command: str, params: Optional[Dict[str, Any]] = None) -> bool:
        """
        Send a command to a connected device.
        
        In a real implementation, this would send the command to the physical
        device using the appropriate protocol. For the hackathon, we're simulating
        the command.
        """
        if device_id not in self.connected_devices:
            self.logger.error(f"Device not connected: {device_id}")
            return False
            
        device = self.connected_devices[device_id]
        device_type = device.get("type")
        capabilities = device.get("capabilities", [])
        
        # Check if the command is supported by the device
        if command not in capabilities and command not in ["status", "refresh"]:
            self.logger.error(f"Command not supported by device: {command}")
            return False
            
        # Simulate command execution
        if command == "lock" and device_type == "lock":
            self.logger.info(f"Locking device: {device_id}")
            self.connected_devices[device_id]["status"] = "locked"
        elif command == "unlock" and device_type == "lock":
            self.logger.info(f"Unlocking device: {device_id}")
            self.connected_devices[device_id]["status"] = "unlocked"
        elif command == "arm" and device_type == "alarm":
            mode = params.get("mode", "away") if params else "away"
            self.logger.info(f"Arming alarm system: {device_id}, mode: {mode}")
            self.connected_devices[device_id]["status"] = f"armed_{mode}"
        elif command == "disarm" and device_type == "alarm":
            self.logger.info(f"Disarming alarm system: {device_id}")
            self.connected_devices[device_id]["status"] = "disarmed"
        elif command == "alert" and "alert" in capabilities:
            self.logger.info(f"Triggering alert on device: {device_id}")
            self.connected_devices[device_id]["status"] = "alert"
            # In a real implementation, this would trigger the device's alert function
        elif command == "status" or command == "refresh":
            self.logger.info(f"Refreshing device status: {device_id}")
            self.connected_devices[device_id]["last_updated"] = time.time()
            
        # Update the device's last updated timestamp
        self.connected_devices[device_id]["last_updated"] = time.time()
        
        return True
        
    def start_monitoring(self):
        """Start monitoring connected IoT devices."""
        if self.monitoring:
            return
            
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitoring_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        self.logger.info("IoT device monitoring started")
        
    def stop_monitoring(self):
        """Stop monitoring connected IoT devices."""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1.0)
            self.monitor_thread = None
        self.logger.info("IoT device monitoring stopped")
        
    def _monitoring_loop(self):
        """Main monitoring loop for IoT devices."""
        while self.monitoring:
            try:
                # In a real implementation, this would poll the devices for updates
                # For the hackathon, we're simulating device updates
                self._simulate_device_updates()
                time.sleep(5)  # Poll every 5 seconds
            except Exception as e:
                self.logger.error(f"Error in IoT monitoring loop: {e}")
                time.sleep(1)  # Prevent tight loop on error
                
    def _simulate_device_updates(self):
        """Simulate updates from connected IoT devices."""
        for device_id, device in list(self.connected_devices.items()):
            # Simulate random events from devices
            device_type = device.get("type")
            capabilities = device.get("capabilities", [])
            
            # Update last_updated timestamp
            self.connected_devices[device_id]["last_updated"] = time.time()
            
            # Simulate battery drain for battery-powered devices
            if "battery" in capabilities and device.get("battery") is not None:
                battery = device.get("battery", 100)
                # Small random battery drain
                battery = max(0, battery - random.uniform(0, 0.1))
                self.connected_devices[device_id]["battery"] = battery
                
            # Simulate random events (very low probability)
            if random.random() < 0.01:  # 1% chance per check
                if device_type == "camera" and "motion" in capabilities:
                    # Simulate motion detection
                    self._trigger_device_event(device_id, "motion_detected", {
                        "confidence": random.uniform(0.7, 0.95),
                        "zone": "front_door"
                    })
                elif device_type == "sensor" and "motion" in capabilities:
                    # Simulate motion detection
                    self._trigger_device_event(device_id, "motion_detected", {
                        "confidence": random.uniform(0.8, 0.99)
                    })
                elif device_type == "sensor" and "smoke" in capabilities:
                    # Very rare smoke detection (0.1% chance)
                    if random.random() < 0.1:
                        self._trigger_device_event(device_id, "smoke_detected", {
                            "level": random.uniform(0.1, 0.3)
                        })
                elif device_type == "medical" and "fall_detection" in capabilities:
                    # Very rare fall detection (0.1% chance)
                    if random.random() < 0.1:
                        self._trigger_device_event(device_id, "fall_detected", {
                            "confidence": random.uniform(0.7, 0.95)
                        })
                        
    def _trigger_device_event(self, device_id: str, event_type: str, data: Dict[str, Any]):
        """Trigger an event from a device and notify callbacks."""
        self.logger.info(f"Device event: {device_id} - {event_type}")
        
        # Create event data
        event_data = {
            "device_id": device_id,
            "device_name": self.connected_devices[device_id].get("name"),
            "device_type": self.connected_devices[device_id].get("type"),
            "event_type": event_type,
            "timestamp": time.time(),
            "data": data
        }
        
        # Notify callbacks for this device
        if device_id in self.device_callbacks:
            for callback in self.device_callbacks[device_id]:
                try:
                    callback(event_data)
                except Exception as e:
                    self.logger.error(f"Error in device callback: {e}")
                    
        # Notify callbacks for all devices
        if "all" in self.device_callbacks:
            for callback in self.device_callbacks["all"]:
                try:
                    callback(event_data)
                except Exception as e:
                    self.logger.error(f"Error in device callback: {e}")
                    
    def register_callback(self, callback: Callable[[Dict[str, Any]], None], device_id: str = "all"):
        """Register a callback for device events."""
        if device_id not in self.device_callbacks:
            self.device_callbacks[device_id] = []
            
        if callback not in self.device_callbacks[device_id]:
            self.device_callbacks[device_id].append(callback)
            
    def unregister_callback(self, callback: Callable[[Dict[str, Any]], None], device_id: str = "all"):
        """Unregister a previously registered callback."""
        if device_id in self.device_callbacks and callback in self.device_callbacks[device_id]:
            self.device_callbacks[device_id].remove(callback)
            
    def get_insurance_discount(self, insurance_id: str, connected_devices: List[str]) -> Optional[float]:
        """
        Calculate the insurance discount based on connected devices.
        
        This simulates the integration with insurance companies to provide
        discounts for users with security and safety devices.
        """
        insurance = None
        for ins in self.get_insurance_integrations():
            if ins["id"] == insurance_id:
                insurance = ins
                break
                
        if not insurance or not insurance.get("discount_available"):
            return None
            
        # Check if the user has the required devices
        requirements = insurance.get("requirements", [])
        device_types = [self.connected_devices[d].get("type") for d in connected_devices if d in self.connected_devices]
        
        # Check if all requirements are met
        requirements_met = all(req in device_types for req in requirements)
        
        if requirements_met:
            return insurance.get("discount_percentage", 0)
        else:
            return 0
