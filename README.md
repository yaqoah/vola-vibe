# Vola-Vibe: Sentiment-Driven Market Volatility Analysis

A financial NLP and time series analysis project that correlates news sentiment with market volatility across major U.S. futures markets using **transformer-based sentiment analysis** and **MLOps best practices**.

## Project Overview

Vola-Vibe ingests historical price data and news articles to build a **sentiment-volatility dataset** that explores correlations between financial news sentiment and market volatility. This project demonstrates **practical AI engineering** in quantitative finance: data pipeline design, domain-specific NLP, and experiment tracking.

## Tech Stack

### AI/ML Core
- **FinBERT** (HuggingFace Transformers) - Financial sentiment classification
- **PyTorch** - Deep learning framework with GPU acceleration
- **Transformers** - Pre-trained language models for NLP tasks

### Data & Finance
- **yfinance** - Historical OHLCV data for futures instruments
- **NewsAPI** - Real-time and historical financial news retrieval
- **Pandas** - Time series data manipulation and aggregation
- **LangChain** - Tool framework for AI integration

### MLOps & Production
- **MLflow** - Experiment tracking, metrics logging, and artifact management
- **python-dotenv** - Secure configuration and API key management


## What I Built

### 1. **NLP Pipeline with Domain-Specific Models**
- Implemented **FinBERT-based sentiment analyzer** with singleton pattern for efficient model loading
- Handles batch processing (32 headlines/batch) for production-grade throughput
- Normalizes sentiment scores: positive (+1 to 0), negative (-1 to 0), neutral (0)

### 2. **Time Series Data Engineering**
- Engineered historical dataset: **5+ years of daily data** across 3 futures instruments
- Calculated 30-day rolling volatility using Pandas time series operations
- Aligned news sentiment with OHLCV data on matching dates

### 3. **MLOps & Experiment Tracking**
- Integrated MLflow for reproducible ML workflows
- Logged dataset artifacts, correlation metrics, and instrument-specific statistics
- Tracked run parameters (date ranges, instruments) for reproducibility

### 4. **Production-Ready Code**
- Modular architecture: separated config, models, tools, and aggregation logic
- Error handling for missing data sources and API failures
- Cloud-agnostic: packaged for Google Colab deployment with reproducible setup

## Key Features

✅ **Multi-Instrument Analysis** - Nasdaq 100, Dow Jones, S&P 500 futures  
✅ **Financial NLP** - Domain-specific sentiment analysis with FinBERT  
✅ **Scalable Pipeline** - Batch processing + MLflow logging for large datasets  
✅ **Correlation Analysis** - Computes sentiment-volatility correlation per instrument  
✅ **Cloud-Ready** - Google Colab integration for serverless computation  


### This project is a research foundation for sentiment-driven market analysis. The sentiment-volatility correlations can serve as features for predictive models, signal generation, or risk analysis in quantitative trading.
