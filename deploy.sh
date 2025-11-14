#!/bin/bash
# Soya Copilot Deployment Script

set -e

echo "🌱 Deploying Soya Copilot..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please create it from .env.example"
    exit 1
fi

# Check required environment variables
echo "🔧 Checking environment variables..."
source .env

if [ -z "$GROQ_API_KEY" ]; then
    echo "❌ GROQ_API_KEY not set in .env"
    exit 1
fi

if [ -z "$OPENWEATHER_API_KEY" ]; then
    echo "⚠️  OPENWEATHER_API_KEY not set - location analysis will not work"
fi

echo "✅ Environment variables checked"

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data/chromadb data/models data/knowledge logs

# Build and start services
echo "🐳 Building Docker containers..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Health check
echo "🏥 Checking service health..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ API service is healthy"
else
    echo "❌ API service is not responding"
    docker-compose logs soya-copilot-api
    exit 1
fi

echo "🎉 Deployment completed successfully!"
echo ""
echo "🌐 Services available at:"
echo "  • API: http://localhost:8000"
echo "  • Frontend: http://localhost:8501"
echo "  • WhatsApp Bot: http://localhost:5000"
echo ""
echo "📊 To view logs: docker-compose logs -f"
echo "🛑 To stop: docker-compose down"