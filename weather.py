import aiohttp
from flask import jsonify

# Helper function to get coordinates from Nominatim
async def get_coordinates(city):
    location_url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json&limit=1"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(location_url) as response:
            location_response = await response.json()
            session.close()

    if not location_response:
        return None, None  # Handle location not found

    lat = location_response[0]['lat']
    lon = location_response[0]['lon']
    return lat, lon

async def get_weather(location):
    if location == 'boston':
        lat, lon = 42.361145, -71.057083
    else:
        lat, lon = await get_coordinates(location)

    if lat is None or lon is None:
        return jsonify({'error': 'Location not found'}), 404

    # Fetch weather data from Open-Meteo
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,weather_code,surface_pressure,wind_speed_10m,wind_direction_10m&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset,uv_index_max&timezone=America%2FNew_York"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(weather_url) as response:
            weather_response = await response.json()
            session.close()
            return weather_response

def celcius_to_fahrenheit(celcius):
    if isinstance(celcius, list):
        return [round(c * 9/5 + 32, 1) for c in celcius]
    else:
        return round(celcius * 9/5 + 32, 1)