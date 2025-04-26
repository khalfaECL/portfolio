from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

app = Flask(__name__)

def scrape_netflix_data():
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)  

    url = "https://finance.yahoo.com/quote/NFLX/history/"
    driver.get(url)

    time.sleep(5)  

    
    rows = driver.find_elements(By.XPATH, '//table//tbody/tr')

    netflix_data = pd.DataFrame(columns=["Date", "Open", "High", "Low", "Close", "Volume"])

    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) < 6:
            continue  

        date = cols[0].text
        open_price = cols[1].text
        high = cols[2].text
        low = cols[3].text
        close = cols[4].text
        volume = cols[6].text if len(cols) > 6 else cols[5].text  

        netflix_data = pd.concat([
            netflix_data,
            pd.DataFrame([{
                "Date": date, "Open": open_price, "High": high, "Low": low, "Close": close, "Volume": volume
            }])
        ], ignore_index=True)

    driver.quit()

    
    netflix_data["Date"] = pd.to_datetime(netflix_data["Date"], errors='coerce')
    netflix_data["Date"] = netflix_data["Date"].dt.strftime('%Y-%m-%d')
    netflix_data["Open"] = pd.to_numeric(netflix_data["Open"].str.replace(',', '').str.replace('-', ''), errors='coerce')
    netflix_data["High"] = pd.to_numeric(netflix_data["High"].str.replace(',', '').str.replace('-', ''), errors='coerce')
    netflix_data["Low"] = pd.to_numeric(netflix_data["Low"].str.replace(',', '').str.replace('-', ''), errors='coerce')
    netflix_data["Close"] = pd.to_numeric(netflix_data["Close"].str.replace(',', '').str.replace('-', ''), errors='coerce')
    netflix_data["Volume"] = pd.to_numeric(netflix_data["Volume"].str.replace(',', '').str.replace('-', ''), errors='coerce')

    netflix_data = netflix_data.dropna(subset=["Date"])  
    netflix_data.to_excel("../Netflix-Stock-Data/data/netflix_data.xlsx", index=False)
    return netflix_data

@app.route("/")
def index():
    netflix_data = scrape_netflix_data()

    
    img = io.BytesIO()
    plt.figure(figsize=(10, 5))
    plt.plot(netflix_data["Date"], netflix_data["Close"], label='Close Price')
    plt.xlabel("Date")
    plt.ylabel("Closing Price")
    plt.title("Netflix Closing Price Over Time")
    plt.legend()
    plt.tight_layout()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template("index.html", tables=[netflix_data.to_html(classes='data')], plot_url=plot_url)

if __name__ == "__main__":
    app.run(debug=True)
