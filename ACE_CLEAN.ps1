# ACE Clean - AttenSync Complete Environment
Write-Host "AttenSync Complete Environment" -ForegroundColor Cyan
Write-Host ""

# Ensure we're in the project directory
Set-Location $PSScriptRoot

# Stop existing processes and free ports
Write-Host "Cleaning up processes..." -ForegroundColor Yellow
Get-Process | Where-Object {$_.ProcessName -eq "python" -or $_.ProcessName -eq "node"} | Stop-Process -Force -ErrorAction SilentlyContinue
netstat -ano | findstr ":5000" | ForEach-Object { $procId = ($_ -split '\s+')[-1]; if($procId -match '^\d+$') { taskkill /f /pid $procId 2>$null } }
netstat -ano | findstr ":3000" | ForEach-Object { $procId = ($_ -split '\s+')[-1]; if($procId -match '^\d+$') { taskkill /f /pid $procId 2>$null } }
Write-Host "Ports cleared" -ForegroundColor Green

# Check if virtual environment exists
if (-not (Test-Path ".\.venv\Scripts\Activate.ps1")) {
    Write-Host "Virtual environment not found! Please create it first:" -ForegroundColor Red
    Write-Host "python -m venv .venv" -ForegroundColor Yellow
    Write-Host ".\.venv\Scripts\Activate.ps1" -ForegroundColor Yellow
    Write-Host "pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment
Write-Host "Activating Environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1
# Note: Activation script may return non-zero even when successful

# Verify environment by checking python path
$pythonPath = & .\.venv\Scripts\python.exe -c "import sys; print(sys.executable)" 2>$null
if ($pythonPath -match "\.venv") {
    Write-Host "Virtual environment activated successfully" -ForegroundColor Green
} else {
    Write-Host "Failed to activate virtual environment!" -ForegroundColor Red
    exit 1
}

# Quick dependency check
Write-Host "Checking dependencies..." -ForegroundColor Yellow
& .\.venv\Scripts\python.exe -c "import flask, bleak, serial, colorama"
if ($LASTEXITCODE -eq 0) {
    Write-Host "Dependencies OK" -ForegroundColor Green
} else {
    Write-Host "Missing dependencies! Installing..." -ForegroundColor Yellow
    & .\.venv\Scripts\pip.exe install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to install dependencies!" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "Starting Services..." -ForegroundColor Cyan

# Start Backend with explicit venv python
Write-Host "Backend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\.venv\Scripts\python.exe .\src\backend\backend.py"
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

# Run RFID system with explicit venv python
& .\.venv\Scripts\python.exe .\src\hardware\rfid_system.py