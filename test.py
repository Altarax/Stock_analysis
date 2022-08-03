from time import sleep
from bs4 import BeautifulSoup as bs
import requests
import yfinance as yf
from datetime import datetime

from stocks.utils import FRENCH_TICKERS

action = yf.Ticker("AC.PA")
print(action.info)