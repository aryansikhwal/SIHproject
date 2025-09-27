# ACE Clean - AttenSync Complete Environment
Write-Host "AttenSync Complete Environment" -ForegroundColor Cyan
Write-Host ""

# Stop existing processes and free ports
Write-Host "Cleaning up processes..." -ForegroundColor Yellow
Get-Process | Where-Object {$_.ProcessName -eq "python" -or $_.ProcessName -eq "node"} | Stop-Process -Force -ErrorAction SilentlyContinue
netstat -ano | findstr ":5000" | ForEach-Object { $pid = ($_ -split '\s+')[-1]; if($pid -match '^\d+$') { taskkill /f /pid $pid 2>$null } }
netstat -ano | findstr ":3000" | ForEach-Object { $pid = ($_ -split '\s+')[-1]; if($pid -match '^\d+$') { taskkill /f /pid $pid 2>$null } }
Write-Host "Ports cleared" -ForegroundColor Green

# Activate virtual environment
Write-Host "Activating Environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

# Quick dependency check
Write-Host "Checking dependencies..." -ForegroundColor Yellow
& python -c "import flask, bleak, serial, colorama"
if ($LASTEXITCODE -eq 0) {
    Write-Host "Dependencies OK" -ForegroundColor Green
} else {
    Write-Host "Missing dependencies!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Starting Services..." -ForegroundColor Cyan

# Start Backend
Write-Host "Backend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\.venv\Scripts\Activate.ps1; python .\src\backend\backend.py"
Write-Host "Backend deployed" -ForegroundColor Green

# Start Frontend  
Write-Host "Frontend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\src\frontend'; npm start"
Write-Host "Frontend deployed" -ForegroundColor Green

# Wait briefly
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "Starting RFID System..." -ForegroundColor Green
Write-Host ""

# Run RFID system
& python .\src\hardware\rfid_system.py