from statsmodels.regression.rolling import RollingOLS
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import statsmodels.api as sm
import pandas as pd
import numpy as np
import datetime as dt
import yfinance as yf
import pandas_ta 
import warnings
warnings.filterwarnings('ignore')

url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

sp500_tables = pd.read_html(url)
sp500_df = sp500_tables[0]
 
print(sp500_df.head())
