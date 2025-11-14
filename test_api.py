"""Test script for Soya Copilot API."""
import requests
import json
import sys

API_URL = "http://localhost:8000"


def test_health():
    """Test health endpoint."""
    print("\n🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed")
            print(f"   Status: {data.get('status')}")
            print(f"   Orchestrator ready: {data.get('orchestrator_ready')}")
            print(f"   Groq configured: {data.get('config', {}).get('groq_configured')}")
            print(f"   Weather configured: {data.get('config', {}).get('weather_configured')}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure it's running on port 8000")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_chat():
    """Test chat endpoint."""
    print("\n🔍 Testing chat endpoint...")
    try:
        payload = {
            "message": "What is the best time to plant soybeans?",
            "latitude": 0.0,
            "longitude": 0.0
        }
        
        response = requests.post(f"{API_URL}/chat", data=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Chat test passed")
                print(f"   Response preview: {data.get('response', '')[:100]}...")
                return True
            else:
                print(f"❌ Chat failed: {data.get('message')}")
                return False
        else:
            print(f"❌ Chat test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_location():
    """Test location analysis."""
    print("\n🔍 Testing location analysis...")
    try:
        payload = {
            "message": "Is this location suitable for soybeans?",
            "latitude": -13.9626,
            "longitude": 33.7741
        }
        
        response = requests.post(f"{API_URL}/chat", data=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Location analysis test passed")
                print(f"   Response preview: {data.get('response', '')[:100]}...")
                return True
            else:
                print(f"❌ Location analysis failed: {data.get('message')}")
                return False
        else:
            print(f"❌ Location test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False





def main():
    """Run all tests."""
    print("=" * 60)
    print("🌱 Soya Copilot API Test Suite")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Health Check", test_health()))
    results.append(("Chat", test_chat()))
    results.append(("Location Analysis", test_location()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
