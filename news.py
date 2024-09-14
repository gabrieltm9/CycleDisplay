import requests

API_KEY = '295cbf9c4b4248bbade7f0e36339036d'

def fetch_news(category, country='us'):
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        'country': country,
        'category': category,
        'apiKey': API_KEY
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'ok':
            articles = data.get('articles', [])[:6]  # Get the articles list

            # Remove the source key from each article title
            for article in articles:
                title = article.get('title', '')  # Get the title of the article
                last_hyphen_index = title.rfind('-')  # Find the last instance of '-'
                if last_hyphen_index != -1:
                    article['title'] = title[:last_hyphen_index]  # Remove characters after the last hyphen
            
            return data.get('articles', [])[:6]  # Return only 6 articles
    return []

def fetch_all_news():
    return {
        'global': fetch_news('general'),  # Fetch general news (global)
        'business': fetch_news('business'),
        'technology': fetch_news('technology')
    }