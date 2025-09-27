# AttenSync - Working RFID Tag Display ACE Command
Write-Host "🎯 AttenSync ACE - RFID TAG MONITOR" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Blue

# Activate environment
& ".\.venv\Scripts\Activate.ps1"

Write-Host "✅ Virtual environment activated" -ForegroundColor Green
Write-Host "🚀 Starting all services..." -ForegroundColor Cyan

# Start backend and frontend in background
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$pwd'; .\.venv\Scripts\Activate.ps1; cd src\backend; python backend.py" -WindowStyle Minimized
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$pwd'; cd src\frontend; npm start" -WindowStyle Minimized

Write-Host "✅ Backend and Frontend started in background" -ForegroundColor Green
Write-Host "Backend: http://localhost:5000" -ForegroundColor White  
Write-Host "Frontend: http://localhost:3000" -ForegroundColor White

Write-Host "`n🏷️ RFID LIVE MONITOR - Real-time tag detection" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to quit all services" -ForegroundColor Gray
Write-Host "============================================" -ForegroundColor Blue

# Run RFID system directly with live output
while ($true) {
    Write-Host "`n🔄 Starting RFID system..." -ForegroundColor Cyan
    
    try {
        # Run RFID system and capture output in real-time
        $process = Start-Process -FilePath "python" -ArgumentList ".\src\hardware\rfid_system.py" -PassThru -NoNewWindow
        
        # Monitor the process
        while (-not $process.HasExited) {
            Start-Sleep -Seconds 1
        }
        
        Write-Host "⚠️ RFID system stopped. Restarting in 5 seconds..." -ForegroundColor Yellow
        Start-Sleep -Seconds 5
        
    } catch {
        Write-Host "❌ Error starting RFID system: $($_.Exception.Message)" -ForegroundColor Red
        Start-Sleep -Seconds 5
    }
}