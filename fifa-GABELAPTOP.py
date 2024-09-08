from flask import Flask, render_template
import io
import pandas as pd
import requests

app = Flask(__name__)

# URL to shared Google Sheet for recent games
recent_games_url = 'https://docs.google.com/spreadsheets/d/e/1AYi1eyzHwZgTCOccHKLhAGVMfaCqqgiePkdRtV1DdQY/pub?sheet=Sheet1&range=A2%3AJ7&output=csv'
# URL to shared Google Sheet for head-to-head data
head_to_head_url = 'https://docs.google.com/spreadsheets/d/e/1AYi1eyzHwZgTCOccHKLhAGVMfaCqqgiePkdRtV1DdQY/pub?sheet=Sheet1&range=M2%3AR6&output=csv'
# URL to shared Google Sheet for total goals
total_goals_url = 'https://docs.google.com/spreadsheets/d/e/1AYi1eyzHwZgTCOccHKLhAGVMfaCqqgiePkdRtV1DdQY/pub?sheet=Sheet1&range=M10%3AR14&output=csv'

def fetch_data(url):
    """Fetch CSV data from the Google Sheets shared URL."""
    response = requests.get(url)
    return pd.read_csv(io.BytesIO(response.content))

@app.route('/fifa')
def fifa():
    # Fetch the data for recent games, head-to-head, and total goals
    recent_games_df = fetch_data(recent_games_url)
    head_to_head_df = fetch_data(head_to_head_url)
    total_goals_df = fetch_data(total_goals_url)

    # Pass the dataframes to the HTML template
    return render_template(
        'fifa.html',
        recent_games=recent_games_df.to_dict(orient='records'),
        head_to_head=head_to_head_df.to_dict(orient='records'),
        total_goals=total_goals_df.to_dict(orient='records')
    )