import random
from symtable import Symbol
from unicodedata import name
from django.db import models
import yfinance as yf
import matplotlib.pyplot as plt
from stocks.parsers.selenium_parser import *
from stocks.parsers.bsoup_parser import *

# Choosing my plt style
plt.style.use('classic')

# Colors list for lines in plot
colors_list = ["r", "b", "g", "k", "m", "y", "c"]

# Create your models here.
class Stock(models.Model):
    name = models.CharField(max_length=60)
    symbol = models.CharField(max_length=10)
    slug = models.SlugField()
    financial_url = models.CharField(max_length=60)

    def get_current_price(self):
        action = yf.Ticker(str(self.symbol))
        return action.info

    def get_price_hist(self):
        action = yf.Ticker(str(self.symbol))
        hist = action.history(period="max")
        hist.index = hist.index.date
        
        # Save hist price
        plt.rcParams.update({'font.size': 22})
        plt.figure(figsize=(18, 8))
        plt.grid(False)
        plt.plot(hist.index, hist["Open"], label=self.name, color=random.choice(colors_list))
        plt.legend(loc='upper right')
        plt.title(f"Montant par action de {action.info['longName']} depuis {hist.index[0]}")
        plt.xlabel('Date')
        plt.ylabel(f'Prix de {self.symbol} en {action.info["currency"]}')
        plt.savefig(f'stocks/static/images/hist_price_{self.name}.png', bbox_inches='tight')

    def get_dividend_hist(self):
        action = yf.Ticker(str(self.symbol))

        # Save dividend price
        plt.figure(figsize=(18, 8))
        plt.grid(False)
        plt.bar(action.dividends.index, action.dividends, label=self.name, color=random.choice(colors_list), width=50)
        plt.legend(loc='upper left')
        plt.title(f"Montant du dividende par action de {action.info['longName']} depuis {action.dividends.index[0]}")
        plt.xlabel('Date')
        plt.ylabel(f'Prix de {self.name} en {action.info["currency"]}')
        plt.savefig(f'stocks/static/images/dividend_price_{self.name}.png')

    def get_fundamentals_data(self):
        action = yf.Ticker(str(self.symbol))
        self.financial_url = get_financials_url(action.info["shortName"])
        save_graphs(self.financial_url, action.info["shortName"])
        super().save()