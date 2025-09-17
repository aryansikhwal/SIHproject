import asyncio
from bleak import BleakScanner
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

async def scan_devices():
    print("Starting detailed BLE scan...")
    print("Press Ctrl+C to stop\n")
    
    while True:
        try:
            devices = await BleakScanner().discover(timeout=5.0)
            print("\nDiscovered Devices:")
            print("=" * 50)
            for d in sorted(devices, key=lambda x: x.rssi, reverse=True):
                print(f"\nDevice: {d.name if d.name else 'Unknown'}")
                print(f"Address: {d.address}")
                print(f"RSSI: {d.rssi}dBm")
                print(f"Details: {d.details}")
                if d.metadata:
                    print("Metadata:")
                    for k, v in d.metadata.items():
                        print(f"  {k}: {v}")
                print("-" * 50)
            print("\nWaiting 2 seconds before next scan...")
            await asyncio.sleep(2)
        except KeyboardInterrupt:
            print("\nScan stopped by user")
            break
        except Exception as e:
            print(f"Scan error: {e}")
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(scan_devices())