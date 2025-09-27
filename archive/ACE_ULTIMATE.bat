@echo off
echo 🎯 AttenSync ULTIMATE ACE COMMAND 🎯
echo ====================================

cd /d "%~dp0\.."
echo ✅ Changed to project directory

echo 🔄 Activating virtual environment...
call .venv\Scripts\activate.bat

echo 🚀 Starting Backend Server...
start /min cmd /k "python src\backend\backend.py"

echo 🚀 Starting Frontend Server...
start /min cmd /k "cd src\frontend && npm start"

echo 🏷️ STARTING RFID TAG MONITOR - LIVE DISPLAY
echo ============================================
echo Tags will appear below in REAL TIME:
echo.

cd src\hardware
python rfid_system.py

echo.
echo ✅ RFID Monitor stopped
pause