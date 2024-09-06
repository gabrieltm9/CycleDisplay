from flask import Flask, render_template, jsonify
import aiohttp
import asyncio

app = Flask(__name__)

# Get weather data from Open-Meteo for hardcoded locations
@app.route('/weather/<location>')
async def get_weather(location):
    lat, lon = await get_coordinates(location)
    if lat is None or lon is None:
        return jsonify({'error': 'Location not found'}), 404

    # Fetch weather data from Open-Meteo
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,weather_code,surface_pressure,wind_speed_10m,wind_direction_10m&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset,uv_index_max&timezone=America%2FNew_York"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(weather_url) as response:
            weather_response = await response.json()

    # Pass location name and weather data to the template, including weather codes
    return render_template('weather.html', location=location.capitalize(), weather=weather_response)

# Helper function to get coordinates from Nominatim
async def get_coordinates(city):
    location_url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json&limit=1"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(location_url) as response:
            location_response = await response.json()

    if not location_response:
        return None, None  # Handle location not found

    lat = location_response[0]['lat']
    lon = location_response[0]['lon']
    return lat, lon

# Updated index route to handle asynchronous call
@app.route('/')
def index():
    # Call async function synchronously using asyncio.run
    return asyncio.run(get_weather('boston'))

@app.route('/weather')
def weather():
    # Call async function synchronously using asyncio.run
    return asyncio.run(get_weather('boston'))

@app.route('/stocks')
def stocks():
    return render_template('stocks.html')

@app.route('/news')
def news():
    return render_template('news.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
