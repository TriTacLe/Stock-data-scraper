#Henter fundamentale data
import request
from bs4 import BeautifulSoup

def get_fundamental_data(ticker):
  url = "https://finance.yahoo.com/quote/{ticker}/"
  response = request.get(url)


  if response.status_code != 200:
    return {"error": "Could not fetch data from yahoo finance"}

  soup = BeautifulSoup(response.text, "lxml")

  def extract_data():
  
  return {}