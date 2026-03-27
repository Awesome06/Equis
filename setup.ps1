# setup.ps1 - Equis Project Setup Script

Write-Host "--- Setting up Equis Project ---" -ForegroundColor Cyan

# 1. Backend Setup
Write-Host "`n[1/2] Setting up Backend..." -ForegroundColor Yellow
cd backend

if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv .venv
}

Write-Host "Installing backend dependencies..."
.\.venv\Scripts\python -m pip install -r requirements.txt

if (-not (Test-Path ".env")) {
    Write-Host "Creating .env from .env.example..."
    Copy-Item .env.example .env
}

cd ..

# 2. Frontend Setup
Write-Host "`n[2/2] Setting up Frontend..." -ForegroundColor Yellow
cd frontend

Write-Host "Installing frontend dependencies..."
npm install --legacy-peer-deps

cd ..

Write-Host "`n--- Setup Complete! ---" -ForegroundColor Green
Write-Host "You can now run the project using: ./run_dev.ps1"
