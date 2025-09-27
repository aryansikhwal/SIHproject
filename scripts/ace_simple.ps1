# AttenSync - Simple ACE COMMAND with RFID Tag Display
# Always runs in virtual environment

$ErrorActionPreference = "Continue"

Write-Host "🎯 AttenSync ACE COMMAND (Simple)" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Blue

# Get project root and activate environment
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $ProjectRoot

# Force virtual environment activation
$venvActivate = ".\.venv\Scripts\Activate.ps1"
if (Test-Path $venvActivate) {
    Write-Host "✅ Activating virtual environment..." -ForegroundColor Green
    & $venvActivate
} else {
    Write-Host "❌ Virtual environment not found!" -ForegroundColor Red
    exit 1
}

# Start services
Write-Host "`n🚀 Starting AttenSync Services..." -ForegroundColor Green

# Backend
Write-Host "Starting Backend..." -ForegroundColor Cyan
$backendJob = Start-Job -ScriptBlock {
    param($root)
    Set-Location "$root"
    & ".\.venv\Scripts\Activate.ps1"
    Set-Location "$root\src\backend"
    python backend.py
} -ArgumentList $ProjectRoot

# Frontend  
Write-Host "Starting Frontend..." -ForegroundColor Cyan
$frontendJob = Start-Job -ScriptBlock {
    param($root)
    Set-Location "$root\src\frontend"
    $env:BROWSER = "none"
    npm start
} -ArgumentList $ProjectRoot

# RFID System
Write-Host "Starting RFID System..." -ForegroundColor Cyan
$rfidJob = Start-Job -ScriptBlock {
    param($root)
    Set-Location "$root"
    & ".\.venv\Scripts\Activate.ps1"
    Set-Location "$root\src\hardware"
    python rfid_system.py
} -ArgumentList $ProjectRoot

Start-Sleep -Seconds 3

Write-Host "`n✅ All services started!" -ForegroundColor Green
Write-Host "Backend: http://localhost:5000" -ForegroundColor White
Write-Host "Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "`n🏷️ RFID Tag Monitor - Watching for scans..." -ForegroundColor Yellow
Write-Host "Press Ctrl+C to quit" -ForegroundColor Gray
Write-Host "===========================================" -ForegroundColor Blue

# Real-time RFID monitoring
try {
    while ($true) {
        Start-Sleep -Seconds 1
        
        # Get RFID output
        $rfidOutput = Receive-Job $rfidJob -Keep -ErrorAction SilentlyContinue
        if ($rfidOutput) {
            $lastLine = $rfidOutput | Select-Object -Last 1
            if ($lastLine) {
                $timestamp = Get-Date -Format "HH:mm:ss"
                
                if ($lastLine -like "*Card detected*") {
                    Write-Host "[$timestamp] 🏷️ RFID TAG DETECTED!" -ForegroundColor Green -BackgroundColor DarkGreen
                    Write-Host "    $lastLine" -ForegroundColor White
                    Write-Host ""
                } elseif ($lastLine -like "*DUPLICATE*") {
                    Write-Host "[$timestamp] ⚠️ DUPLICATE SCAN" -ForegroundColor Yellow
                    Write-Host "    $lastLine" -ForegroundColor White
                    Write-Host ""
                } elseif ($lastLine -like "*SUCCESS*") {
                    Write-Host "[$timestamp] ✅ ATTENDANCE MARKED" -ForegroundColor Cyan
                    Write-Host "    $lastLine" -ForegroundColor White
                    Write-Host ""
                } elseif ($lastLine -like "*Connected*ESP32*") {
                    Write-Host "[$timestamp] 🔗 ESP32 Connected" -ForegroundColor Cyan
                } elseif ($lastLine -like "*FOUND*ESP32*") {
                    Write-Host "[$timestamp] 📡 ESP32 Found" -ForegroundColor Green
                } elseif ($lastLine -like "*ERROR*") {
                    Write-Host "[$timestamp] ❌ ERROR" -ForegroundColor Red
                    Write-Host "    $lastLine" -ForegroundColor White
                }
            }
        }
    }
} finally {
    Write-Host "`n🛑 Stopping all services..." -ForegroundColor Yellow
    Stop-Job $backendJob -ErrorAction SilentlyContinue
    Stop-Job $frontendJob -ErrorAction SilentlyContinue  
    Stop-Job $rfidJob -ErrorAction SilentlyContinue
    Remove-Job $backendJob -ErrorAction SilentlyContinue
    Remove-Job $frontendJob -ErrorAction SilentlyContinue
    Remove-Job $rfidJob -ErrorAction SilentlyContinue
    Write-Host "✅ All services stopped" -ForegroundColor Green
}