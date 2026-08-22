# Start GlobeTrotter Application
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  Starting GlobeTrotter Travel Planning Platform" -ForegroundColor Cyan
Write-Host "  Powered by Flask & PostgreSQL" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host "`n[1/2] Initializing PostgreSQL database..." -ForegroundColor Yellow
& "$ScriptDir\.venv\Scripts\python.exe" run.py --init-db

Write-Host "`n[2/2] Launching Flask server on http://localhost:5000 ..." -ForegroundColor Green
Start-Process "http://localhost:5000"
& "$ScriptDir\.venv\Scripts\python.exe" run.py
