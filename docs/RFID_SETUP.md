# RFID Hardware Setup Guide

## Overview
AttenSync's RFID functionality uses Bluetooth Low Energy (BLE) to communicate with ESP32-based RFID readers. This requires additional Python dependencies that may need special setup on Windows.

## Quick Install (if you have Visual Studio Build Tools)
```bash
pip install bleak pyserial
```

## Windows Installation (Detailed)

### Option 1: Install Pre-compiled Wheels
Try this first - it often works without needing Visual Studio:
```powershell
pip install --upgrade pip
pip install bleak pyserial --prefer-binary
```

### Option 2: Install Visual Studio Build Tools
If Option 1 fails, you need Microsoft Visual Studio Build Tools:

1. Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Install "C++ build tools" workload
3. Restart your computer
4. Run: `pip install bleak pyserial`

### Option 3: Use Conda (Recommended for complex setups)
```bash
conda install -c conda-forge bleak pyserial
```

## Testing RFID Dependencies
Test if dependencies are installed correctly:
```python
# Test script
try:
    import bleak
    import serial
    print("✅ RFID dependencies are installed!")
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
```

## Hardware Requirements
- ESP32 development board
- RFID-RC522 module
- Bluetooth Low Energy support
- Proper wiring between ESP32 and RFID module

## Troubleshooting

### "bleak-winrt build failed" Error
This means you need Visual Studio Build Tools (see Option 2 above).

### "Serial port not found" Error
- Check ESP32 connection
- Install correct USB drivers for your ESP32 board
- Verify COM port in Device Manager

### "Bluetooth adapter not found" Error
- Ensure your computer has Bluetooth capability
- Update Bluetooth drivers
- Try restarting Bluetooth service

## Running Without RFID
AttenSync can run perfectly without RFID hardware:
```bash
# Skip RFID component
./scripts/start_attensync.sh --no-rfid
# or
.\scripts\start_attensync.ps1 -NoRFID
```

## Development Mode
For development/testing without actual hardware, you can:
1. Use the demo RFID simulator: `python src/hardware/demo_rfid.py`
2. Run web-only mode with `--no-rfid` flag
3. Manually add attendance records via the web interface