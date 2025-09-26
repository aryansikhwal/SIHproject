#!/usr/bin/env python3
"""
ESP32 BLE Connection Test
Direct Bluetooth Low Energy connection to ESP32
"""

import asyncio
from bleak import BleakScanner, BleakClient
import logging
import time
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ESP32 Configuration
ESP32_CONFIG = {
    'device_name': 'ESP32',  # Common ESP32 BLE name
    'service_uuid': '12345678-1234-1234-1234-1234567890ab',
    'characteristic_uuid': 'abcd1234-5678-90ab-cdef-1234567890ab',
    'scan_timeout': 10.0,
    'connection_timeout': 10.0
}

class ESP32BLEConnector:
    def __init__(self):
        self.client = None
        self.device_address = None
        self.connected = False
        
    async def scan_for_esp32(self):
        """Scan for ESP32 devices"""
        try:
            logger.info("🔍 Scanning for ESP32 BLE devices...")
            
            # Scan for devices
            devices = await BleakScanner.discover(timeout=ESP32_CONFIG['scan_timeout'])
            
            logger.info(f"📡 Found {len(devices)} BLE devices:")
            
            esp32_devices = []
            for device in devices:
                device_info = f"  📱 {device.address}"
                if device.name:
                    device_info += f" - {device.name}"
                else:
                    device_info += " - (Unknown Name)"
                
                # Get RSSI from metadata if available
                try:
                    rssi = device.metadata.get('rssi', None) if hasattr(device, 'metadata') else None
                    if rssi:
                        device_info += f" (RSSI: {rssi})"
                except:
                    pass
                    
                logger.info(device_info)
                
                # Check if this could be an ESP32
                if device.name and ('ESP32' in device.name.upper() or 'ESP' in device.name.upper()):
                    esp32_devices.append(device)
                    logger.info(f"✅ Potential ESP32 found: {device.name} ({device.address})")
                elif device.name and ('ATTENSYNC' in device.name.upper() or 'RFID' in device.name.upper()):
                    esp32_devices.append(device)
                    logger.info(f"✅ Potential AttenSync device found: {device.name} ({device.address})")
                
                # Also check devices without names (ESP32 might not broadcast name)
                elif not device.name:
                    esp32_devices.append(device)
                    logger.info(f"🤔 Unnamed device (might be ESP32): {device.address}")
            
            if esp32_devices:
                # Try the first potential ESP32 device
                selected_device = esp32_devices[0]
                logger.info(f"🎯 Selected device: {selected_device.address}")
                return selected_device.address
            else:
                logger.warning("⚠️ No ESP32 devices found. Will try first available device...")
                # If no obvious ESP32, try the first device
                if devices:
                    return devices[0].address
                
            return None
            
        except Exception as e:
            logger.error(f"❌ Scan error: {e}")
            return None

    async def connect_to_device(self, address):
        """Connect to ESP32 device"""
        try:
            logger.info(f"🔌 Connecting to device: {address}")
            
            self.client = BleakClient(address, timeout=ESP32_CONFIG['connection_timeout'])
            
            # Try to connect
            await self.client.connect()
            
            if self.client.is_connected:
                self.connected = True
                self.device_address = address
                logger.info(f"✅ Connected to device: {address}")
                
                # Get device info
                try:
                    device_name = await self.client.read_gatt_char("00002a00-0000-1000-8000-00805f9b34fb")  # Device Name
                    logger.info(f"📱 Device name: {device_name.decode('utf-8')}")
                except:
                    logger.info("📱 Device name: Not available")
                
                # List all services
                services = self.client.services
                logger.info(f"🔧 Available services ({len(services)}):")
                
                for service in services:
                    logger.info(f"   Service: {service.uuid}")
                    for char in service.characteristics:
                        logger.info(f"     Characteristic: {char.uuid} - {char.properties}")
                
                return True
            else:
                logger.error("❌ Failed to establish connection")
                return False
                
        except Exception as e:
            logger.error(f"❌ Connection error: {e}")
            return False

    async def test_rfid_communication(self):
        """Test communication with ESP32 RFID system"""
        if not self.connected or not self.client:
            logger.error("❌ Not connected to device")
            return False
            
        try:
            logger.info("🏷️ Testing RFID communication...")
            
            # Try to find RFID service/characteristic
            services = self.client.services
            
            # Look for our custom service or standard services
            target_chars = []
            for service in services:
                for char in service.characteristics:
                    if 'notify' in char.properties or 'read' in char.properties:
                        target_chars.append(char)
            
            if target_chars:
                # Try to read from the first available characteristic
                test_char = target_chars[0]
                logger.info(f"📡 Testing characteristic: {test_char.uuid}")
                
                if 'notify' in test_char.properties:
                    # Set up notification handler
                    def notification_handler(sender, data):
                        logger.info(f"📨 Received data: {data}")
                        try:
                            decoded = data.decode('utf-8')
                            logger.info(f"📄 Decoded: {decoded}")
                            if 'RFID:' in decoded:
                                logger.info("🏷️ RFID data detected!")
                        except:
                            logger.info(f"📊 Raw bytes: {data.hex()}")
                    
                    await self.client.start_notify(test_char.uuid, notification_handler)
                    logger.info("✅ Notification handler set up. Waiting for RFID scans...")
                    
                    # Wait for data
                    await asyncio.sleep(30)  # Wait 30 seconds for RFID scans
                    
                    await self.client.stop_notify(test_char.uuid)
                    
                elif 'read' in test_char.properties:
                    # Try to read data
                    data = await self.client.read_gatt_char(test_char.uuid)
                    logger.info(f"📨 Read data: {data}")
                    
            return True
            
        except Exception as e:
            logger.error(f"❌ Communication test failed: {e}")
            return False

    async def disconnect(self):
        """Disconnect from device"""
        if self.client and self.connected:
            try:
                await self.client.disconnect()
                logger.info("👋 Disconnected from device")
            except Exception as e:
                logger.error(f"❌ Disconnect error: {e}")
        
        self.connected = False
        self.client = None
        self.device_address = None

async def main():
    """Main connection test"""
    connector = ESP32BLEConnector()
    
    try:
        logger.info("🚀 Starting ESP32 BLE Connection Test...")
        logger.info("=" * 50)
        
        # Step 1: Scan for devices
        device_address = await connector.scan_for_esp32()
        
        if not device_address:
            logger.error("❌ No ESP32 device found")
            return
        
        # Step 2: Connect to device
        connected = await connector.connect_to_device(device_address)
        
        if not connected:
            logger.error("❌ Failed to connect to ESP32")
            return
        
        # Step 3: Test RFID communication
        await connector.test_rfid_communication()
        
        logger.info("✅ ESP32 BLE connection test completed!")
        
    except KeyboardInterrupt:
        logger.info("⏹️ Test interrupted by user")
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
    finally:
        # Cleanup
        await connector.disconnect()
        logger.info("🏁 Test finished")

if __name__ == "__main__":
    # Run the connection test
    asyncio.run(main())