# AttenSync - Enhanced ACE COMMAND 🎯
# ALWAYS runs everything in virtual environment with RFID monitoring

param(
    [switch]$SkipDeps = $false,
    [switch]$NoRFID = $false
)

$ErrorActionPreference = "Continue"
$Host.UI.RawUI.WindowTitle = "AttenSync - ACE COMMAND"                            } elseif ($line -like "*FOUND*ESP32*") {
                                Write-Host "📡 ESP32 Device Found" -ForegroundColor Green
                            } elseif ($line -like "*ERROR*") {
                                Write-Host "❌ ERROR: $line" -ForegroundColor Red
                            }
                        }
                    }
                } catch {
                    Write-Host "❌ Error reading RFID output: $($_.Exception.Message)" -ForegroundColor Red
                }
            }
        } else {
            Write-Host "❌ RFID system not running" -ForegroundColor Red
        }
    }
    else {
        Write-Host "🎯 ACE services running... (q/s/l/r)" -ForegroundColor Green
    }
} while ($true)ot FIRST
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
Set-Location $ProjectRoot

# CRITICAL: FORCE VIRTUAL ENVIRONMENT ACTIVATION IMMEDIATELY
$venvPath = Join-Path $ProjectRoot ".venv"
$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"

# CHECK IF WE'RE ALREADY IN VENV
if (-not $env:VIRTUAL_ENV) {
    Write-Host "🔄 FORCING Virtual Environment Activation..." -ForegroundColor Red
    if (Test-Path $activateScript) {
        # Execute this script INSIDE the virtual environment
        $scriptPath = $MyInvocation.MyCommand.Path
        $arguments = if ($SkipDeps) { "-SkipDeps" } else { "" }
        $arguments += if ($NoRFID) { " -NoRFID" } else { "" }
        
        Write-Host "⚡ Restarting ACE command INSIDE virtual environment..." -ForegroundColor Yellow
        & $activateScript
        & powershell -NoExit -Command "& '$scriptPath' $arguments"
        exit
    } else {
        Write-Host "❌ Virtual environment not found! Creating..." -ForegroundColor Red
        python -m venv .venv
        Write-Host "⚡ Restarting ACE command INSIDE virtual environment..." -ForegroundColor Yellow
        & $activateScript
        & powershell -NoExit -Command "& '$MyInvocation.MyCommand.Path'"
        exit
    }
}

Write-Host "🎯 AttenSync ACE COMMAND 🎯" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Blue
Write-Host "✅ RUNNING INSIDE VIRTUAL ENVIRONMENT" -ForegroundColor Green
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
    Write-Host "Python not found!" -ForegroundColor Red
    $prereqs = $false
} else {
    Write-Host "Python found" -ForegroundColor Green
}

if (-not (Test-Command "node")) {
    Write-Host "Node.js not found!" -ForegroundColor Red
    $prereqs = $false
} else {
    Write-Host "Node.js found" -ForegroundColor Green
}

