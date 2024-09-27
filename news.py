from datetime import datetime, timedelta

import worldnewsapi

API_KEY = 'bf01da6925de41fb9ec675822593a52a'

configuration = worldnewsapi.Configuration(
    host = "https://api.worldnewsapi.com"
)
configuration.api_key['apiKey'] = API_KEY

last_api_call = None  # This will store the last time the API call was made
start_fetch = '06:00'
end_fetch = '22:00'
time_between_fetches = timedelta(minutes=60)

max_articles_per_source = 4
number_of_articles = 18

# Blacklist words in the title to reduce spam
blacklist_words = ['wordle', 'crossword', 'hints and answers']
blacklist_sports = [
    "lakers",
    "yankees",
    "bulls",
    "cowboys",
    "warriors",
    "knicks",
    "dodgers",
    "packers",
    "cubs",
    "49ers",
    "rams",
    "eagles",
    "rockets",
    "steelers",
    "seahawks",
    "spurs",
    "saints",
    "broncos",
    "pistons",
]
# Override blacklist if title contains any of these words
whitelisted_words = ['red sox', 'celtics', 'bruins', 'patriots']

def is_within_time_range():
    """Check if the current time is between start and end times."""
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
    time_passed = current_time - time_between_fetches
    if last_api_call < time_passed:
        return True

    return False


def fetch_news(categories = ['politics','business','technology','science'], country='us'):    
    """Fetch news from the API if the conditions are met."""
    global last_api_call

    if not is_within_time_range():
        print("Conditions not met for fetching news - not within time range: {} to {}".format(start_fetch, end_fetch))
        return []
    if not check_fetch_delay():
        remaining_delay = last_api_call + time_between_fetches - datetime.now()
        print(f"Conditions not met for fetching news - remaining fetch delay: {remaining_delay}")
        return []
    
    with worldnewsapi.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = worldnewsapi.NewsApi(api_client)
        source_countries = 'us' # str | The ISO 3166 country code of the country for which top news should be retrieved.
        language = 'en' # str | The ISO 6391 language code of the top news. The language must be one spoken in the source-country.
        number = 100
        news_sources = 'www.cnn.com,www.bbc.co.uk,www.bloomberg.com,www.reuters.com,aljazeera.com,time.com,cnbc.com,www.pcgamer.com,www.forbes.com,bostonherald.com,techcrunch.com,arstechnica.com,scientificamerican.com'

        # Earliest publish date 12 hours ago
        start_date = (datetime.now() - timedelta(hours=12)).strftime('%Y-%m-%d %H:%M:%S')

        try:
            # Top News
            api_response = api_instance.search_news(news_sources=news_sources, source_countries=source_countries, language=language, number=number, earliest_publish_date=start_date, sort_direction='desc')
            news = api_response.news

            # Remove articles without an image
            news = [article for article in news if article.image]

            # Remove articles with blacklisted words/sports in the title but not whitelisted words
            news = [article for article in news if (not any(word in article.title.lower() for word in blacklist_words) and not any(sport in article.title.lower() for sport in blacklist_sports)) or any(word in article.title.lower() for word in whitelisted_words)]

            # Organize articles by source (domain)
            articles_by_source = {}
            for article in news:
                # Extract the source (domain) from the URL
                article.url = article.url.split('/')[2].replace('www.', '').split('.')[0]
                if article.url not in articles_by_source:
                    articles_by_source[article.url] = []
                articles_by_source[article.url].append(article)

            # Print the number of articles by source
            sources = {source: len(articles) for source, articles in articles_by_source.items()}
            print('Fetched sources: ', sources)

            # Ensure each source has at most 'max_articles_per_source' articles
            filtered_news = []
            for articles in articles_by_source.items():
                filtered_news.extend(articles[:max_articles_per_source])
            
            final_articles = filtered_news[:number_of_articles]

            # Sort articles by publish date again
            final_articles.sort(key=lambda x: x.publish_date, reverse=True)

            # # Replace publish date string with a formatted string showing time
            for article in final_articles:
                article.publish_date = datetime.strptime(article.publish_date, "%Y-%m-%d %H:%M:%S").strftime('%I:%M %p')

            last_api_call = datetime.now()
            return final_articles
        except Exception as e:
            print("Exception when getting news: %s\n" % e)
    
    return []