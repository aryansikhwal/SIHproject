# AttenSync Startup Scripts

This directory contains various scripts to start the AttenSync RFID Attendance System components.

## 🚀 Quick Start (Recommended)

### Windows Users:
```powershell
# Option 1: Double-click this file
scripts\start_attensync.bat

# Option 2: Run in PowerShell
powershell -ExecutionPolicy Bypass -File scripts\start_attensync.ps1

# Option 3: PowerShell directly
cd scripts
.\start_attensync.ps1
```

### Linux/macOS Users:
```bash
# Make executable (first time only)
chmod +x scripts/start_attensync.sh

# Run the unified launcher
./scripts/start_attensync.sh
```

## 📋 Available Options

### Unified Launcher Options:
- `--skip-deps` / `-SkipDeps`: Skip dependency installation
- `--no-rfid` / `-NoRFID`: Skip RFID hardware listener (useful for web-only testing)
- `--production` / `-DevMode $false`: Run in production mode

### Examples:
```bash
# Skip RFID hardware (for web-only development)
./scripts/start_attensync.sh --no-rfid

# Skip dependency installation (faster startup)
./scripts/start_attensync.sh --skip-deps

# Windows equivalent
.\scripts\start_attensync.ps1 -NoRFID -SkipDeps
```

## 🔧 Individual Component Scripts

If you need to start components individually:

```bash
# Start only backend
./scripts/start_backend.sh

# Start only frontend  
./scripts/start_frontend.sh

# Start only RFID listener
./scripts/start_rfid.sh
```

## 🌐 Service URLs

Once started, access AttenSync at:

- **Frontend (Web Interface)**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **API Health Check**: http://localhost:5000/api/health

## 📊 What Gets Started

The unified launcher starts these components in parallel:

1. **Flask Backend Server** (Port 5000)
   - REST API endpoints
   - Database operations
   - Authentication & session management

2. **React Frontend Server** (Port 3000) 
   - Web dashboard
   - Student management interface
   - Real-time attendance views

3. **RFID Hardware Listener** (Background)
   - ESP32 Bluetooth Low Energy connection
   - RFID card scanning
   - Automatic attendance logging

## 🛑 Stopping Services

- **Windows**: Press 'q' + Enter in the PowerShell window, or Ctrl+C
- **Linux/macOS**: Press Ctrl+C to stop all services

## 📝 Logs

Logs are created in the `logs/` directory:
- `logs/backend.log` - Flask backend logs
- `logs/frontend.log` - React development server logs  
- `logs/rfid.log` - RFID hardware listener logs

## ⚠️ Troubleshooting

### Common Issues:

1. **Port already in use**:
   - Stop other processes using ports 3000 or 5000
   - Or modify the port in the respective config files

2. **Python not found**:
   - Install Python 3.8+ from python.org
   - Ensure python is in your system PATH

3. **Node.js/npm not found**:
   - Install Node.js 16+ from nodejs.org
   - This includes npm automatically

4. **Permission errors (Linux/macOS)**:
   ```bash
   chmod +x scripts/*.sh
   ```

5. **RFID hardware not connecting**:
   - **Quick fix**: Use `--no-rfid` flag to skip hardware
   - **For RFID setup**: See `docs/RFID_SETUP.md` for detailed installation guide
   - **Dependencies**: RFID requires `bleak` and `pyserial` packages
   - **Install**: `pip install bleak pyserial` (may require Visual Studio Build Tools on Windows)

### RFID Dependencies Note:
The RFID listener requires additional dependencies (`bleak`, `pyserial`) that may need special setup on Windows. If you encounter build errors:
- See `docs/RFID_SETUP.md` for detailed instructions
- Or use `--no-rfid` flag to run web-only mode
- The unified launcher will automatically detect missing RFID dependencies and skip gracefully

## 🔧 Development Mode vs Production

- **Development Mode** (default): Hot reloading, debug output, detailed logs
- **Production Mode**: Optimized builds, minimal logs, better performance

For production deployment, use:
```bash
./scripts/start_attensync.sh --production
```

## 📚 Dependencies

The launcher automatically installs:

**Python packages** (from requirements.txt):
- Flask, SQLAlchemy, pandas, etc.

**Node.js packages** (from src/frontend/package.json):
- React, axios, recharts, etc.

Use `--skip-deps` to skip automatic installation if dependencies are already installed.