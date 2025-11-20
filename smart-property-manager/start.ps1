# Quick Start Script for Smart Property Manager
Write-Host "=== Smart Property Manager Quick Start ===" -ForegroundColor Cyan
Write-Host ""

# Check if migrations have been run
$migrationsNeeded = $true
if (Test-Path "backend\db.sqlite3") {
    Write-Host "Local database detected. Switching to Supabase..." -ForegroundColor Yellow
    $migrationsNeeded = $true
}

if ($migrationsNeeded) {
    Write-Host "Running migrations..." -ForegroundColor Yellow
    Set-Location backend
    
    # Activate venv if exists
    if (Test-Path "venv\Scripts\Activate.ps1") {
        .\venv\Scripts\Activate.ps1
    }
    
    python manage.py makemigrations
    python manage.py migrate
    
    Write-Host ""
    Write-Host "Migrations complete!" -ForegroundColor Green
    Write-Host ""
    
    # Ask about creating superadmin
    $createAdmin = Read-Host "Do you want to create a superadmin user? (Y/N)"
    if ($createAdmin -eq "Y" -or $createAdmin -eq "y") {
        python manage.py create_superadmin
    }
    
    Set-Location ..
}

Write-Host ""
Write-Host "Starting backend server..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; if (Test-Path venv\Scripts\Activate.ps1) { .\venv\Scripts\Activate.ps1 }; python manage.py runserver"

Start-Sleep -Seconds 3

Write-Host "Starting frontend server..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

Write-Host ""
Write-Host "=== Servers Starting ===" -ForegroundColor Green
Write-Host ""
Write-Host "Backend:  http://localhost:8000" -ForegroundColor Yellow
Write-Host "Frontend: http://localhost:5173" -ForegroundColor Yellow
Write-Host ""
Write-Host "Please wait a few seconds for servers to fully start..." -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to exit this window..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
