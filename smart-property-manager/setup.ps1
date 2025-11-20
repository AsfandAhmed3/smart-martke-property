# Setup Script for Smart Property Manager
# Run this script to set up the database and create a superadmin user

Write-Host "=== Smart Property Manager Setup ===" -ForegroundColor Cyan
Write-Host ""

# Navigate to backend directory
Set-Location -Path "backend"

# Check if .env exists
if (-Not (Test-Path ".env")) {
    Write-Host "Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host ""
    Write-Host "⚠️  IMPORTANT: Edit backend/.env and add your Supabase credentials!" -ForegroundColor Red
    Write-Host "   - DB_USER" -ForegroundColor Yellow
    Write-Host "   - DB_PASSWORD" -ForegroundColor Yellow
    Write-Host "   - DB_HOST" -ForegroundColor Yellow
    Write-Host ""
    $continue = Read-Host "Press Enter after updating .env file, or Ctrl+C to exit"
}

# Check if virtual environment exists
if (-Not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Install requirements
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Run migrations
Write-Host "Running database migrations..." -ForegroundColor Yellow
python manage.py makemigrations
python manage.py migrate

# Create superadmin
Write-Host ""
Write-Host "=== Creating Superadmin User ===" -ForegroundColor Cyan
Write-Host ""
$email = Read-Host "Enter superadmin email (default: admin@smartproperty.com)"
if ([string]::IsNullOrWhiteSpace($email)) {
    $email = "admin@smartproperty.com"
}

$password = Read-Host "Enter superadmin password (default: admin123456)" -AsSecureString
$passwordPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($password))
if ([string]::IsNullOrWhiteSpace($passwordPlain)) {
    $passwordPlain = "admin123456"
}

$firstName = Read-Host "Enter first name (default: Super)"
if ([string]::IsNullOrWhiteSpace($firstName)) {
    $firstName = "Super"
}

$lastName = Read-Host "Enter last name (default: Admin)"
if ([string]::IsNullOrWhiteSpace($lastName)) {
    $lastName = "Admin"
}

python manage.py create_superadmin --email="$email" --password="$passwordPlain" --first-name="$firstName" --last-name="$lastName"

Write-Host ""
Write-Host "=== Setup Complete! ===" -ForegroundColor Green
Write-Host ""
Write-Host "To start the backend server, run:" -ForegroundColor Cyan
Write-Host "  cd backend" -ForegroundColor Yellow
Write-Host "  python manage.py runserver" -ForegroundColor Yellow
Write-Host ""
Write-Host "To start the frontend, run in a new terminal:" -ForegroundColor Cyan
Write-Host "  cd frontend" -ForegroundColor Yellow
Write-Host "  npm install" -ForegroundColor Yellow
Write-Host "  npm run dev" -ForegroundColor Yellow
Write-Host ""
