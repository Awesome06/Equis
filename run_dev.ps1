# run_dev.ps1 - Equis Project Runtime Script

Write-Host "--- Starting Equis Project (Development Mode) ---" -ForegroundColor Cyan

# 1. Start Backend in a new window
Write-Host "Launching Backend (FastAPI)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; . .\.venv\Scripts\activate; uvicorn app.main:app --reload" -WindowStyle Normal

# 2. Start Frontend in a new window
Write-Host "Launching Frontend (Next.js)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev" -WindowStyle Normal

Write-Host "`n--- Both servers are starting in separate windows! ---" -ForegroundColor Green
Write-Host "Backend: http://localhost:8000"
Write-Host "Frontend: http://localhost:3000"
