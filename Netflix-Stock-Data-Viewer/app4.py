from flask import Flask, render_template
import requests
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import io
import base64
import yfinance as yf
app = Flask(__name__)

# Web scraping function
def scrape_netflix_data():
    #url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/netflix_data_webpage.html"
    url="https://finance.yahoo.com/quote/NFLX/history/"
    #url="C:/Users/Lenovo/Documents/GitHub/portfolio/Netflix-Stock-Data-Viewer/Netflix_Yahoo_Finance.html"
    data = requests.get(url).text
    soup = BeautifulSoup(data, 'html.parser')

    netflix_data = pd.DataFrame(columns=["Date", "Open", "High", "Low", "Close", "Volume"])
    for row in soup.find("tbody").find_all('tr'):
        col = row.find_all("td")
        date = col[0].text
        open_price = col[1].text
        high = col[2].text
        low = col[3].text
        close = col[4].text
        volume = col[5].text
        netflix_data=pd.concat([netflix_data,
            pd.DataFrame([{"Date": date, "Open": open_price, "High": high, "Low": low, "Close": close, "Volume": volume}])],
            ignore_index=True
        )

    # Convert columns to appropriate data types
    netflix_data["Date"] = pd.to_datetime(netflix_data["Date"])
    netflix_data["Open"] = pd.to_numeric(netflix_data["Open"].str.replace(',', ''), errors='coerce')
    netflix_data["High"] = pd.to_numeric(netflix_data["High"].str.replace(',', ''), errors='coerce')
    netflix_data["Low"] = pd.to_numeric(netflix_data["Low"].str.replace(',', ''), errors='coerce')
    netflix_data["Close"] = pd.to_numeric(netflix_data["Close"].str.replace(',', ''), errors='coerce')
    netflix_data["Volume"] = pd.to_numeric(netflix_data["Volume"].str.replace(',', ''), errors='coerce')

    return netflix_data

# Route for the main page
@app.route("/")
def index():
    netflix_data = scrape_netflix_data()
    # Generate the plot as a base64 image
    img = io.BytesIO()
    plt.figure(figsize=(10, 5))
    plt.plot(netflix_data["Date"], netflix_data["Close"], label='Close Price')
    plt.xlabel("Date")
    plt.ylabel("Closing Price")
    plt.title("Netflix Closing Price Over Time")
    plt.legend()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template("index.html", tables=[netflix_data.to_html(classes='data')], plot_url=plot_url)

if __name__ == "__main__":
    app.run(debug=True)