if (-not $prereqs) {
    Write-Host "`nPrerequisites missing!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check virtual environment
Write-Host "`nChecking Virtual Environment..." -ForegroundColor Yellow
if (-not (Test-Path $venvPath)) {
    Write-Host "Virtual environment not found!" -ForegroundColor Red
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
    & $activateScript
}

# Install dependencies in virtual environment ONLY if needed
if (-not $SkipDeps) {
    # Quick check if main dependencies exist
    try {
        python -c "import flask, bleak" 2>$null | Out-Null
        Write-Host "✅ Dependencies already installed!" -ForegroundColor Green
    } catch {
        Write-Host "Installing missing dependencies in virtual environment..." -ForegroundColor Yellow
        pip install -r requirements.txt --quiet
        
        Set-Location "src\frontend"
        npm install --silent
        Set-Location $ProjectRoot
        
        Write-Host "Dependencies installed!" -ForegroundColor Green
    }
}

Write-Host "`n🚀 Starting AttenSync Components..." -ForegroundColor Green

# Array to store background jobs
$jobs = @()

# Start Backend Server in virtual environment
Write-Host "Starting Backend Server..." -ForegroundColor Cyan
$backendJob = Start-Job -ScriptBlock {
    param($projectRoot)
    Set-Location "$projectRoot"
    & "$projectRoot\.venv\Scripts\Activate.ps1"
    Set-Location "$projectRoot\src\backend"
    python backend.py
} -ArgumentList $ProjectRoot
$jobs += $backendJob
Write-Host "✅ Backend started (Job ID: $($backendJob.Id))" -ForegroundColor Green

Start-Sleep -Seconds 3

# Start Frontend Server
Write-Host "Starting Frontend Server..." -ForegroundColor Cyan
$frontendJob = Start-Job -ScriptBlock {
    param($projectRoot)
    Set-Location "$projectRoot\src\frontend"
    $env:BROWSER = "none"
    npm start
} -ArgumentList $ProjectRoot
$jobs += $frontendJob
Write-Host "✅ Frontend started (Job ID: $($frontendJob.Id))" -ForegroundColor Green

# Start RFID System in virtual environment
$rfidJob = $null
if (-not $NoRFID) {
    Write-Host "Starting RFID System..." -ForegroundColor Cyan
    
    # Test dependencies in activated environment (we're already inside venv)
    try {
        python -c "import bleak, flask_login; print('OK')" 2>$null | Out-Null
        $rfidTest = "OK"
    } catch {
        $rfidTest = "MISSING"
    }
    
    if ($rfidTest -eq "OK") {
        $rfidJob = Start-Job -ScriptBlock {
            param($projectRoot)
            Set-Location "$projectRoot"
            & "$projectRoot\.venv\Scripts\Activate.ps1"
            Set-Location "$projectRoot\src\hardware"
            python rfid_system.py
        } -ArgumentList $ProjectRoot
        $jobs += $rfidJob
        Write-Host "✅ RFID Listener started (Job ID: $($rfidJob.Id))" -ForegroundColor Green
    } else {
        Write-Host "⚠️  RFID dependencies missing - install with:" -ForegroundColor Yellow
        Write-Host "   pip install bleak pyserial flask flask-login" -ForegroundColor Gray
    }
}

# Display running services
Write-Host "`n🎯 AttenSync Services Active:" -ForegroundColor Green
Write-Host "   Backend API:    http://localhost:5000" -ForegroundColor White
Write-Host "   Frontend Web:   http://localhost:3000" -ForegroundColor White
Write-Host "   API Health:     http://localhost:5000/api/health" -ForegroundColor White
if ($rfidJob) {
    Write-Host "   RFID Listener:  Active & Monitoring" -ForegroundColor White
} else {
    Write-Host "   RFID Listener:  Not started" -ForegroundColor Gray
}

Write-Host "`nCommands:" -ForegroundColor Yellow
Write-Host "   q = quit all services" -ForegroundColor Gray
Write-Host "   s = show status" -ForegroundColor Gray
Write-Host "   l = show logs" -ForegroundColor Gray
Write-Host "   r = RFID real-time monitor" -ForegroundColor Gray

# Management loop
do {
    $input = Read-Host "`nACE Manager"
    
    if ($input.ToLower() -eq "q") {
        Write-Host "`nStopping all services..." -ForegroundColor Yellow
        foreach ($job in $jobs) {
            Stop-Job $job -PassThru | Remove-Job
        }
        Write-Host "🎯 ACE COMMAND stopped. Goodbye!" -ForegroundColor Green
        break
    } 
    elseif ($input.ToLower() -eq "s") {
        Write-Host "`nService Status:" -ForegroundColor Cyan
        foreach ($job in $jobs) {
            $status = Get-Job $job
            $jobName = switch ($job.Id) {
                $backendJob.Id { "Backend" }
                $frontendJob.Id { "Frontend" }
                { $rfidJob -and $_ -eq $rfidJob.Id } { "RFID" }
                default { "Unknown" }
            }
            Write-Host "   $jobName (Job $($job.Id)): $($status.State)" -ForegroundColor White
        }
    }
    elseif ($input.ToLower() -eq "l") {
        Write-Host "`nRecent Logs:" -ForegroundColor Cyan
        foreach ($job in $jobs) {
            $jobName = switch ($job.Id) {
                $backendJob.Id { "Backend" }
                $frontendJob.Id { "Frontend" }
                { $rfidJob -and $_ -eq $rfidJob.Id } { "RFID" }
                default { "Unknown" }
            }
            Write-Host "--- $jobName ---" -ForegroundColor Yellow
            try {
                $output = Receive-Job $job -Keep | Select-Object -Last 5
                if ($output) {
                    $output | ForEach-Object { Write-Host "   $_" }
                } else {
                    Write-Host "   No output available" -ForegroundColor Gray
                }
            }
            catch {
                Write-Host "   Error reading logs: $_" -ForegroundColor Red
            }
        }
    }
    elseif ($input.ToLower() -eq "r") {
        if ($rfidJob) {
            Write-Host "`n🎯 RFID Real-Time Monitor (Press 'q' to return)" -ForegroundColor Green
            Write-Host "Watching for card scans..." -ForegroundColor Cyan
            Write-Host "===========================================" -ForegroundColor Blue
            
            $lastOutputCount = 0
            while ($true) {
                Start-Sleep -Seconds 1
                
                # Check if user wants to quit
                if ([Console]::KeyAvailable) {
                    $key = [Console]::ReadKey($true)
                    if ($key.KeyChar -eq 'q') {
                        Write-Host "`nReturning to main menu..." -ForegroundColor Yellow
                        break
                    }
                }
                
                # Get new RFID output
                try {
                    $allOutput = Receive-Job $rfidJob -Keep -ErrorAction SilentlyContinue
                    if ($allOutput -and $allOutput.Count -gt $lastOutputCount) {
                        $newLines = $allOutput | Select-Object -Skip $lastOutputCount
                        $lastOutputCount = $allOutput.Count
                        
                        foreach ($line in $newLines) {
                            # Debug: Show all lines to see what we're getting
                            Write-Host "[DEBUG] $line" -ForegroundColor DarkGray
                            
                            if ($line -like "*Card detected*") {
                                Write-Host "🏷️  RFID TAG DETECTED!" -ForegroundColor Green -BackgroundColor DarkGreen
                                Write-Host "   $line" -ForegroundColor White
                            } elseif ($line -like "*DUPLICATE*") {
                                Write-Host "⚠️  DUPLICATE SCAN" -ForegroundColor Yellow
                                Write-Host "   $line" -ForegroundColor White
                            } elseif ($line -like "*SUCCESS*") {
                                Write-Host "✅ ATTENDANCE MARKED" -ForegroundColor Yellow  
                                Write-Host "   $line" -ForegroundColor White
                            } elseif ($line -like "*Connected*ESP32*") {
                                Write-Host "🔗 ESP32 Connected" -ForegroundColor Cyan
                            } elseif ($line -like "*SCAN*") {
                                Write-Host "� Scanning..." -ForegroundColor Gray
                            } elseif ($line -like "*FOUND*ESP32*") {
                                Write-Host "� ESP32 Device Found" -ForegroundColor Green
                            } elseif ($line -like "*ERROR*") {
                                Write-Host "❌ ERROR: $line" -ForegroundColor Red
                            }
                        }
                    }
                } catch {
                    Write-Host "❌ Error reading RFID output: $($_.Exception.Message)" -ForegroundColor Red
                }
            }
        } else {
            Write-Host "❌ RFID system not running" -ForegroundColor Red
        }
    }
    else {
        Write-Host "🎯 ACE services running... (q/s/l/r)" -ForegroundColor Green
    }
} while ($true)