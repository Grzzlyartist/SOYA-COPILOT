@echo off
REM Soya Copilot Deployment Script for Windows

echo 🌱 Deploying Soya Copilot...

REM Check if .env file exists
if not exist .env (
    echo ❌ .env file not found. Please create it from .env.example
    exit /b 1
)

REM Create necessary directories
echo 📁 Creating directories...
if not exist data\chromadb mkdir data\chromadb
if not exist data\models mkdir data\models
if not exist data\knowledge mkdir data\knowledge
if not exist logs mkdir logs

REM Build and start services
echo 🐳 Building Docker containers...
docker-compose build

if %errorlevel% neq 0 (
    echo ❌ Docker build failed
    exit /b 1
)

echo 🚀 Starting services...
docker-compose up -d

if %errorlevel% neq 0 (
    echo ❌ Failed to start services
    exit /b 1
)

REM Wait for services to be ready
echo ⏳ Waiting for services to start...
timeout /t 10 /nobreak >nul

REM Health check
echo 🏥 Checking service health...
curl -f http://localhost:8000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ API service is healthy
) else (
    echo ❌ API service is not responding
    docker-compose logs soya-copilot-api
    exit /b 1
)

echo 🎉 Deployment completed successfully!
echo.
echo 🌐 Services available at:
echo   • API: http://localhost:8000
echo   • Frontend: http://localhost:8501
echo   • WhatsApp Bot: http://localhost:5000
echo.
echo 📊 To view logs: docker-compose logs -f
echo 🛑 To stop: docker-compose down

pause