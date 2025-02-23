import os
from sqlalchemy import create_engine, Column, String, Float, BigInteger, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

#Database url and env variables
DATABASE_URL = os.getenv("DATABASE_URL")

#Database connection
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#test connection
try:
  with engine.connect() as connection:
    print("Database connected ramandeep")
except Exception as e:
  print(f"Error connection to database ramandeep: {str(e)}")
class Stock(Base):
  __tablename__ = "stocks"

  id = Column(BigInteger, primary_key=True, autoincrement=True)
  ticker = Column(String, index=True)
  period = Column(String)  
  price = Column(Float)
  open_price = Column(Float)
  high_price = Column(Float)
  low_price = Column(Float)
  volume = Column(BigInteger)
  marketcap = Column(BigInteger)
  pe_ratio = Column(Float)
  dividend_yield = Column(Float)
  moving_avg_50 = Column(Float)
  moving_avg_200 = Column(Float)
  bollinger_high = Column(Float)
  bollinger_low = Column(Float)
  rsi = Column(Float)
  macd = Column(Float)
  macd_signal = Column(Float)
  stochastic_k = Column(Float)
  stochastic_d = Column(Float)
  volume_trend = Column(String)
  timestamp = Column(DateTime, default=datetime.utcnow)

#Make the table in the database
Base.metadata.create_all(bind=engine)

#Function to save stock data
def save_stock_data(data):
  session = SessionLocal()
  stock = Stock(**data)
  session.add(stock)
  session.commit()
  session.close()  