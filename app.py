from flask import Flask, render_template, jsonify
import time

app = Flask(__name__)

# Route for weather page
@app.route('/')
def weather():
    return render_template('weather.html')

# Route for stocks page
@app.route('/stocks')
def stocks():
    return render_template('stocks.html')

# Route for news page
@app.route('/news')
def news():
    return render_template('news.html')

# API endpoint to get the current time (can expand for screen changes)
@app.route('/api/time')
def get_time():
    return jsonify({'time': time.strftime('%H:%M:%S')})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
