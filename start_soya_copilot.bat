@echo off
echo Starting Soya Copilot System...
echo.

REM Check if virtual environment exists and activate it
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

echo Starting backend server on port 8000...
start "Soya Copilot API" cmd /k "python main.py"

REM Wait a moment for the server to start
timeout /t 5 /nobreak >nul

echo Starting frontend on port 8501...
start "Soya Copilot Frontend" cmd /k "streamlit run frontend/streamlit/app.py"

echo.
echo ✅ Soya Copilot is starting up!
echo.
echo 🌐 Backend API: http://localhost:8000
echo 🖥️  Frontend UI: http://localhost:8501
echo 📱 WhatsApp Bot: Run 'python frontend/whatsapp/whatsapp_bot.py' for port 5000
echo.
echo Press any key to exit this launcher...
pause >nul