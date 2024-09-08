import os
from flask import Flask, render_template, send_from_directory
import asyncio
from datetime import datetime
from stocks import get_stock_prices, get_sp500_graph
from weather import get_weather, celcius_to_fahrenheit

app = Flask(__name__)

# Get weather data from Open-Meteo for hardcoded locations
@app.route('/weather/<location>')
async def location_weather(location):
    # Call get_weather function from weather.py
    weather_response = await get_weather(location)

    # Convert celcius to fahrenheit
    weather_response['current']['temperature_2m'] = celcius_to_fahrenheit(weather_response['current']['temperature_2m'])
    weather_response['daily']['temperature_2m_max'] = celcius_to_fahrenheit(weather_response['daily']['temperature_2m_max'])
    weather_response['daily']['temperature_2m_min'] = celcius_to_fahrenheit(weather_response['daily']['temperature_2m_min'])

    # Modify sunrise and sunset to HH:MM format using strftime. First convert to datetime object
    weather_response['daily']['sunrise'][0] = datetime.strptime(weather_response['daily']['sunrise'][0], '%Y-%m-%dT%H:%M').strftime('%H:%M')
    weather_response['daily']['sunset'][0] = datetime.strptime(weather_response['daily']['sunset'][0], '%Y-%m-%dT%H:%M').strftime('%H:%M')
    
    # Modify wind direction to be more human-readable
    wind_directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    weather_response['current']['wind_direction_10m'] = wind_directions[int((weather_response['current']['wind_direction_10m'] + 22.5) / 45) % 8]

    # Pass location name and weather data to the template, including weather codes
    return render_template('weather.html', location=location.capitalize(), weather=weather_response)

@app.route('/')
def index():
    # Call async function synchronously using asyncio.run
    return render_template('index.html')

@app.route('/weather')
def weather():
    # Call async function synchronously using asyncio.run
    return asyncio.run(location_weather('boston'))

@app.route('/stocks')
def stocks():
    stock_symbols = ['AAPL', 'GOOGL', 'AMZN', 'MSFT', 'NVDA', 'IBM', 'TSLA', 'NFLX', 'META']  # stock symbols
    stock_prices = get_stock_prices(stock_symbols)
    sp500_graph = get_sp500_graph()

    return render_template('stocks.html', stock_prices=stock_prices, sp500_graph=sp500_graph)

@app.route('/news')
def news():
    return render_template('news.html')


@app.route('/fifa')
def fifa():
    return render_template('fifa.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')