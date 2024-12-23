import asyncio
import gc
import os
from flask import Flask, render_template, send_from_directory, redirect
from datetime import datetime, timedelta

from weather import get_weather, celcius_to_fahrenheit
from stocks import get_stock_prices, fetch_sp500_data, get_sp500_graph, get_sp500_change
from news import fetch_news
from fifa import render_fifa

app = Flask(__name__)

# Create an async lock for managing access to globals
data_lock = asyncio.Lock()

# ----------------------- Data -----------------------
# Global variables to store the latest data and time of the last update
latest_weather = None
latest_stocks = None
latest_news = None

last_update_time = None
time_remaining = timedelta(0)
refresh_interval = timedelta(minutes=5)  # Refresh every 5 minutes

# Async function to fetch and update weather and stock data
async def update_data():
    global latest_weather, latest_stocks, latest_news, last_update_time, time_remaining, refresh_interval
    stock_symbols = ['AAPL', 'GOOG', 'AMZN', 'MSFT', 'NVDA', 'IBM', 'TSLA', 'NFLX', 'META', 'QCOM']  # stock symbols
    
    async with data_lock:
        try:
            # Update the last update time
            last_update_time = datetime.now()

            print(f"Updating data at {last_update_time}")

            # Fetch weather for a hardcoded location (e.g., 'boston')
            latest_weather = await get_weather('boston')
            latest_weather['current']['temperature_2m_f'] = celcius_to_fahrenheit(latest_weather['current']['temperature_2m'])
            latest_weather['daily']['temperature_2m_max_f'] = celcius_to_fahrenheit(latest_weather['daily']['temperature_2m_max'])
            latest_weather['daily']['temperature_2m_min_f'] = celcius_to_fahrenheit(latest_weather['daily']['temperature_2m_min'])
            latest_weather['daily']['sunrise'][0] = datetime.strptime(latest_weather['daily']['sunrise'][0], '%Y-%m-%dT%H:%M').strftime('%I:%M %p')
            latest_weather['daily']['sunset'][0] = datetime.strptime(latest_weather['daily']['sunset'][0], '%Y-%m-%dT%H:%M').strftime('%I:%M %p')
            wind_directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
            latest_weather['current']['wind_direction_10m'] = wind_directions[int((latest_weather['current']['wind_direction_10m'] + 22.5) / 45) % 8]
            
            print("Weather data updated successfully! Temp: " + str(latest_weather['current']['temperature_2m']))

            # Fetch stock prices and S&P 500 data
            stock_prices = get_stock_prices(stock_symbols)
            sp500_data = fetch_sp500_data()
            sp500_graph = get_sp500_graph(sp500_data)
            sp500_change = get_sp500_change(sp500_data)
            latest_stocks = {
                'stock_prices': stock_prices,
                'sp500_graph': sp500_graph,
                'sp500_change': sp500_change
            }

            ibm_price = next(item['price'] for item in stock_prices if item['symbol'] == 'IBM')
            print("Stock data updated successfully! IBM: " + str(ibm_price))

            # Fetch news articles
            news = fetch_news()
            if news:
                latest_news = news
                print("News data updated successfully! Articles: " + str(len(latest_news)))
            else:
                print("No news articles fetched.")
        except Exception as e:
            print(f"Error updating data: {e}")
        
    # Force garbage collection after data update
    gc.collect()

# Function to check if an update is needed and update the data
async def check_update():
    global time_remaining
    time_remaining = time_until_next_refresh()
    if time_remaining.total_seconds() <= 0:
        print("Time to update data!")
        await update_data()
        time_remaining = refresh_interval
    else:
        print("Update time remaining: " + str(time_remaining)[:7])

    return time_remaining

# Function to calculate the time until the next refresh
def time_until_next_refresh():
    global time_remaining
    if last_update_time is None:
        return timedelta(seconds=0)
    time_remaining = last_update_time + refresh_interval - datetime.now()
    return time_remaining

# Inject the weather data and time remaining into the context for all templates
@app.context_processor
def inject_data():
    # Fetch the most recent cached data
    current_time = datetime.now().strftime('%I:%M %p')
    return {
        'weather': latest_weather,
        'time_until_refresh': time_remaining,
        'current_time': current_time
    }

# ----------------------- Index -----------------------
@app.route('/')
async def index():
    await check_update()

    if latest_weather is None:
        return "Weather data is not available. Please try again later."
    return render_template('index.html')

@app.route('/cycle')
def cycle():
    return redirect('/')

# ----------------------- Weather -----------------------
# Route to return the weather page using the cached weather data
@app.route('/weather')
async def weather():
    await check_update()

    if latest_weather is None:
        return "Weather data is not available. Please try again later."
    return render_template('weather.html', location='Boston')

# ----------------------- Stocks -----------------------
# Route to return the stocks page using the cached stock data
@app.route('/stocks')
async def stocks():
    global latest_stocks
    await check_update()
    
    if latest_stocks is None:
        return "Stock data is not available yet. Please try again later."
    return render_template('stocks.html', stock_prices=latest_stocks['stock_prices'], sp500_graph=latest_stocks['sp500_graph'], sp500_change=latest_stocks['sp500_change'])

# ----------------------- News -----------------------
@app.route('/news')
async def news():
    global latest_news
    await check_update()

    if latest_news is None:
        return "News data is not available yet. Please try again later."
    return render_template('news.html', news_data=latest_news)

# ----------------------- Fifa -----------------------
@app.route('/fifa')
def fifa():
    return render_fifa()

# ----------------------- Dashboard -----------------------
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# ----------------------- Misc -----------------------
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Start the background task to update data and run the app
if __name__ == '__main__':
    context = ('origin.pem', 'privkey.pem') #certificate and key files
    app.run(host='0.0.0.0', port=5000, ssl_context=context)