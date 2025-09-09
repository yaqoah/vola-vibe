import os
from dotenv import load_dotenv

load_dotenv()

FUTURES_INSTRUMENTS = [
    {
        "ticker": "NQ=F",
        "name": "Nasdaq 100 Futures",
        "search_term": '"Nasdaq 100" OR "NDX" OR "Nasdaq futures"'
    },
    {
        "ticker": "YM=F",
        "name": "Dow Jones Industrial Average Futures",
        "search_term": '"Dow Jones" OR "DJIA" OR "Dow futures"'
    },
    {
        "ticker": "ES=F",
        "name": "S&P 500 Futures",
        "search_term": '"S&P 500" OR "SPX" OR "S&P futures"'
    }
]

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

if not NEWS_API_KEY:
    raise ValueError("API keys for OpenAI and NewsAPI must be set in the .env file.")