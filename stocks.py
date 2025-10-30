import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mtick
from io import BytesIO
import base64
import datetime

# Use 'Agg' backend to avoid GUI issues with matplotlib
plt.switch_backend('Agg')

# Function to get stock prices and percentage change over the past 5 days for multiple symbols
import requests

def get_stock_prices(symbols):
    stock_prices = []
    for symbol in symbols:
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=2d'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        with requests.get(url, headers=headers) as response:  # Ensures connection is closed after request
            data = response.json()
            try:
                result = data['chart']['result'][0]
                timestamps = result['timestamp']
                close_prices = result['indicators']['quote'][0]['close']
                if len(close_prices) < 2:
                    continue
                start_price = close_prices[-2]
                end_price = close_prices[-1]
                percentage_change = ((end_price - start_price) / start_price) * 100
                stock_prices.append({
                    'symbol': symbol,
                    'price': round(end_price, 2),
                    'percentage_change': round(percentage_change, 2)
                })
            except (KeyError, IndexError, TypeError):
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
    line_color = '#2563eb'
    fill_color = '#2563eb'
    values = sp500_data['Close']
    fig, ax = plt.subplots(figsize=(6, 4), constrained_layout=True)
    ax.plot(sp500_data.index, values, color=line_color, linewidth=2)
    ax.fill_between(sp500_data.index, values, color=fill_color, alpha=0.08)

    # Apply minimalist styling that still keeps the chart readable in the dashboard
    ax.set_facecolor('white')
    fig.patch.set_alpha(0)
    ax.set_xlabel('Date', fontsize=11, color='#4b5563', labelpad=8)
    ax.set_ylabel('Price', fontsize=11, color='#4b5563', labelpad=8)
    ax.tick_params(axis='x', colors='#374151', labelsize=10, rotation=45)
    ax.tick_params(axis='y', colors='#374151', labelsize=10)

    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))

    for spine in ('top', 'right'):
        ax.spines[spine].set_visible(False)
    for spine in ('left', 'bottom'):
        ax.spines[spine].set_color('#d1d5db')
        ax.spines[spine].set_linewidth(1)

    ax.grid(axis='y', color='#e5e7eb', linewidth=0.8, alpha=0.8, linestyle='-')
    ax.grid(False, axis='x')

    # Fit the y-axis tightly around the data with a small visual buffer
    y_min, y_max = values.min(), values.max()
    if y_min == y_max:
        pad = max(y_min * 0.01, 1)
        ax.set_ylim(y_min - pad, y_max + pad)
    else:
        pad = (y_max - y_min) * 0.08
        ax.set_ylim(y_min - pad, y_max + pad)

    ax.margins(x=0.01)

    # Save the graph to a bytes buffer
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=200, bbox_inches='tight')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    plt.close(fig)

    return image_base64

# Function to calculate the total and percentage change over the past 5 days
def get_sp500_change(sp500_data):
    # Calculate total and percentage change
    start_price = sp500_data['Close'].iloc[0]
    end_price = sp500_data['Close'].iloc[-1]
    total_change = end_price - start_price
    percentage_change = (total_change / start_price) * 100

    return total_change, percentage_change