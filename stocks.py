import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from io import BytesIO
import base64

# Use 'Agg' backend to avoid GUI issues with matplotlib
plt.switch_backend('Agg')

# Function to get stock prices
def get_stock_prices(symbols):
    stock_data = []
    for symbol in symbols:
        stock = yf.Ticker(symbol)
        # Use .iloc[0] to access the first row by position
        price = stock.history(period="1d")['Close'].iloc[0]
        stock_data.append({'symbol': symbol, 'price': price})
    return stock_data

# Function to fetch the S&P 500 data for the past 5 days
def fetch_sp500_data():
    sp500 = yf.Ticker("^GSPC")
    sp500_data = sp500.history(period="5d")  # Fetch past 5 days' data
    return sp500_data

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