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
    price = stock.history(period="1d")["Close"].iloc[-1]
    
    return {
      "ticker": ticker,
      "price": price
    }
  except Exception as e:
    raise HTTPException(status_code=404, detail="Error fetching stock data")

#Run the api with uvicorn
if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="127.0.0.1", port=8000)