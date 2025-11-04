import requests
from google.transit import gtfs_realtime_pb2
from datetime import datetime
import pytz

def get_next_trains(station_id_prefix='635', num_trains=5):
    """
    Fetch the next trains for a given station from the MTA GTFS feed.
    
    Args:
        station_id_prefix: Station ID prefix (635 for 51st St, will check both N and S)
        num_trains: Number of upcoming trains to return
    
    Returns:
        List of dictionaries with train arrival information
    """
    try:
        # MTA GTFS Feed URL for the 6 train (part of the 1-6 lines feed)
        # This is a public feed that doesn't require an API key
        feed_url = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs'
        
        # Fetch the GTFS feed (no API key needed)
        response = requests.get(feed_url, timeout=10)
        response.raise_for_status()
        
        # Parse the protobuf feed
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(response.content)
        
        # Get current time in NYC timezone
        ny_tz = pytz.timezone('America/New_York')
        now = datetime.now(ny_tz)
        
        # Extract train arrivals for the specified station
        arrivals = []
        
        for entity in feed.entity:
            if entity.HasField('trip_update'):
                trip = entity.trip_update.trip
                for stop in entity.trip_update.stop_time_update:
                    # Check if this stop matches our station (any direction)
                    if stop.stop_id.startswith(station_id_prefix):
                        if stop.HasField('arrival'):
                            arrival_time = datetime.fromtimestamp(
                                stop.arrival.time, 
                                tz=ny_tz
                            )
                            
                            # Only include future arrivals
                            if arrival_time > now:
                                minutes_until = int((arrival_time - now).total_seconds() / 60)
                                
                                # Determine direction based on stop_id suffix
                                direction = 'Uptown' if 'N' in stop.stop_id else 'Downtown'
                                
                                arrivals.append({
                                    'route': trip.route_id,
                                    'arrival_time': arrival_time.strftime('%I:%M %p'),
                                    'minutes_until': minutes_until,
                                    'direction': direction
                                })
        
        # Sort by arrival time and return the next few trains
        arrivals.sort(key=lambda x: x['minutes_until'])
        return arrivals[:num_trains]
    
    except Exception as e:
        print(f"Error fetching subway data: {e}")
        import traceback
        traceback.print_exc()
        return []

def get_subway_data():
    """
    Get subway information for display on the home page.
    Returns data for 51st St & Lexington Ave station.
    """
    # 635 is the stop ID prefix for 51st St (covers both N and S directions)
    trains = get_next_trains(station_id_prefix='635', num_trains=6)
    
    if not trains:
        # Return placeholder data if API fails
        return {
            'station': '51st St & Lex',
            'line': '6',
            'trains': [],
            'error': 'Unable to fetch train data'
        }
    
    return {
        'station': '51st St & Lex',
        'line': '6',
        'trains': trains
    }
