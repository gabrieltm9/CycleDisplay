import requests
from datetime import datetime, timedelta

API_KEY = '3819ce6b7a5a9cbb43f1af2b572dee90'

blacklist = ['fox', 'the guardian', 'wired', 'business line']

last_api_call = None  # This will store the last time the API call was made
start_fetch = '07:00'
end_fetch = '22:00'
hours_between_fetches = 1

max_articles_per_source = 4

def is_within_time_range():
    """Check if the current time is between 7 AM and 10 PM."""
    current_time = datetime.now().time()
    start_time = datetime.strptime(start_fetch, "%H:%M").time()
    end_time = datetime.strptime(end_fetch, "%H:%M").time()
    return start_time <= current_time <= end_time


def check_fetch_delay():
    """Determine if news should be fetched based on delay conditions."""
    global last_api_call
    current_time = datetime.now()

    if last_api_call is None:
        return True  # Fetch if no API call has been made yet

    # Check if more than one hour has passed since the last call
    hours_past = current_time - timedelta(hours=hours_between_fetches)
    if last_api_call < hours_past:
        return True

    return False


def fetch_news(categories = ['politics','business','technology','science'], country='us'):    
    """Fetch news from the API if the conditions are met."""
    global last_api_call

    if not is_within_time_range():
        print("Conditions not met for fetching news: not within time range.")
        return []
    if not check_fetch_delay():
        print("Conditions not met for fetching news: fetch delay has not elapsed.")
        return []
    
    categories_string = ','.join(categories)  # Convert the list of categories to a string

    # Date string
    start_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    end_date = datetime.now().strftime("%Y-%m-%d")
    date_string = f"{start_date},{end_date}"

    url = "http://api.mediastack.com/v1/news"
    params = {
        'access_key': API_KEY,
        'countries': country,
        'categories': categories_string,
        'languages': 'en',
        'limit': '100',
        'sort': 'popularity',
        'date': date_string,
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        news = data.get('data', [])  # Mediastack response contains 'data' key

        # Print all unique categories with count for each
        categories = {}
        for article in news:
            categories[article['category']] = categories.get(article['category'], 0) + 1
        print('Fetched categories: ', categories)

        # Remove articles without an image
        #news = [article for article in news if article.get('image')]

        # Remove articles from blacklisted sources
        news = [article for article in news if not any(source in article['source'].lower() for source in blacklist)]

        # Remove source string past the first hyphen or | character
        for article in news:
            article['source'] = article['source'].split('-')[0].strip()
            article['source'] = article['source'].split('|')[0].strip()
        
        # Ensure each source has at most 'max_articles_per_source' articles
        source_counts = {}
        filtered_news = []
        for article in news:
            source = article['source']
            if source_counts.get(source, 0) < max_articles_per_source:
                source_counts[source] = source_counts.get(source, 0) + 1
                filtered_news.append(article)

        # Move articles in a category with 3 articles or less to the front
        category_counts = {}
        for article in filtered_news:
            category = article['category']
            category_counts[category] = category_counts.get(category, 0) + 1

        filtered_news = sorted(filtered_news, key=lambda x: category_counts.get(x['category'], 0) > 3, reverse=True)

        filtered_categories = {}
        for article in filtered_news:
            filtered_categories[article['category']] = filtered_categories.get(article['category'], 0) + 1
        print('Filtered categories: ', filtered_categories)

        # Update last API call time
        last_api_call = datetime.now()

        # Return first 18 articles
        return filtered_news[:18]
    
    print(f"Error fetching news: {response.status_code}")
    return []