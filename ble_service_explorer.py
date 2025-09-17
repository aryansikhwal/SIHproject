import asyncio
from bleak import BleakClient, BleakScanner

ESP32_MAC = "D4:8A:FC:C7:CF:72"  # Update if needed

async def explore_services(address):
    print(f"Connecting to {address}...")
    async with BleakClient(address) as client:
        print("Connected! Discovering services...")
        for service in client.services:
            print(f"\nService: {service.uuid} ({service.description})")
            for char in service.characteristics:
                props = ', '.join(char.properties)
                print(f"  Characteristic: {char.uuid} ({char.description})")
                print(f"    Properties: {props}")
                if char.descriptors:
                    for desc in char.descriptors:
                        print(f"    Descriptor: {desc.uuid}")

async def main():
    print("Scanning for ESP32...")
    devices = await BleakScanner().discover(timeout=5.0)
    target = None
    for d in devices:
        if d.address.upper() == ESP32_MAC or (d.name and "ESP32" in d.name):
            target = d.address
            print(f"Found: {d.name} ({d.address})")
            break
    if not target:
        print("ESP32 not found. Make sure it is advertising and in range.")
        return
    await explore_services(target)

if __name__ == "__main__":
    asyncio.run(main())
