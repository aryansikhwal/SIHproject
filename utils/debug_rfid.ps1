# Debug RFID Tag Display Test
Write-Host "🔍 DEBUGGING RFID TAG DISPLAY" -ForegroundColor Yellow
Write-Host "=============================" -ForegroundColor Blue

# Activate environment
$ProjectRoot = Get-Location
& ".\.venv\Scripts\Activate.ps1"

Write-Host "✅ Virtual environment activated" -ForegroundColor Green
Write-Host "📍 Project root: $ProjectRoot" -ForegroundColor Cyan

# Test RFID dependencies
Write-Host "`n🧪 Testing RFID dependencies..." -ForegroundColor Yellow
try {
    python -c "import bleak, flask_login, serial; print('✅ All RFID dependencies available')"
} catch {
    Write-Host "❌ RFID dependencies missing!" -ForegroundColor Red
    exit 1
}

# Start RFID system with detailed output
Write-Host "`n🚀 Starting RFID system..." -ForegroundColor Green
$rfidJob = Start-Job -ScriptBlock {
    param($root)
    Set-Location "$root"
    & ".\.venv\Scripts\Activate.ps1"
    Set-Location "$root\src\hardware"
    python rfid_system.py 2>&1  # Capture all output including errors
} -ArgumentList $ProjectRoot

Write-Host "✅ RFID job started (ID: $($rfidJob.Id))" -ForegroundColor Green

# Wait a moment for startup
Write-Host "`n⏳ Waiting for RFID system to initialize..." -ForegroundColor Cyan
Start-Sleep -Seconds 10

# Check job status
$jobState = Get-Job $rfidJob
Write-Host "🔍 RFID Job Status: $($jobState.State)" -ForegroundColor Yellow

# Get initial output
$initialOutput = Receive-Job $rfidJob -Keep
if ($initialOutput) {
    Write-Host "`n📋 RFID System Output:" -ForegroundColor Cyan
    $initialOutput | ForEach-Object { Write-Host "   $_" -ForegroundColor White }
} else {
    Write-Host "❌ No output from RFID system yet" -ForegroundColor Red
}

# Real-time monitoring with detailed debug
Write-Host "`n🏷️ Starting real-time tag monitoring..." -ForegroundColor Green
Write-Host "Press Ctrl+C to stop" -ForegroundColor Gray
Write-Host "===========================================" -ForegroundColor Blue

$outputCount = if ($initialOutput) { $initialOutput.Count } else { 0 }

try {
    while ($true) {
        Start-Sleep -Seconds 2
        
        # Get all output
        $allOutput = Receive-Job $rfidJob -Keep -ErrorAction SilentlyContinue
        
        # Check job status
        $currentState = (Get-Job $rfidJob).State
        if ($currentState -eq "Failed" -or $currentState -eq "Stopped") {
            Write-Host "❌ RFID job failed/stopped! State: $currentState" -ForegroundColor Red
            break
        }
        
        # Show new output
        if ($allOutput -and $allOutput.Count -gt $outputCount) {
            $newLines = $allOutput | Select-Object -Skip $outputCount
            $outputCount = $allOutput.Count
            
            foreach ($line in $newLines) {
                $timestamp = Get-Date -Format "HH:mm:ss"
                Write-Host "[$timestamp] RAW: $line" -ForegroundColor DarkGray
                
                if ($line -like "*Card detected*") {
                    Write-Host "[$timestamp] 🏷️ RFID TAG DETECTED!" -ForegroundColor Green -BackgroundColor DarkGreen
                    Write-Host "    DETAILS: $line" -ForegroundColor White
                    Write-Host ""
                } elseif ($line -like "*DUPLICATE*") {
                    Write-Host "[$timestamp] ⚠️ DUPLICATE SCAN" -ForegroundColor Yellow
                    Write-Host "    DETAILS: $line" -ForegroundColor White
                    Write-Host ""
                } elseif ($line -like "*SUCCESS*" -or $line -like "*marked*") {
                    Write-Host "[$timestamp] ✅ ATTENDANCE MARKED" -ForegroundColor Cyan
                    Write-Host "    DETAILS: $line" -ForegroundColor White
                    Write-Host ""
                } elseif ($line -like "*Connected*ESP32*") {
                    Write-Host "[$timestamp] 🔗 ESP32 Connected" -ForegroundColor Cyan
                } elseif ($line -like "*FOUND*ESP32*") {
                    Write-Host "[$timestamp] 📡 ESP32 Found" -ForegroundColor Green
                } elseif ($line -like "*LISTEN*" -or $line -like "*Listening*") {
                    Write-Host "[$timestamp] 👂 RFID System Ready - Listening for cards" -ForegroundColor Green
                } elseif ($line -like "*ERROR*") {
                    Write-Host "[$timestamp] ❌ ERROR" -ForegroundColor Red
                    Write-Host "    DETAILS: $line" -ForegroundColor White
                }
            }
        } else {
            Write-Host "." -NoNewline -ForegroundColor DarkGray
        }
    }
} finally {
    Write-Host "`n🛑 Cleaning up..." -ForegroundColor Yellow
    Stop-Job $rfidJob -ErrorAction SilentlyContinue
    Remove-Job $rfidJob -ErrorAction SilentlyContinue
    Write-Host "✅ Done" -ForegroundColor Green
}