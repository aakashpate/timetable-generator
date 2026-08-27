@echo off
echo ================================
echo  Timetable Generator Setup
echo ================================
echo.

echo [1/4] Installing Python dependencies...
pip install -r backend\requirements.txt

echo [2/4] Setting up database...
cd backend
python -c "from database.connection import engine, Base; from models.models import *; Base.metadata.create_all(bind=engine); print('Tables created!')"
python -c "from database.seed import seed_db; seed_db()"
cd ..

echo [3/4] Installing frontend dependencies...
cd frontend
call npm install
cd ..

echo.
echo ================================
echo  Setup Complete!
echo ================================
echo.
echo To start the app:
echo   1. Backend:  cd backend ^& python -m uvicorn main:app --reload
echo   2. Frontend: cd frontend ^& npm run dev
echo.
echo Open http://localhost:5173
echo.
pause
