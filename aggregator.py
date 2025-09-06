import os
import pandas as pd
import yfinance as yf
from newsapi import NewsApiClient
from datetime import date, timedelta
import time
import mlflow

from config import NEWS_API_KEY, FUTURES_INSTRUMENTS
from models.sentiment_analyser import sentiment_analyser

START_DATE = "2021-01-31"
END_DATE = date.today().strftime("%Y-%m-%d")
OUTPUT_DIR = "data"
DATABASE_FILE = os.path.join(OUTPUT_DIR, "historical_data.csv")
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

def generate_historical_data():
    with mlflow.start_run(run_name="Futures_Sentiment_Volatility_Build"):
        
        instrument_names = [inst['name'] for inst in FUTURES_INSTRUMENTS]
        mlflow.log_param("instruments", ", ".join(instrument_names))
        mlflow.log_param("start_date", START_DATE)
        mlflow.log_param("end_date", END_DATE)

        all_data = []
        
        start_date_obj = date.fromisoformat(START_DATE)
        end_date_obj = date.fromisoformat(END_DATE)
        total_days = (end_date_obj - start_date_obj).days

        print(f"Starting data generation for instruments: {instrument_names}")
        print(f"Date range: {START_DATE} to {END_DATE}")

        for instrument in FUTURES_INSTRUMENTS:
            instrument_name = instrument['name']
            ticker = instrument['ticker']
            search_term = instrument['search_term']
            
            stock_data = yf.download(ticker, start=START_DATE, end=END_DATE)
            if stock_data.empty:
                print(f"Could not fetch price data for {ticker}. Skipping.")
                continue

            stock_data.index = stock_data.index.strftime('%Y-%m-%d') 
            stock_data = stock_data[~stock_data.index.duplicated(keep='first')]


            stock_data['daily_return'] = stock_data['Close'].pct_change()
            stock_data['volatility'] = stock_data['daily_return'].rolling(window=30).std()

            print(f"  Fetching historical news for {ticker}...")
            yf_ticker = yf.Ticker(ticker)
            news_list = yf_ticker.news
            
            if not news_list:
                print(f"  Warning: No news found for {ticker} via yfinance.")
                news_df = pd.DataFrame(columns=['date', 'title'])
            else:
                news_df = pd.DataFrame(news_list)
                
                if 'publishedAt' in news_df.columns:
                    news_df['date'] = pd.to_datetime(news_df['publishedAt']).dt.strftime('%Y-%m-%d')
                elif 'providerPublishTime' in news_df.columns:
                    news_df['date'] = pd.to_datetime(news_df['providerPublishTime'], unit='s').dt.strftime('%Y-%m-%d')
                else:
                    news_df['date'] = None

                if 'title' not in news_df.columns:
                    news_df['title'] = None


            for i in range(total_days):
                current_date = start_date_obj + timedelta(days=i)
                current_date_str = current_date.strftime("%Y-%m-%d")
                
                headlines_for_day = news_df[news_df['date'] == current_date_str]['title'].tolist()
                
                sentiment_score = sentiment_analyser.get_aggregated_score(headlines_for_day)

                if current_date_str in stock_data.index:
                    volatility_series = stock_data.loc[current_date_str, 'volatility']
    
                    if isinstance(volatility_series, pd.Series):
                        volatility = volatility_series.iloc[0]
                    else:
                        volatility = volatility_series

                    if pd.notna(volatility):
                        all_data.append({
                            "date": current_date_str,
                            "instrument_name": instrument_name,
                            "ticker": ticker,
                            "sentiment_score": sentiment_score,
                            "volatility": volatility
                        })
                
                if i % 90 == 0:
                    print(f"  ... processed up to {current_date_str}")

        if not all_data:
            print("No data was generated. Exiting.")
            mlflow.log_metric("rows_generated", 0)
            return

        df = pd.DataFrame(all_data)
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        df.to_csv(DATABASE_FILE, index=False)
        print(f"\n✅ Historical database saved to {DATABASE_FILE}")

        mlflow.log_metric("rows_generated", len(df))
        mlflow.log_metric("unique_instruments", df['instrument_name'].nunique())
        mlflow.log_artifact(DATABASE_FILE, "datasets")
        
        for name in instrument_names:
            inst_df = df[df['instrument_name'] == name]
            if len(inst_df) > 1:
                correlation = inst_df['sentiment_score'].corr(inst_df['volatility'])
                if not pd.isna(correlation):
                    mlflow.log_metric(f"correlation_{name.replace(' ', '_')}", correlation)

        print("\n✅ MLflow run completed and logged.")

if __name__ == "__main__":
    generate_historical_data()