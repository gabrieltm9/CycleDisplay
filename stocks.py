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

# Function to generate S&P 500 graph with improved aesthetics
def get_sp500_graph():
    sp500 = yf.Ticker("^GSPC")
    sp500_data = sp500.history(period="1mo")

    # Plot the S&P 500 data with improved aesthetics
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(sp500_data.index, sp500_data['Close'], label='S&P 500', color='blue', linewidth=2)

    # Improve formatting
    ax.set_title('S&P 500 Performance - Past Month', fontsize=14, weight='bold')
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Price', fontsize=12)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
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