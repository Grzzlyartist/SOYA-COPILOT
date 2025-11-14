@echo off
echo Starting Soya Copilot Frontend...
echo.

REM Check if virtual environment exists and activate it
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

echo Starting Streamlit frontend...
streamlit run frontend/streamlit/app.py

pause