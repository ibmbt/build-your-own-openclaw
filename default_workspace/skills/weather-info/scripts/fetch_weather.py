# skills/weather-info/scripts/fetch_weather.py
import urllib.request
import json
import sys

def get_weather(city):
    # Hardcoded coordinates for simplicity
    coords = {
        "lahore": {"lat": 31.5497, "lon": 74.3436},
        "london": {"lat": 51.5074, "lon": -0.1278}
    }
    
    city_clean = city.lower().strip()
    geo = coords.get(city_clean, {"lat": 31.5497, "lon": 74.3436})
    
    url = f"https://api.open-meteo.com/v1/forecast?latitude={geo['lat']}&longitude={geo['lon']}&current_weather=true"
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            current = data["current_weather"]
            print(f"{city.title()} Weather: {current['temperature']}°C, Wind: {current['windspeed']}km/h")
    except Exception as e:
        print(f"Error fetching weather: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        get_weather(sys.argv[1])
    else:
        print("Please provide a city name.")
