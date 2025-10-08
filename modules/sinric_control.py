"""
Sinric Pro IoT Control Module for AURA Assistant
Handles smart home device control via Sinric Pro platform
"""

import json
import logging
import websocket
import threading
import time
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SinricControl:
    """Handles IoT device control through Sinric Pro"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.ws = None
        self.connected = False
        self.app_key = os.getenv('SINRIC_APP_KEY')
        self.app_secret = os.getenv('SINRIC_APP_SECRET')
        
        # Device mappings (to be configured based on your devices)
        self.devices = {
            'living room light': os.getenv('SINRIC_LIGHT_ID'),
            'bedroom light': os.getenv('SINRIC_BEDROOM_LIGHT_ID'),
            'fan': os.getenv('SINRIC_FAN_ID'),
            'ac': os.getenv('SINRIC_AC_ID'),
            'tv': os.getenv('SINRIC_TV_ID')
        }
        
        if self.app_key and self.app_secret:
            self.connect()
    
    def connect(self):
        """Connect to Sinric Pro WebSocket"""
        try:
            websocket_url = f"ws://iot.sinric.pro?appkey={self.app_key}&deviceids={'&deviceids='.join(self.devices.values())}"
            
            self.ws = websocket.WebSocketApp(
                websocket_url,
                on_open=self.on_open,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close
            )
            
            # Start WebSocket in a separate thread
            ws_thread = threading.Thread(target=self.ws.run_forever)
            ws_thread.daemon = True
            ws_thread.start()
            
            self.logger.info("Connecting to Sinric Pro...")
            
        except Exception as e:
            self.logger.error(f"Failed to connect to Sinric Pro: {e}")
    
    def on_open(self, ws):
        """WebSocket connection opened"""
        self.connected = True
        self.logger.info("Connected to Sinric Pro successfully")
    
    def on_message(self, ws, message):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(message)
            self.logger.info(f"Received message: {data}")
            
            # Handle device state updates or responses
            if 'deviceId' in data and 'action' in data:
                device_name = self.get_device_name(data['deviceId'])
                if device_name:
                    self.logger.info(f"Device {device_name} state updated")
                    
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
    
    def on_error(self, ws, error):
        """Handle WebSocket errors"""
        self.logger.error(f"Sinric Pro WebSocket error: {error}")
        self.connected = False
    
    def on_close(self, ws, close_status_code, close_msg):
        """Handle WebSocket connection close"""
        self.connected = False
        self.logger.info("Sinric Pro connection closed")
    
    def get_device_name(self, device_id):
        """Get device name from device ID"""
        for name, id in self.devices.items():
            if id == device_id:
                return name
        return None
    
    def get_device_id(self, device_name):
        """Get device ID from device name"""
        device_name = device_name.lower()
        return self.devices.get(device_name)
    
    def send_command(self, device_id, action, value=None):
        """Send command to Sinric Pro device"""
        try:
            if not self.connected or not self.ws:
                self.logger.error("Not connected to Sinric Pro")
                return False
            
            # Create command payload
            payload = {
                "deviceId": device_id,
                "action": action,
                "timestamp": int(time.time()),
                "messageId": f"msg_{int(time.time())}"
            }
            
            if value is not None:
                payload["value"] = value
            
            # Send command
            message = json.dumps(payload)
            self.ws.send(message)
            
            self.logger.info(f"Command sent: {payload}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send command: {e}")
            return False
    
    def control_device(self, device_name, action):
        """Control a device (turn on/off)"""
        try:
            device_id = self.get_device_id(device_name)
            if not device_id:
                self.logger.error(f"Device '{device_name}' not found")
                return False
            
            # Map action to Sinric Pro format
            if action.lower() in ['on', 'turn on', 'enable']:
                sinric_action = "setPowerState"
                value = {"state": "On"}
            elif action.lower() in ['off', 'turn off', 'disable']:
                sinric_action = "setPowerState"
                value = {"state": "Off"}
            else:
                self.logger.error(f"Unknown action: {action}")
                return False
            
            return self.send_command(device_id, sinric_action, value)
            
        except Exception as e:
            self.logger.error(f"Device control failed: {e}")
            return False
    
    def set_device_value(self, device_name, value):
        """Set device to specific value (brightness, temperature, etc.)"""
        try:
            device_id = self.get_device_id(device_name)
            if not device_id:
                self.logger.error(f"Device '{device_name}' not found")
                return False
            
            # Determine action based on device type and value
            if 'light' in device_name.lower():
                # Set brightness
                action = "setBrightness"
                payload = {"brightness": min(100, max(0, value))}
            elif 'ac' in device_name.lower() or 'air' in device_name.lower():
                # Set temperature
                action = "setTargetTemperature"
                payload = {"temperature": {"value": value, "scale": "CELSIUS"}}
            elif 'fan' in device_name.lower():
                # Set fan speed
                action = "setRangeValue"
                payload = {"rangeValue": min(100, max(0, value))}
            else:
                # Generic range value
                action = "setRangeValue"
                payload = {"rangeValue": value}
            
            return self.send_command(device_id, action, payload)
            
        except Exception as e:
            self.logger.error(f"Set device value failed: {e}")
            return False
    
    def get_device_status(self, device_name):
        """Get current status of a device"""
        try:
            device_id = self.get_device_id(device_name)
            if not device_id:
                self.logger.error(f"Device '{device_name}' not found")
                return None
            
            # Request device status
            action = "getPowerState"
            return self.send_command(device_id, action)
            
        except Exception as e:
            self.logger.error(f"Get device status failed: {e}")
            return None
    
    def list_devices(self):
        """List all configured devices"""
        return list(self.devices.keys())
    
    def add_device(self, device_name, device_id):
        """Add a new device to the configuration"""
        try:
            self.devices[device_name.lower()] = device_id
            self.logger.info(f"Device '{device_name}' added with ID: {device_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add device: {e}")
            return False
    
    def remove_device(self, device_name):
        """Remove a device from the configuration"""
        try:
            device_name = device_name.lower()
            if device_name in self.devices:
                del self.devices[device_name]
                self.logger.info(f"Device '{device_name}' removed")
                return True
            else:
                self.logger.error(f"Device '{device_name}' not found")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to remove device: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from Sinric Pro"""
        try:
            if self.ws:
                self.ws.close()
                self.connected = False
                self.logger.info("Disconnected from Sinric Pro")
                
        except Exception as e:
            self.logger.error(f"Disconnect error: {e}")
    
    def reconnect(self):
        """Reconnect to Sinric Pro"""
        try:
            self.disconnect()
            time.sleep(2)
            self.connect()
            
        except Exception as e:
            self.logger.error(f"Reconnect failed: {e}")
    
    def is_connected(self):
        """Check if connected to Sinric Pro"""
        return self.connected