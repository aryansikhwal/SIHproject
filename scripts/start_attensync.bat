@echo off
REM AttenSync - Simple Windows Launcher
REM Double-click this file to start AttenSync

title AttenSync Launcher

echo.
echo     ____  __  __            ____
echo    /  _/ / /_/ /___  ____  / __/__ ______  _____
echo    / /  / __/ __/ / / / /_/ /\ \/ / / / _ \/ ___/
echo  _/ /  / /_/ /_/ /_/ / __/___/ / /_/ /  __/ /__  
echo /___/  \__/\__/\__, /\__//____/\__, /\___/\___/  
echo              /____/          /____/             
echo.
echo AttenSync RFID Attendance System
echo.

REM Change to the script directory
cd /d "%~dp0"

REM Check if PowerShell is available
where powershell >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: PowerShell not found!
    echo Please install PowerShell or run the .ps1 script manually.
    pause
    exit /b 1
)

echo Starting AttenSync with PowerShell...
echo.

REM Execute the PowerShell script
powershell.exe -ExecutionPolicy Bypass -File "start_attensync.ps1"

REM Keep window open if script exits unexpectedly
if %errorlevel% neq 0 (
    echo.
    echo Script exited with error code: %errorlevel%
    pause
)