from flask import Flask, render_template
import io
import pandas as pd
import requests

app = Flask(__name__)

# Corrected URLs for shared Google Sheets with CSV format
recent_games_url = 'https://docs.google.com/spreadsheets/d/1AYi1eyzHwZgTCOccHKLhAGVMfaCqqgiePkdRtV1DdQY/gviz/tq?tqx=out:csv&range=A1:J8'
head_to_head_url = 'https://docs.google.com/spreadsheets/d/1AYi1eyzHwZgTCOccHKLhAGVMfaCqqgiePkdRtV1DdQY/gviz/tq?tqx=out:csv&range=M1:R6'
total_goals_url = 'https://docs.google.com/spreadsheets/d/1AYi1eyzHwZgTCOccHKLhAGVMfaCqqgiePkdRtV1DdQY/gviz/tq?tqx=out:csv&range=M9:R14'

def fetch_data(url):
    """Fetch CSV data from the Google Sheets shared URL."""
    response = requests.get(url)
    if response.status_code == 200:
        df = pd.read_csv(io.BytesIO(response.content), sep=',')
        df = df.fillna("")  # Replace all NaNs with empty strings
        df = df.dropna(axis=1, how='all')  # Drop columns that are all NaN
        return df
    else:
        raise Exception(f"Error fetching data from {url}")

def render_fifa():
    # Fetch the data for recent games, head-to-head, and total goals
    recent_games_df = fetch_data(recent_games_url)
    head_to_head_df = fetch_data(head_to_head_url)
    total_goals_df = fetch_data(total_goals_url)

    # Pass the dataframes to the HTML template
    return render_template(
        'fifa.html',
        recent_games=df_to_html(recent_games_df),
        head_to_head=df_to_html(head_to_head_df),
        total_goals=df_to_html(total_goals_df)
    )

def df_to_html(df):
    """Convert a DataFrame to an HTML table."""
    return df.to_html(classes=["table", "table-bordered", "table-striped", "table-hover", "table-sm"], index=False)