@echo off
REM Quick Setup Script for AttenSync (Windows)
REM Run this after cloning the repository

echo 🚀 AttenSync Quick Setup Script (Windows)
echo ==========================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 16+ first.
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed

REM Create virtual environment
echo 📦 Creating Python virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate

REM Install Python dependencies
echo 📚 Installing Python dependencies...
pip install -r requirements.txt

REM Initialize database
echo 🗄️ Initializing database with sample data...
python initialize_system.py

REM Install Node.js dependencies
echo ⚛️ Installing React dependencies...
cd client
npm install
cd ..

echo.
echo 🎉 Setup Complete!
echo ===================
echo.
echo To run the application:
echo 1️⃣ Backend:  python backend.py
echo 2️⃣ Frontend: cd client ^&^& npm start
echo.
echo Then visit: http://localhost:3000
echo.
echo For RFID hardware: python direct_esp32_connection.py
echo.
echo Happy coding! 🚀
pause