from geopy.geocoders import Nominatim
import requests
import os


class GeoAnalyzer:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="soya_copilot")

    def get_location_data(self, lat, lon):
        try:
            location = self.geolocator.reverse(f"{lat}, {lon}")
            return location.raw if location else {}
        except:
            return {}

    def get_weather_data(self, lat, lon):
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            return {"error": "OpenWeather API key not configured"}
        
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
            response = requests.get(url)
            return response.json() if response.status_code == 200 else {}
        except:
            return {}

    def analyze_soybean_suitability(self, lat, lon):
        weather_data = self.get_weather_data(lat, lon)
        location_data = self.get_location_data(lat, lon)
        return self.assess_suitability(weather_data, location_data)

    def assess_suitability(self, weather_data, location_data):
        if not weather_data or 'main' not in weather_data:
            return {
                'suitable': False,
                'reason': 'Weather data unavailable',
                'recommendations': ['Check your internet connection and try again']
            }
        
        try:
            temp_kelvin = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
            rainfall = weather_data.get('rain', {}).get('1h', 0)
            temp_celsius = temp_kelvin - 273.15
            
            # Soybean suitability criteria
            temp_suitable = 20 <= temp_celsius <= 30
            humidity_suitable = 40 <= humidity <= 80
            
            recommendations = []
            if temp_suitable:
                recommendations.append("Temperature is ideal for soybean growth")
            else:
                recommendations.append(f"Temperature ({temp_celsius:.1f}°C) is outside ideal range (20-30°C)")
            
            if humidity_suitable:
                recommendations.append("Humidity levels are suitable")
            else:
                recommendations.append(f"Humidity ({humidity}%) may affect soybean growth")
            
            suitable = temp_suitable and humidity_suitable
            
            return {
                'suitable': suitable,
                'temperature': temp_celsius,
                'humidity': humidity,
                'rainfall': rainfall,
                'recommendations': recommendations,
                'location_info': location_data.get('display_name', 'Unknown location')
            }
        except Exception as e:
            return {
                'suitable': False,
                'reason': f'Analysis error: {str(e)}',
                'recommendations': ['Unable to analyze climate conditions']
            }
