import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from io import BytesIO
import base64
import datetime

# Use 'Agg' backend to avoid GUI issues with matplotlib
plt.switch_backend('Agg')

# Function to get stock prices and percentage change over the past 5 days for multiple symbols
def get_stock_prices(symbols):
    # Prepare a list of dictionaries with symbol, its price, and the percentage change
    stock_prices = []
    for symbol in symbols:
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=5d'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        try:
            result = data['chart']['result'][0]
            timestamps = result['timestamp']
            close_prices = result['indicators']['quote'][0]['close']
            if len(close_prices) < 2:
                continue
            start_price = close_prices[0]
            end_price = result['meta']['regularMarketPrice']
            percentage_change = ((end_price - start_price) / start_price) * 100
            stock_prices.append({
                'symbol': symbol,
                'price': round(end_price, 2),
                'percentage_change': round(percentage_change, 2)
            })
        except (KeyError, IndexError, TypeError):
            # Handle error or skip this symbol
            continue
    return stock_prices

# Function to fetch the S&P 500 data for the past 5 days (only fetched once)
def fetch_sp500_data():
    symbol = '^GSPC'
    url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=5d'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    try:
        result = data['chart']['result'][0]
        timestamps = result['timestamp']
        close_prices = result['indicators']['quote'][0]['close']
        dates = [datetime.datetime.fromtimestamp(ts) for ts in timestamps]
        sp500_data = pd.DataFrame({'Date': dates, 'Close': close_prices})
        sp500_data.set_index('Date', inplace=True)
        return sp500_data
    except (KeyError, IndexError, TypeError):
        return None

# Function to generate S&P 500 graph with improved aesthetics
def get_sp500_graph(sp500_data):
    # Plot the S&P 500 data with improved aesthetics
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(sp500_data.index, sp500_data['Close'], label='S&P 500', color='blue', linewidth=2)

    # Improve formatting
    ax.set_title('S&P 500 Performance - Past 5 Days', fontsize=14, weight='bold')
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Price', fontsize=12)
    
    # Format the x-axis to show only day and month
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    plt.xticks(rotation=45)
    ax.grid(True)

    fig.patch.set_alpha(0)

    # Save the graph to a bytes buffer
    buf = BytesIO()
    plt.tight_layout()  # Adjust the layout
    plt.savefig(buf, format="png")
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    return image_base64

# Function to calculate the total and percentage change over the past 5 days
def get_sp500_change(sp500_data):
    # Calculate total and percentage change
    start_price = sp500_data['Close'].iloc[0]
    end_price = sp500_data['Close'].iloc[-1]
    total_change = end_price - start_price
    percentage_change = (total_change / start_price) * 100

    return total_change, percentage_change