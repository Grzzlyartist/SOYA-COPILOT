#!/usr/bin/env python3
"""
Health check script for Soya Copilot deployment
"""

import requests
import sys
import time
import os
from dotenv import load_dotenv

load_dotenv()

def check_service(name, url, timeout=10):
    """Check if a service is healthy"""
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            print(f"✅ {name}: Healthy")
            return True
        else:
            print(f"❌ {name}: Unhealthy (Status: {response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ {name}: Unreachable ({str(e)})")
        return False

def main():
    """Run health checks on all services"""
    print("🏥 Soya Copilot Health Check")
    print("=" * 40)
    
    services = [
        ("API Backend", "http://localhost:8000/health"),
        ("Frontend", "http://localhost:8501"),
        ("WhatsApp Bot", "http://localhost:5000/health"),
    ]
    
    all_healthy = True
    
    for name, url in services:
        if not check_service(name, url):
            all_healthy = False
    
    print("\n" + "=" * 40)
    
    if all_healthy:
        print("🎉 All services are healthy!")
        return 0
    else:
        print("⚠️  Some services are unhealthy!")
        return 1

if __name__ == "__main__":
    sys.exit(main())