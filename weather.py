import requests

# Helper function to get coordinates from Nominatim
def get_coordinates(city):
    location_url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json&limit=1"
    headers = {
        'User-Agent': 'CycleDisplay/1.0 (Weather App)'
    }
    
    try:
        response = requests.get(location_url, headers=headers, timeout=5)
        response.raise_for_status()
        
        if response.text.strip() == '':
            print(f"Warning: Empty response from Nominatim for city: {city}")
            return None, None
            
        location_response = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching coordinates for {city}: {e}")
        return None, None
    except Exception as e:
        print(f"Error parsing coordinates response: {e}")
        return None, None

    if not location_response:
        print(f"City not found: {city}")
        return None, None

    lat = location_response[0]['lat']
    lon = location_response[0]['lon']
    return lat, lon

def get_weather(location):
    if location == 'boston':
        lat, lon = 42.361145, -71.057083
    else:
        lat, lon = get_coordinates(location)

    if lat is None or lon is None:
        return {'error': 'Location not found'}

    # Fetch weather data from Open-Meteo
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,weather_code,surface_pressure,wind_speed_10m,wind_direction_10m&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset,uv_index_max,weather_code,precipitation_sum,relative_humidity_2m_max&timezone=America%2FNew_York"
    
    try:
        response = requests.get(weather_url, timeout=5)
        response.raise_for_status()
        weather_response = response.json()
        return weather_response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return {'error': str(e)}
    except Exception as e:
        print(f"Error parsing weather response: {e}")
        return {'error': str(e)}

def celcius_to_fahrenheit(celcius):
    if isinstance(celcius, list):
        return [round(c * 9/5 + 32, 1) for c in celcius]
    else:
        return round(celcius * 9/5 + 32, 1)