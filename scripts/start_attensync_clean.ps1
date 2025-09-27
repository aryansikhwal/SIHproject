# AttenSync - Unified Startup Script for Windows
# Starts all components: Backend, Frontend, and RFID Hardware Listener

param(
    [switch]$SkipDeps = $false,
    [switch]$NoRFID = $false
)

$ErrorActionPreference = "Continue"
$Host.UI.RawUI.WindowTitle = "AttenSync - Unified Launcher"

Write-Host "AttenSync Unified Startup Script" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Blue

# Get script directory and set project root
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
Set-Location $ProjectRoot

Write-Host "Project Root: $ProjectRoot" -ForegroundColor Cyan

# Function to check if a command exists
function Test-Command($cmd) {
    try { 
        if (Get-Command $cmd -ErrorAction SilentlyContinue) { 
            return $true 
        } 
    }
    catch { 
        return $false 
    }
    return $false
}

# Check prerequisites
Write-Host "`nChecking Prerequisites..." -ForegroundColor Yellow
$prereqs = $true

if (-not (Test-Command "python")) {
    Write-Host "Python not found! Please install Python 3.8+" -ForegroundColor Red
    $prereqs = $false
} else {
    Write-Host "Python found" -ForegroundColor Green
}

if (-not (Test-Command "node")) {
    Write-Host "Node.js not found! Please install Node.js 16+" -ForegroundColor Red
    $prereqs = $false
} else {
    Write-Host "Node.js found" -ForegroundColor Green
}

if (-not (Test-Command "npm")) {
    Write-Host "npm not found! Please install Node.js with npm" -ForegroundColor Red
    $prereqs = $false
} else {
    Write-Host "npm found" -ForegroundColor Green
}

