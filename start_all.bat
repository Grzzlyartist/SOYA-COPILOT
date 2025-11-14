@echo off
echo Starting Soya Copilot Services...
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found. Please run setup first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start FastAPI backend in new window
echo Starting FastAPI Backend on port 8000...
start "Soya Copilot API" cmd /k "python main.py"

REM Wait a moment for API to start
timeout /t 3 /nobreak > nul

REM Start Streamlit in new window
echo Starting Streamlit Web UI on port 8501...
start "Soya Copilot Web UI" cmd /k "streamlit run frontend/streamlit/app.py"

echo.
echo All services started!
echo - API: http://localhost:8000
echo - Web UI: http://localhost:8501
echo.
echo Press any key to exit (services will continue running)...
pause > nul
