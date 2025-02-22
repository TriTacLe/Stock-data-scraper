from fastapi import FastAPI, HTTPException
import yfinance as yf
#Importerer de forskjellige funksjonene fra de andre filene

"""
from scraping import get_fundamental_data
from database import save_stock_data
from ml_model import predict_stock
from notifications import send_telegram_notification
"""

#Made application with metadata
app = FastAPI(title="Stock API", description="API that scrapes stock data and makes prediction", version="0.1")

#Home route 
@app.get("/")
def home():
  return {"message": "App is running Ramandeep"}

#Gets data from yahoo finance 
@app.get("/stock/{ticker}")
def stock_data(ticker: str):
  try:
    stock = yf.Ticker(ticker)
    history = stock.history(period="1d")
    
    #sanntidspris
    price = float(history["Close"].iloc[-1])
    open_price = float(history["Open"].iloc[-1])
    high_price = float(history["High"].iloc[-1])
    low_price = float(history["Low"].iloc[-1])
    volume = float(history["Volume"].iloc[-1])

    #Funamdentaldata, skal flyttes over til scraping.py for høyere cohesion
    info = stock.info
    pe = float(info.get("trailingPE", None))
    marketcap = float(info.get("marketCap", None))
    dividend_yield = float(info.get("dividendYield", None))

    #Ta indikatorer
    ma_50 = float(stock.history(period="50d")["Close"].mean())
    ma_200 = float(stock.history(period="200d")["Close"].mean())

    return {
      "ticker": ticker,
      "price": price,
      "open_price": open_price,
      "high_price": high_price,
      "low_price": low_price,
      "volume": volume,
      "marketcap": marketcap,
      "pe_ratio": pe,
      "dividend_yield": dividend_yield,
      "moving_avg_50": ma_50,
      "moving_avg_200": ma_200

    }
  except Exception as e:
    raise HTTPException(status_code=404, detail="Error fetching stock data")

#Run the api with uvicorn
if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="127.0.0.1", port=8000)