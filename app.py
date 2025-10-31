import gc
import os
import threading
from flask import Flask, render_template, redirect, send_from_directory
from datetime import datetime, timedelta

from weather import get_weather, celcius_to_fahrenheit
from stocks import get_stock_prices, fetch_sp500_data, get_sp500_graph, get_sp500_change
from news import fetch_news
from fifa import render_fifa

app = Flask(__name__)

# Thread lock for managing access to globals
data_lock = threading.Lock()

# ----------------------- Data -----------------------
# Global variables to store the latest data and time of the last update
latest_weather = None
latest_stocks = None
latest_news = None

last_update_time = None
time_remaining = timedelta(0)
refresh_interval = timedelta(minutes=5)  # Refresh every 5 minutes

# Function to fetch and update weather and stock data (synchronous)
def update_data():
    global latest_weather, latest_stocks, latest_news, last_update_time
    stock_symbols = ['AAPL', 'GOOG', 'AMZN', 'MSFT', 'NVDA', 'IBM', 'TSLA', 'NFLX', 'META', 'QCOM', 'AMD', 'INTC']  # stock symbols
    
    with data_lock:
        try:
            # Update the last update time
            last_update_time = datetime.now()

            print(f"Updating data at {last_update_time}")

            # Fetch weather for a hardcoded location (e.g., 'manhattan')
            weather_data = get_weather('manhattan')
            
            # Check if we got an error response
            if 'error' in weather_data:
                print(f"Weather API error: {weather_data['error']}")
                raise Exception(f"Failed to fetch weather: {weather_data['error']}")
            
            weather_data['current']['temperature_2m_f'] = celcius_to_fahrenheit(weather_data['current']['temperature_2m'])
            weather_data['daily']['temperature_2m_max_f'] = celcius_to_fahrenheit(weather_data['daily']['temperature_2m_max'])
            weather_data['daily']['temperature_2m_min_f'] = celcius_to_fahrenheit(weather_data['daily']['temperature_2m_min'])
            weather_data['daily']['sunrise'] = [
                datetime.strptime(sunrise, '%Y-%m-%dT%H:%M').strftime('%I:%M %p')
                for sunrise in weather_data['daily']['sunrise']
            ]
            weather_data['daily']['sunset'] = [
                datetime.strptime(sunset, '%Y-%m-%dT%H:%M').strftime('%I:%M %p')
                for sunset in weather_data['daily']['sunset']
            ]
            wind_directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
            weather_data['current']['wind_direction_10m'] = wind_directions[int((weather_data['current']['wind_direction_10m'] + 22.5) / 45) % 8]
            latest_weather = weather_data
            
            print("Weather data updated successfully! Temp: " + str(latest_weather['current']['temperature_2m']))

            # Fetch stock prices and S&P 500 data
            stock_prices = get_stock_prices(stock_symbols)
            sp500_data = fetch_sp500_data()
            sp500_graph = get_sp500_graph(sp500_data)
            sp500_graph_transparent = get_sp500_graph(sp500_data, transparent=True)
            sp500_change = get_sp500_change(sp500_data)
            latest_stocks = {
                'stock_prices': stock_prices,
                'sp500_graph': sp500_graph,
                'sp500_graph_transparent': sp500_graph_transparent,
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
            import traceback
            traceback.print_exc()
        
    # Force garbage collection after data update
    gc.collect()

# Function to check if an update is needed and update the data
def check_update():
    global time_remaining
    time_remaining = time_until_next_refresh()
    if time_remaining.total_seconds() <= 0:
        print("Time to update data!")
        update_data()
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
def index():
    check_update()

    if latest_weather is None:
        return "Data is not available yet :( Please try again later."
    return render_template('index.html')

@app.route('/cycle')
def cycle():
    return redirect('/')

# ----------------------- Weather -----------------------
# Route to return the weather page using the cached weather data
@app.route('/weather')
def weather():
    check_update()

    if latest_weather is None:
        return "Weather data is not available. Please try again later."
    daily_data = latest_weather['daily']
    daily_forecast = []

    for index, date_str in enumerate(daily_data['time'][:7]):
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            formatted_date = date_obj.strftime('%a %b %d')
        except ValueError:
            formatted_date = date_str

        daily_forecast.append({
            'date': formatted_date,
            'code': daily_data.get('weather_code', [None] * len(daily_data['time']))[index],
            'high_f': daily_data['temperature_2m_max_f'][index],
            'low_f': daily_data['temperature_2m_min_f'][index],
            'high_c': daily_data['temperature_2m_max'][index],
            'low_c': daily_data['temperature_2m_min'][index],
            'sunrise': daily_data['sunrise'][index],
            'sunset': daily_data['sunset'][index],
            'uv': daily_data['uv_index_max'][index],
            'humidity': daily_data.get('relative_humidity_2m_max', [0] * len(daily_data['time']))[index],
            'rain': daily_data.get('precipitation_sum', [0] * len(daily_data['time']))[index]
        })

    return render_template('weather.html', location='Manhattan', daily_forecast=daily_forecast)

# ----------------------- Stocks -----------------------
# Route to return the stocks page using the cached stock data
@app.route('/stocks')
def stocks():
    global latest_stocks
    check_update()
    
    if latest_stocks is None:
        return "Stock data is not available yet. Please try again later."
    return render_template('stocks.html', stock_prices=latest_stocks['stock_prices'], sp500_graph=latest_stocks['sp500_graph'], sp500_change=latest_stocks['sp500_change'])

# ----------------------- News -----------------------
@app.route('/news')
def news():
    global latest_news
    check_update()

    if latest_news is None:
        return "News data is not available yet. Please try again later."
    return render_template('news.html', news_data=latest_news)

# ----------------------- Fifa -----------------------
@app.route('/fifa')
def fifa():
    return render_fifa()

# ----------------------- Home -----------------------
@app.route('/home')
def home():
    check_update()
    
    # Prepare data for each tile, setting to None if unavailable
    stock_prices = None
    sp500_graph = None
    sp500_change = None
    weather_preview = None
    news_data = None
    
    # Stock data
    if latest_stocks is not None:
        stock_prices = latest_stocks.get('stock_prices')
        sp500_graph = latest_stocks.get('sp500_graph_transparent')  # Use transparent version for home
        sp500_change = latest_stocks.get('sp500_change')
    
    # Weather data
    if latest_weather is not None:
        try:
            daily_data = latest_weather['daily']
            weather_preview = []
            for index in range(5):
                date_str = daily_data['time'][index]
                try:
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    formatted_date = date_obj.strftime('%a')
                except ValueError:
                    formatted_date = date_str
                
                weather_preview.append({
                    'date': formatted_date,
                    'code': daily_data.get('weather_code', [None] * len(daily_data['time']))[index],
                    'high_c': daily_data['temperature_2m_max'][index],
                    'low_c': daily_data['temperature_2m_min'][index],
                    'high_f': daily_data['temperature_2m_max_f'][index],
                    'low_f': daily_data['temperature_2m_min_f'][index],
                    'precipitation': daily_data.get('precipitation_sum', [0] * len(daily_data['time']))[index],
                    'humidity': daily_data.get('relative_humidity_2m_max', [0] * len(daily_data['time']))[index],
                })
        except (KeyError, IndexError) as e:
            print(f"Error preparing weather preview: {e}")
            weather_preview = None
    
    # News data
    if latest_news is not None:
        news_data = latest_news
    
    return render_template('home.html', 
                         stock_prices=stock_prices,
                         sp500_graph=sp500_graph,
                         sp500_change=sp500_change,
                         weather_preview=weather_preview,
                         news_data=news_data)

# ----------------------- Dashboard -----------------------
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# ----------------------- Findmy -----------------------
@app.route('/findmy')
def findmy():
    return send_from_directory(os.path.join(app.root_path, 'findmy', 'noVNC'), 'vnc.html')

# ----------------------- Misc -----------------------
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Start the background task to update data and run the app
if __name__ == '__main__':
    # Fetch initial data before starting the server
    print("Fetching initial data...")
    update_data()
    
    context = ('origin.pem', 'privkey.pem') #certificate and key files
    debug_mode = os.getenv('DOCKER') is None
    app.run(host='0.0.0.0', port=5000, debug=debug_mode, ssl_context=context)