if (-not $prereqs) {
    Write-Host "`nPrerequisites missing! Please install required software." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Install dependencies if not skipped
if (-not $SkipDeps) {
    Write-Host "`nInstalling/Updating Dependencies..." -ForegroundColor Yellow
    
    # Check for virtual environment
    Write-Host "Checking virtual environment..." -ForegroundColor Cyan
    $venvPath = Join-Path $ProjectRoot ".venv"
    if (-not (Test-Path $venvPath)) {
        Write-Host "Virtual environment not found at $venvPath" -ForegroundColor Red
        Write-Host "Please create it first: python -m venv .venv" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    # Install Python dependencies in virtual environment
    Write-Host "Installing Python packages in virtual environment..." -ForegroundColor Cyan
    try {
        & "$venvPath\Scripts\pip.exe" install -r requirements.txt --quiet
        Write-Host "Python packages installed in virtual environment" -ForegroundColor Green
    }
    catch {
        Write-Host "Python dependencies installation had issues, continuing..." -ForegroundColor Yellow
    }
    
    # Install Node.js dependencies
    Write-Host "Installing Node.js packages..." -ForegroundColor Cyan
    try {
        Set-Location "src\frontend"
        npm install --silent
        Write-Host "Node.js packages installed" -ForegroundColor Green
        Set-Location $ProjectRoot
    }
    catch {
        Write-Host "Node.js dependencies installation had issues, continuing..." -ForegroundColor Yellow
        Set-Location $ProjectRoot
    }
}

Write-Host "`nStarting AttenSync Components..." -ForegroundColor Green

# Array to store background jobs
$jobs = @()

# Start Backend Server
Write-Host "Starting Backend Server (Flask)..." -ForegroundColor Cyan
$backendJob = Start-Job -ScriptBlock {
    param($projectRoot)
    Set-Location "$projectRoot\src\backend"
    & "$projectRoot\.venv\Scripts\python.exe" backend.py
} -ArgumentList $ProjectRoot
$jobs += $backendJob
Write-Host "Backend started (Job ID: $($backendJob.Id))" -ForegroundColor Green

# Wait a moment for backend to initialize
Start-Sleep -Seconds 3

# Start Frontend Development Server
Write-Host "Starting Frontend Server (React)..." -ForegroundColor Cyan
$frontendJob = Start-Job -ScriptBlock {
    param($projectRoot)
    Set-Location "$projectRoot\src\frontend"
    $env:BROWSER = "none"
    npm start
} -ArgumentList $ProjectRoot
$jobs += $frontendJob
Write-Host "Frontend started (Job ID: $($frontendJob.Id))" -ForegroundColor Green

# Start RFID Hardware Listener (optional)
$rfidJob = $null
if (-not $NoRFID) {
    Write-Host "Starting RFID Hardware Listener..." -ForegroundColor Cyan
    
    # Test if RFID dependencies are available in virtual environment
    $rfidTestResult = & "$ProjectRoot\.venv\Scripts\python.exe" -c "try: import bleak; print('OK')
except ImportError: print('MISSING_DEPS')" 2>$null
    
    if ($rfidTestResult -eq "OK") {
        $rfidJob = Start-Job -ScriptBlock {
            param($projectRoot)
            Set-Location "$projectRoot\src\hardware"
            & "$projectRoot\.venv\Scripts\python.exe" rfid_system.py
        } -ArgumentList $ProjectRoot
        $jobs += $rfidJob
        Write-Host "RFID Listener started (Job ID: $($rfidJob.Id))" -ForegroundColor Green
    } else {
        Write-Host "RFID dependencies (bleak) not installed in virtual environment - skipping RFID listener" -ForegroundColor Yellow
        Write-Host "To install: .\.venv\Scripts\pip.exe install bleak pyserial" -ForegroundColor Gray
    }
} else {
    Write-Host "RFID Listener skipped (NoRFID flag)" -ForegroundColor Yellow
}

# Display service information
Write-Host "`nAttenSync Services Running:" -ForegroundColor Green
Write-Host "Backend API:    http://localhost:5000" -ForegroundColor White
Write-Host "Frontend Web:   http://localhost:3000" -ForegroundColor White
Write-Host "API Health:     http://localhost:5000/api/health" -ForegroundColor White
if ($rfidJob) {
    Write-Host "RFID Listener:  Active" -ForegroundColor White
} else {
    Write-Host "RFID Listener:  Not started (missing dependencies or disabled)" -ForegroundColor Gray
}

Write-Host "`nPress 'q' + Enter to quit all services" -ForegroundColor Yellow
Write-Host "Press 'r' + Enter to show real-time RFID activity" -ForegroundColor Yellow

# Simple management loop with RFID monitoring
do {
    $input = Read-Host "`nAttenSync Manager (q=quit, s=status, l=logs, r=rfid)"
    
    if ($input.ToLower() -eq "q") {
        Write-Host "`nStopping all AttenSync services..." -ForegroundColor Yellow
        foreach ($job in $jobs) {
            Stop-Job $job -PassThru | Remove-Job
        }
        Write-Host "All services stopped. Goodbye!" -ForegroundColor Green
        break
    } 
    elseif ($input.ToLower() -eq "s") {
        Write-Host "`nService Status:" -ForegroundColor Cyan
        foreach ($job in $jobs) {
            $status = Get-Job $job
            $jobName = if ($job.Id -eq $backendJob.Id) { "Backend" } elseif ($job.Id -eq $frontendJob.Id) { "Frontend" } elseif ($rfidJob -and $job.Id -eq $rfidJob.Id) { "RFID" } else { "Unknown" }
            Write-Host "  $jobName (Job $($job.Id)): $($status.State)" -ForegroundColor White
        }
        if (-not $rfidJob) {
            Write-Host "  RFID: Not started (missing dependencies or disabled)" -ForegroundColor Gray
        }
    } 
    elseif ($input.ToLower() -eq "l") {
        Write-Host "`nRecent Job Output:" -ForegroundColor Cyan
        foreach ($job in $jobs) {
            $jobName = if ($job.Id -eq $backendJob.Id) { "Backend" } elseif ($job.Id -eq $frontendJob.Id) { "Frontend" } elseif ($rfidJob -and $job.Id -eq $rfidJob.Id) { "RFID" } else { "Unknown" }
            Write-Host "--- $jobName (Job $($job.Id)) ---" -ForegroundColor Yellow
            try {
                $output = Receive-Job $job -Keep | Select-Object -Last 10
                if ($output) {
                    $output | ForEach-Object { Write-Host $_ }
                } else {
                    Write-Host "No output available" -ForegroundColor Gray
                }
            }
            catch {
                Write-Host "Error reading job output: $_" -ForegroundColor Red
            }
        }
    } 
    elseif ($input.ToLower() -eq "r") {
        if ($rfidJob) {
            Write-Host "`n🎯 RFID Real-Time Monitor - Press Ctrl+C to return" -ForegroundColor Green
            Write-Host "Watching for RFID card scans..." -ForegroundColor Cyan
            Write-Host "================================" -ForegroundColor Blue
            
            try {
                $lastOutputLength = 0
                while ($true) {
                    Start-Sleep -Seconds 1
                    $rfidOutput = Receive-Job $rfidJob -Keep
                    
                    if ($rfidOutput -and $rfidOutput.Length -gt $lastOutputLength) {
                        $newLines = $rfidOutput[$lastOutputLength..($rfidOutput.Length - 1)]
                        foreach ($line in $newLines) {
                            if ($line -match "RFID.*Card detected") {
                                Write-Host "🏷️  $line" -ForegroundColor Green
                            } elseif ($line -match "(SUCCESS|DUPLICATE)") {
                                Write-Host "✅ $line" -ForegroundColor Yellow
                            } elseif ($line -match "(UNKNOWN|ERROR)") {
                                Write-Host "❌ $line" -ForegroundColor Red
                            } elseif ($line -match "(CONNECT|FOUND|LISTEN)") {
                                Write-Host "🔗 $line" -ForegroundColor Cyan
                            } else {
                                Write-Host "$line" -ForegroundColor White
                            }
                        }
                        $lastOutputLength = $rfidOutput.Length
                    }
                }
            }
            catch {
                Write-Host "`nRFID monitoring stopped" -ForegroundColor Yellow
            }
        } else {
            Write-Host "RFID Listener is not running" -ForegroundColor Red
        }
    } 
    else {
        Write-Host "Services are running... (q=quit, s=status, l=logs, r=rfid)" -ForegroundColor Green
    }
} while ($true)