# 🚀 AttenSync Setup Instructions

Welcome to **AttenSync** - An automated RFID-based attendance management system with ESP32 integration!

## 📋 Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.8+** ([Download here](https://www.python.org/downloads/))
- **Node.js 16+** ([Download here](https://nodejs.org/))
- **Git** ([Download here](https://git-scm.com/))
- **ESP32 RFID Hardware** (Optional - for live RFID scanning)

## 🔧 Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/aryansikhwal/SIHproject.git
cd SIHproject
```

### 2️⃣ Python Backend Setup

```bash
# Create and activate virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Initialize the database with sample data
python initialize_system.py
```

### 3️⃣ React Frontend Setup

```bash
# Navigate to client directory
cd client

# Install Node.js dependencies
npm install

# Return to root directory
cd ..
```

## 🎯 Running the Application

### Method 1: Run Both Services Manually

**Terminal 1 - Start Backend Server:**
```bash
# Activate virtual environment (if not already active)
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Start Flask backend server
python backend.py
```
*Backend will run on: http://localhost:5000*

**Terminal 2 - Start Frontend Server:**
```bash
# In a new terminal, navigate to client folder
cd client

# Start React development server
npm start
```
*Frontend will run on: http://localhost:3000*

### Method 2: Quick Start Scripts (Windows)

```bash
# Start backend
start_backend.sh

# Start frontend (in another terminal)
start_frontend.sh
```

## 🌐 Accessing the Application

Once both servers are running:

- **Web Dashboard:** http://localhost:3000
- **API Endpoints:** http://localhost:5000/api/
- **Backend Health:** http://localhost:5000/api/health

## 📱 ESP32 RFID Integration (Optional)

If you have ESP32 RFID hardware:

### Prerequisites:
- ESP32 with RFID-RC522 module
- Bluetooth capability on your system
- RFID cards for testing

### Setup Steps:

1. **Flash ESP32** with the provided Arduino code (check hardware documentation)

2. **Connect ESP32 via Bluetooth:**
```bash
# Test BLE connection
python ble_connection_test.py

# Start RFID listener for live scanning
python direct_esp32_connection.py
```

3. **Register RFID Cards:**
```bash
# Register your physical RFID cards to students
python register_rfid_cards.py
```

## 🎨 Sample Data & Students

The system comes pre-loaded with Indian student data:

- **Arjun Sharma** (Roll: 2024001) - *Can be linked to your RFID*
- **Priya Patel** (Roll: 2024002) - *Can be linked to your RFID*
- **Rajesh Kumar** (Roll: 2024003)
- **Sneha Gupta** (Roll: 2024004)
- ... and 6 more students

To update students with your own data:
```bash
python update_indian_names.py
```

## 🔧 Configuration

### Environment Variables (Optional)

Create a `.env` file in the root directory for custom configuration:

```env
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Database Configuration
DATABASE_URL=sqlite:///instance/attensync.db

# API Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:5000

# ESP32 Configuration
ESP32_MAC_ADDRESS=D4:8A:FC:C7:CF:72
BLE_SERVICE_UUID=12345678-1234-1234-1234-1234567890ab
```

### Database Reset

If you need to reset the database:
```bash
python initialize_system.py --reset
```

## 📊 Features Overview

### ✅ Core Features:
- **Real-time RFID Scanning** - ESP32 Bluetooth integration
- **Student Management** - Add, edit, delete students
- **Attendance Tracking** - Automatic attendance marking
- **Dashboard Analytics** - Visual attendance statistics  
- **RFID Scan Logs** - Detailed scan history with status
- **Responsive Web UI** - Modern React interface
- **API Endpoints** - RESTful API for all operations

### 🎯 Advanced Features:
- **Indian Student Database** - Pre-loaded authentic data
- **Multi-language Support** - English + regional languages
- **Offline Capabilities** - Works without internet
- **Real-time Updates** - Live data synchronization
- **Export Functionality** - Download attendance reports

## 🛠️ Troubleshooting

### Common Issues:

**1. Port Already in Use:**
```bash
# Kill processes on ports 3000/5000
# Windows:
taskkill /F /IM python.exe
taskkill /F /IM node.exe

# macOS/Linux:
sudo lsof -t -i tcp:3000 | xargs kill -9
sudo lsof -t -i tcp:5000 | xargs kill -9
```

**2. Python Dependencies Issues:**
```bash
# Upgrade pip and reinstall
python -m pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

**3. Node.js Dependencies Issues:**
```bash
# Clear npm cache and reinstall
cd client
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

**4. Database Issues:**
```bash
# Reset database
python initialize_system.py --reset
```

**5. ESP32 Connection Issues:**
- Ensure ESP32 is powered on and running RFID code
- Check Bluetooth is enabled on your system
- Verify ESP32 MAC address in configuration
- Try running: `python ble_connection_test.py`

## 📝 API Documentation

### Key Endpoints:

- `GET /api/health` - System health check
- `GET /api/students` - List all students
- `POST /api/students` - Add new student
- `GET /api/attendance` - Get attendance records
- `POST /api/attendance` - Mark attendance
- `GET /api/rfid/scans` - Get RFID scan logs
- `GET /api/stats/dashboard` - Dashboard statistics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues:

1. Check this README for troubleshooting steps
2. Review the logs for error messages
3. Create an issue on GitHub with:
   - Your operating system
   - Python and Node.js versions
   - Error messages or screenshots
   - Steps to reproduce the problem

## 🎉 Success!

If everything is set up correctly, you should see:

✅ Backend server running on http://localhost:5000  
✅ Frontend dashboard on http://localhost:3000  
✅ Sample students loaded in database  
✅ RFID scanning ready (if hardware connected)  

**Congratulations! Your AttenSync system is ready to use!** 🚀

---

*Built with ❤️ for automated attendance management*