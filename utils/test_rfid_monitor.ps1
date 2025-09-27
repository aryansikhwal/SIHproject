# Simple RFID Monitor Test
Write-Host "🎯 Testing RFID Tag Display" -ForegroundColor Green

# Activate virtual environment
& ".\.venv\Scripts\Activate.ps1"

# Start RFID system and monitor output directly
Write-Host "Starting RFID system..." -ForegroundColor Cyan

$rfidJob = Start-Job -ScriptBlock {
    param($projectRoot)
    Set-Location "$projectRoot"
    & "$projectRoot\.venv\Scripts\Activate.ps1"
    Set-Location "$projectRoot\src\hardware"
    python rfid_system.py
} -ArgumentList (Get-Location)

Write-Host "✅ RFID started - monitoring for tags..." -ForegroundColor Green
Write-Host "Press 'q' to quit" -ForegroundColor Yellow

while ($true) {
    Start-Sleep -Seconds 1
    
    # Check for quit
    if ([Console]::KeyAvailable) {
        $key = [Console]::ReadKey($true)
        if ($key.KeyChar -eq 'q') {
            Stop-Job $rfidJob
            Remove-Job $rfidJob
            Write-Host "`nStopped RFID monitor" -ForegroundColor Yellow
            break
        }
    }
    
    # Get all output
    $output = Receive-Job $rfidJob -Keep
    if ($output) {
        $lastLine = $output | Select-Object -Last 1
        if ($lastLine) {
            $timestamp = Get-Date -Format "HH:mm:ss"
            
            if ($lastLine -like "*Card detected*") {
                Write-Host "[$timestamp] 🏷️ RFID TAG SCANNED!" -ForegroundColor Green -BackgroundColor DarkGreen
                Write-Host "  $lastLine" -ForegroundColor White
                Write-Host ""
            } elseif ($lastLine -like "*DUPLICATE*") {
                Write-Host "[$timestamp] ⚠️ DUPLICATE SCAN" -ForegroundColor Yellow
                Write-Host "  $lastLine" -ForegroundColor White
                Write-Host ""
            } elseif ($lastLine -like "*SUCCESS*") {
                Write-Host "[$timestamp] ✅ ATTENDANCE MARKED" -ForegroundColor Cyan
                Write-Host "  $lastLine" -ForegroundColor White
                Write-Host ""
            } elseif ($lastLine -like "*Connected*ESP32*") {
                Write-Host "[$timestamp] 🔗 ESP32 Connected" -ForegroundColor Cyan
            } elseif ($lastLine -like "*FOUND*ESP32*") {
                Write-Host "[$timestamp] 📡 ESP32 Found" -ForegroundColor Green
            }
        }
    }
}