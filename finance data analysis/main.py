import scrapy
import json
import requests
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Scrapy Spider to scrape financial news
class FinanceNewsSpider(scrapy.Spider):
    name = "finance_news"
    start_urls = ["https://www.reuters.com/markets/"]  # Example site

    def parse(self, response):
        for article in response.css("article.story-card"):  # Adjust based on the site's structure
            yield {
                'title': article.css("h3.story-title a::text").get(),
                'link': response.urljoin(article.css("a::attr(href)").get()),
                'summary': article.css("p::text").get(),
            }

# Function to fetch stock market data from Polygon.io
def fetch_stock_data(ticker, api_key):
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/2024-01-01/2025-01-01?apiKey={api_key}"
    response = requests.get(url)
    print(f"Fetching data from URL: {url}")
    print(f"Response Status: {response.status_code}, Response: {response.text}")
    data = response.json()
    return data.get("results", [])

# Data Analysis and Visualization
def analyze_stock_data(stock_data, ticker):
    df = pd.DataFrame(stock_data)
    df['t'] = pd.to_datetime(df['t'], unit='ms')
    df.set_index('t', inplace=True)
    
    # Plot stock prices
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df['c'], label='Closing Price')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.title(f'Stock Price Trends for {ticker}')
    plt.legend()
    plt.savefig("static/plot.png")
    
    return df.to_dict()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/stock/<ticker>')
def get_stock_data(ticker):
    print(f"Fetching data for: {ticker}")
    API_KEY = "pmTuPJFgCPpa9WtBWsB7MmSlhDr60l9O"
    stock_data = fetch_stock_data(ticker, API_KEY)
    
    if stock_data:
        data = analyze_stock_data(stock_data, ticker)
        return jsonify({"data": data, "plot": "static/plot.png"})
    else:
        return jsonify({"error": f"No data found for ticker: {ticker}. Check API key and ticker symbol."})



if __name__ == "__main__":
    #app.run(debug=True, port=5001)
    app.run(debug=True, use_reloader=False)

