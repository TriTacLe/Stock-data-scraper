from fastapi import FastAPI, HTTPException
import yfinance as yf
#import ta
#import ta.momentum
import pandas as pd

from database import save_stock_data

"""
from scraping import get_fundamental_data
from ml_model import predict_stock
from notifications import send_telegram_notification
"""

#Made fastapi instance with metadata
app = FastAPI(
  title="Stock API", 
  description="API that scrapes stock data and makes prediction", 
  version="0.1")

#Home route 
@app.get("/")
def home():
  return {"message": "App is running Ramandeep"}

#Gets data from yahoo finance 
@app.get("/stock/{ticker}/{period}")
def stock_data(ticker: str, period: str = "1d"):

  """
  :param ticker: (ex: "AAPL")
  :param period: (1d, 5d, 1mo, 3mo, 6mo, 1y, 5y, 10y, ytd, max)
  """

  VALID_PERIODS = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]

  if period not in VALID_PERIODS:
    raise HTTPException(status_code=400, detail="Invalid period ramandeep. Chose from 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max")

  try:
    stock = yf.Ticker(ticker)
    history = stock.history(period=period)
    
    if history.empty:
      raise HTTPException(status_code=404, detail="No stock data found ramandeep")

    #Helper function to safely convert to float
    def safe_float(value):
      return float(value) if not pd.isna(value) else None
 
    #Price data
    latest = history.iloc[-1]
    price = safe_float(latest["Close"])
    open_price = safe_float(latest["Open"])
    high_price = safe_float(latest["High"])
    low_price = safe_float(latest["Low"])
    volume = safe_float(latest["Volume"])

    #Fundamental data 
    info = stock.info
    pe = safe_float(info.get("trailingPE"))
    marketcap = safe_float(info.get("marketCap"))
    dividend_yield = safe_float(info.get("dividendYield"))

    #Technical indicators
    #Moving averages using existing history
    ma_50 = safe_float(history["Close"].tail(50).mean())
    ma_200 = safe_float(history["Close"].mean())
    
    #Volume analysis
    volume_avg = safe_float(history["Volume"].rolling(window=20).mean().iloc[-1])
    volume_trend = "Increasing" if volume and volume_avg and volume > volume_avg else "Decreasing"

    stock_data = {
      "ticker": ticker,
      "period": period,
      "price": price,
      "open_price": open_price,
      "high_price": high_price,
      "low_price": low_price,
      "volume": volume,
      "marketcap": marketcap,
      "pe_ratio": pe,
      "dividend_yield": dividend_yield,
      "moving_avg_50": ma_50,
      "moving_avg_200": ma_200,
      "volume_trend": volume_trend
    }

    #stock_data.pop("period", None)  

    save_stock_data(stock_data)

    return stock_data
    
  except Exception as e:
      raise HTTPException(status_code=500, detail=f"Error fetching stock data: {str(e)}")


#Run the api with uvicorn
if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="127.0.0.1", port=8000)