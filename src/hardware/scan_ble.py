import asyncio
from bleak import BleakScanner
import time
import logging
import platform
import asyncio.exceptions
import winreg
import re

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

def get_paired_devices():
    paired_devices = []
    try:
        bluetooth_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\BTHPORT\Parameters\Devices")
        i = 0
        while True:
            try:
                # Get device MAC from registry
                device_mac = winreg.EnumKey(bluetooth_key, i)
                device_key = winreg.OpenKey(bluetooth_key, device_mac)
                
                # Get device name if available
                try:
                    name = winreg.QueryValueEx(device_key, "Name")[0]
                except FileNotFoundError:
                    name = "Unknown Device"
                
                # Format MAC address
                mac = ':'.join(re.findall('..', device_mac))
                paired_devices.append((name, mac.upper()))
                i += 1
            except WindowsError:
                break
    except WindowsError as e:
        print(f"Error accessing registry: {e}")
    return paired_devices

class BLEDeviceMonitor:
    def __init__(self):
        self.target_name = "ESP32"  # The name you see in Windows Bluetooth settings
        self.esp32_found = False
        self.running = True
        self.all_devices = set()  # Track all discovered devices
        
        # Get the operating system
        self.os = platform.system()
        # Windows-specific scanner settings
        self.detection_timeout = 5.0
        if self.os == "Windows":
            self.detection_timeout = 10.0  # Longer timeout for Windows
            
        # Get paired devices first
        print("\nChecking paired devices first...")
        paired_devices = get_paired_devices()
        for name, mac in paired_devices:
            print(f"Paired Device: {name} ({mac})")
            decoded_name = name.decode('utf-8').strip('\x00') if isinstance(name, bytes) else name
            if "esp" in decoded_name.lower():
                print("\n🎯 FOUND PAIRED ESP32!")
                print(f"Name: {decoded_name}")
                print(f"Address: {mac}")
                print("\nYou can use this address in the RFID listener.")
                self.esp32_found = True

    async def scan_loop(self):
        print(f"Starting BLE scan, looking for device named '{self.target_name}'")
        print("Will check both paired and unpaired devices")
        print("Press Ctrl+C to stop scanning\n")
        
        while self.running:
            try:
                print("Scanning...")
                # Create scanner with system-specific settings
                scanner = BleakScanner()
                
                # Start scanning and get discovered devices
                devices = await scanner.discover(timeout=self.detection_timeout)
                
                # Process discovered devices
                for device in devices:
                    name = device.name or ""
                    address = device.address
                    
                    # Create a unique key for this device
                    device_key = f"{address}:{name}"
                    
                    if device_key not in self.all_devices:
                        self.all_devices.add(device_key)
                        print(f"\nNew Device Found:")
                        print(f"Name: {name}")
                        print(f"Address: {address}")
                        print(f"RSSI: {device.rssi}dBm")
                        print("-" * 40)
                    
                    # Check if this is our ESP32
                    if name and self.target_name.lower() in name.lower():
                        if not self.esp32_found:
                            print("\n🎯 ESP32 DEVICE FOUND!")
                            print(f"Name: {name}")
                            print(f"Address: {address}")
                            print(f"RSSI: {device.rssi}dBm")
                            print("\nYou can use this address in the RFID listener.")
                            self.esp32_found = True
                            print("\nContinuing to monitor signal strength...")
                        else:
                            # Update signal strength for monitoring
                            print(f"\rRSSI: {device.rssi}dBm | Distance: {'Near' if device.rssi > -70 else 'Medium' if device.rssi > -85 else 'Far'}", end="")
                    

                
            except Exception as e:
                print(f"Scan error: {str(e)}")
                await asyncio.sleep(1)

async def main():
    monitor = BLEDeviceMonitor()
    try:
        await monitor.scan_loop()
    except KeyboardInterrupt:
        print("\nStopping scan...")
        monitor.running = False

if __name__ == "__main__":
    asyncio.run(main())