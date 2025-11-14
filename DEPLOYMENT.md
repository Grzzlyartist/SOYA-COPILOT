# 🚀 Soya Copilot Deployment Guide

This guide covers deploying Soya Copilot in production environments.

## 📋 Prerequisites

### System Requirements
- **OS**: Linux (Ubuntu 20.04+), Windows 10+, or macOS
- **RAM**: Minimum 4GB, Recommended 8GB+
- **Storage**: 10GB+ free space
- **Network**: Internet connection for API services

### Software Requirements
- **Docker** & **Docker Compose** (Recommended)
- **Python 3.11+** (Alternative deployment)
- **Git** (for cloning repository)

## 🐳 Docker Deployment (Recommended)

### Quick Start
```bash
# Clone repository
git clone <repository-url>
cd soya-copilot

# Copy environment file
cp production.env.example .env
# Edit .env with your API keys

# Deploy with one command
./deploy.sh  # Linux/Mac
# OR
deploy.bat   # Windows
```

### Manual Docker Deployment
```bash
# 1. Build containers
docker-compose build

# 2. Start services
docker-compose up -d

# 3. Check health
python health_check.py
```

### Docker Services
- **soya-copilot-api**: Main API backend (Port 8000)
- **soya-copilot-frontend**: Streamlit UI (Port 8501)
- **soya-copilot-whatsapp**: WhatsApp bot (Port 5000)

## 🔧 Manual Deployment

### 1. Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements-production.txt
```

### 2. Configuration
```bash
# Copy environment file
cp production.env.example .env
# Edit .env with your configuration
```

### 3. Start Services
```bash
# Start API (Production)
gunicorn -c gunicorn.conf.py main:app

# Start Frontend
streamlit run frontend/streamlit/app.py --server.port 8501

# Start WhatsApp Bot
python frontend/whatsapp/whatsapp_bot.py
```

## 🔑 Environment Configuration

### Required API Keys
```bash
# Get from https://console.groq.com
GROQ_API_KEY=your_groq_api_key

# Get from https://openweathermap.org/api
OPENWEATHER_API_KEY=your_openweather_key

# Get from https://console.twilio.com (for WhatsApp)
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=your_whatsapp_number
```

### Production Settings
```bash
ENVIRONMENT=production
LOG_LEVEL=INFO
WORKERS=4
SECRET_KEY=generate_secure_random_string
```

## 🌐 Reverse Proxy Setup (Nginx)

### Nginx Configuration
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # API Backend
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Frontend
    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support for Streamlit
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # WhatsApp Webhook
    location /whatsapp {
        proxy_pass http://localhost:5000/whatsapp;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 📊 Monitoring & Logging

### Health Checks
```bash
# Check all services
python health_check.py

# Check individual services
curl http://localhost:8000/health
curl http://localhost:5000/health
```

### Logs
```bash
# Docker logs
docker-compose logs -f

# Individual service logs
docker-compose logs -f soya-copilot-api
docker-compose logs -f soya-copilot-frontend
docker-compose logs -f soya-copilot-whatsapp

# File logs (manual deployment)
tail -f logs/access.log
tail -f logs/error.log
```

## 🔒 Security Considerations

### API Security
- Use HTTPS in production
- Set strong SECRET_KEY and JWT_SECRET
- Implement rate limiting
- Use environment variables for secrets

### Network Security
- Configure firewall rules
- Use VPN for admin access
- Regular security updates

### Data Security
- Backup knowledge base regularly
- Encrypt sensitive data
- Monitor access logs

## 🚀 Scaling

### Horizontal Scaling
```yaml
# docker-compose.yml
services:
  soya-copilot-api:
    deploy:
      replicas: 3
    # ... other config
```

### Load Balancing
- Use Nginx or HAProxy
- Configure health checks
- Session affinity for Streamlit

### Database Scaling
- Use external PostgreSQL for production
- Configure connection pooling
- Regular backups

## 🛠️ Maintenance

### Updates
```bash
# Pull latest code
git pull origin main

# Rebuild containers
docker-compose build

# Rolling update
docker-compose up -d
```

### Backups
```bash
# Backup data directory
tar -czf backup-$(date +%Y%m%d).tar.gz data/

# Backup database (if using external DB)
pg_dump soya_copilot > backup-$(date +%Y%m%d).sql
```

### Performance Tuning
- Monitor resource usage
- Adjust worker counts
- Optimize knowledge base size
- Cache frequently accessed data

## 🆘 Troubleshooting

### Common Issues

**Service won't start**
```bash
# Check logs
docker-compose logs service-name

# Check environment variables
docker-compose config

# Restart service
docker-compose restart service-name
```

**API not responding**
```bash
# Check health endpoint
curl http://localhost:8000/health

# Check worker processes
ps aux | grep gunicorn

# Check port availability
netstat -tlnp | grep 8000
```

**WhatsApp webhook issues**
```bash
# Test webhook locally
curl -X POST http://localhost:5000/whatsapp \
  -d "Body=test message" \
  -d "From=whatsapp:+1234567890"

# Check Twilio configuration
# Verify webhook URL in Twilio console
```

### Performance Issues
- Increase worker count
- Add more memory
- Optimize knowledge base
- Use caching

### Getting Help
- Check logs first
- Run health checks
- Review configuration
- Open GitHub issue with logs

## 📈 Production Checklist

- [ ] Environment variables configured
- [ ] API keys obtained and tested
- [ ] SSL certificates installed
- [ ] Reverse proxy configured
- [ ] Monitoring setup
- [ ] Backup strategy implemented
- [ ] Security measures in place
- [ ] Health checks passing
- [ ] Load testing completed
- [ ] Documentation updated