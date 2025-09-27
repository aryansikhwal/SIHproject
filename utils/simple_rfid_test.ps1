# Simple RFID Tag Debug Test
Write-Host "🔍 RFID TAG DEBUG TEST" -ForegroundColor Yellow

# Activate environment and run RFID directly
& ".\.venv\Scripts\Activate.ps1"

Write-Host "🚀 Starting RFID system with direct output..." -ForegroundColor Green

# Run RFID system and capture output line by line
$rfidProcess = Start-Process -FilePath "python" -ArgumentList ".\src\hardware\rfid_system.py" -PassThru -RedirectStandardOutput "rfid_output.txt" -RedirectStandardError "rfid_error.txt" -WindowStyle Hidden

Write-Host "✅ RFID process started (PID: $($rfidProcess.Id))" -ForegroundColor Green
Write-Host "🏷️ Monitoring for RFID tags..." -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop" -ForegroundColor Gray

try {
    while (-not $rfidProcess.HasExited) {
        Start-Sleep -Seconds 2
        
        if (Test-Path "rfid_output.txt") {
            $content = Get-Content "rfid_output.txt" -ErrorAction SilentlyContinue
            if ($content) {
                $lastLine = $content | Select-Object -Last 1
                $timestamp = Get-Date -Format "HH:mm:ss"
                
                Write-Host "[$timestamp] $lastLine" -ForegroundColor White
                
                if ($lastLine -like "*Card detected*") {
                    Write-Host "🏷️ RFID TAG DETECTED!" -ForegroundColor Green -BackgroundColor DarkGreen
                    Write-Host ""
                }
                
                if ($lastLine -like "*DUPLICATE*") {
                    Write-Host "⚠️ DUPLICATE SCAN!" -ForegroundColor Yellow
                    Write-Host ""
                }
                
                if ($lastLine -like "*Connected*ESP32*") {
                    Write-Host "🔗 ESP32 Connected!" -ForegroundColor Cyan
                }
            }
        }
        
        Write-Host "." -NoNewline -ForegroundColor DarkGray
    }
} finally {
    if (-not $rfidProcess.HasExited) {
        $rfidProcess.Kill()
    }
    if (Test-Path "rfid_output.txt") { Remove-Item "rfid_output.txt" }
    if (Test-Path "rfid_error.txt") { Remove-Item "rfid_error.txt" }
    Write-Host "`n✅ Cleanup complete" -ForegroundColor Green
}