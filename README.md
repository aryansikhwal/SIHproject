# 🎯 AttenSync - Automated RFID Attendance System

![AttenSync](https://img.shields.io/badge/AttenSync-RFID%20Attendance-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=flat-square)
![React](https://img.shields.io/badge/React-18+-blue?style=flat-square)
![ESP32](https://img.shields.io/badge/ESP32-BLE%20RFID-red?style=flat-square)

A comprehensive **IoT-based attendance management system** that combines **ESP32 RFID hardware** with a modern **React web dashboard** for real-time attendance tracking.

## 🌟 Key Features

- 🔷 **Real-time RFID Scanning** - ESP32 Bluetooth integration
- 🎨 **Modern Web Dashboard** - React-based responsive UI
- 📊 **Live Analytics** - Real-time attendance statistics
- 👥 **Student Management** - Complete CRUD operations
- 📱 **Mobile Responsive** - Works on all devices
- 🔄 **Live Data Sync** - Instant updates across all interfaces
- 🌏 **Indian Localization** - Pre-loaded with authentic Indian student data

## 🚀 Quick Start

### Option 1: Automated Setup

```bash
# Clone the repository
git clone https://github.com/aryansikhwal/SIHproject.git
cd SIHproject

# Run automated setup script
# Windows:
quick_setup.bat
# Linux/macOS:
chmod +x quick_setup.sh && ./quick_setup.sh
```

### Option 2: Manual Setup

📖 **For detailed setup instructions, see [SETUP.md](SETUP.md)**

## 🎯 Quick Run

```bash
# Start backend server
python backend.py

# Start frontend (in another terminal)
cd client && npm start

# Access the application
# Web Dashboard: http://localhost:3000
# API Endpoints: http://localhost:5000/api/
```

## 🔧 Tech Stack

| Component | Technology |
|-----------|------------|
| **Frontend** | React 18, TailwindCSS, Axios |
| **Backend** | Flask, SQLAlchemy, Flask-CORS |
| **Database** | SQLite (development), PostgreSQL (production) |
| **Hardware** | ESP32, RFID-RC522, Bluetooth Low Energy |
| **Communication** | REST API, WebSocket (future), BLE |

## 📱 Hardware Requirements

- **ESP32 Development Board**
- **RFID-RC522 Module**  
- **RFID Cards/Tags**
- **Bluetooth-enabled Computer**

*Note: Software runs independently without hardware for demo purposes*

## 📊 System Architecture

```
┌─────────────┐    BLE     ┌──────────────┐    HTTP    ┌─────────────┐
│   ESP32     │◄──────────►│    Python    │◄──────────►│   React     │
│   RFID      │            │   Backend    │            │  Dashboard  │
│  Scanner    │            │   (Flask)    │            │    (Web)    │
└─────────────┘            └──────────────┘            └─────────────┘
                                   │
                                   ▼
                           ┌──────────────┐
                           │   SQLite     │
                           │  Database    │
                           └──────────────┘
```

## 🎨 Screenshots

*Dashboard with real-time RFID scan data and attendance analytics*

## 📈 Sample Data

The system comes pre-loaded with **Indian student data**:

- Arjun Sharma, Priya Patel, Rajesh Kumar, Sneha Gupta, and more
- Realistic roll numbers (2024001-2024010)
- Complete attendance history
- RFID card assignments

## 🤖 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | System status |
| `/api/students` | GET/POST | Student management |
| `/api/attendance` | GET/POST | Attendance operations |
| `/api/rfid/scans` | GET | RFID scan logs |
| `/api/stats/dashboard` | GET | Dashboard analytics |

## 🔧 Development

```bash
# Backend development
python backend.py  # Auto-reload enabled

# Frontend development  
cd client && npm start  # Hot reload enabled

# Database reset
python initialize_system.py --reset
```

## 📋 Project Structure

```
AttenSync/
├── 📁 client/                 # React frontend
│   ├── 📁 src/components/     # React components
│   ├── 📁 src/pages/          # Page components
│   └── 📁 src/services/       # API services
├── 📄 backend.py              # Flask server
├── 📄 models.py               # Database models
├── 📄 direct_esp32_connection.py  # ESP32 BLE handler
├── 📄 initialize_system.py    # Database setup
├── 📄 requirements.txt        # Python dependencies
├── 📄 SETUP.md               # Detailed setup guide
└── 📄 README.md              # This file
```

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature-name`
3. **Commit** your changes: `git commit -m 'Add feature'`
4. **Push** to the branch: `git push origin feature-name`  
5. **Open** a Pull Request

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🏆 Achievements

- ✅ **End-to-end IoT Solution** - Hardware to Web Dashboard
- ✅ **Real-time Data Processing** - Live RFID scan integration  
- ✅ **Professional UI/UX** - Modern React interface
- ✅ **Scalable Architecture** - RESTful API design
- ✅ **Production Ready** - Complete with documentation

## 📞 Support

Having issues? Check our **[Setup Guide](SETUP.md)** or create an issue with:
- Your operating system
- Python/Node.js versions  
- Error messages/screenshots
- Steps to reproduce

---

**⭐ Star this repository if you find it helpful!**

*Built with ❤️ for the future of automated attendance management*