from newsapi import NewsApiClient
from langchain.tools import tool
from models.sentiment_analyser import sentiment_analyser
from config import NEWS_API_KEY

newsapi = NewsApiClient(api_key=NEWS_API_KEY)

@tool
def get_recent_financial_news_and_sentiment(search_term):
    try:
        all_articles = newsapi.get_everything(
            q=search_term,
            language='en',
            sort_by='relevancy',
            page_size=20
        )

        headlines = [article['title'] for article in all_articles['articles']]
        if not headlines:
            return f"No recent news found for search term: '{search_term}'."

        aggregated_score = sentiment_analyser.get_aggregated_score(headlines)
        
        top_5_headlines = "\n".join([f"- {h}" for h in headlines[:5]])

        return (
            f"Aggregated Sentiment Score for '{search_term}': {aggregated_score:.3f}\n\n"
            f"Top 5 Recent Headlines:\n{top_5_headlines}"
        )
    except Exception as e:
        return f"An error occurred while fetching news: {e}"