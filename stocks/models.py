import json
import random
from django.contrib.postgres.fields import DecimalRangeField
from django.db import models
from django.forms import IntegerField
import yfinance as yf
import matplotlib.pyplot as plt
from stocks.parsers.selenium_parser import *
from stocks.parsers.bsoup_parser import *
from django.contrib.postgres.fields import ArrayField
import json
from PIL import Image

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
    per_values = models.TextField(null=True)
    roa_values = models.TextField(null=True)
    roe_values = models.TextField(null=True)
    bna_values = models.TextField(null=True)
    bvps_values = models.TextField(null=True)
    capex_values = models.TextField(null=True)
    yield_values = models.TextField(null=True)
    turnover_values = models.TextField(null=True)
    net_margin_values = models.TextField(null=True)
    net_results_values = models.TextField(null=True)
    free_cash_flow_values = models.TextField(null=True)
    operating_margin_values = models.TextField(null=True)
    operating_result_values = models.TextField(null=True)

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

        if (action.dividends.empty):
            plt.figure()
            plt.plot(NULL)
            plt.savefig(f'stocks/static/images/dividend_price_{self.name}.png')
        else:
            # Save dividend price
            plt.figure(figsize=(18, 8))
            plt.grid(False)
            plt.bar(action.dividends.index, action.dividends, label=self.name, color=random.choice(colors_list), width=50)
            plt.legend(loc='upper left')
            plt.title(f"Montant du dividende par action de {action.info['longName']} depuis {action.dividends.index[0]}")
            plt.xlabel('Date')
            plt.ylabel(f'Prix de {self.name} en {action.info["currency"]}')
            plt.savefig(f'stocks/static/images/dividend_price_{self.name}.png')

    def initialize_fundamentals_data(self):
        action = yf.Ticker(str(self.symbol))
        short_name = action.info["shortName"].split()[0] 
        self.financial_url = get_financials_url(short_name)
        parser_initialize(self.financial_url, short_name)
        super().save()

    def get_bna(self):
        temp = parser_get_per()
        self.bna_values = json.dumps(temp)
        super().save()

    def get_per(self):
        temp = parser_get_per()
        self.per_values = json.dumps(temp)
        super().save()

    def get_bvps(self):
        temp = parser_get_bvps()
        self.bvps_values = json.dumps(temp)
        super().save()

    def get_roe(self):
        temp = parser_get_roe()
        self.roe_values = json.dumps(temp)
        super().save()

    def get_roa(self):
        temp = parser_get_roe()
        self.roa_values= json.dumps(temp)
        super().save()

    def get_yield(self):
        temp = parser_get_yield()
        self.yield_values = json.dumps(temp)
        super().save()

    def get_operating_margin(self):
        temp = parser_get_operating_margin()
        self.operating_margin_values = json.dumps(temp)
        super().save()

    def get_operating_result(self):
        temp = parser_get_operating_result()
        self.operating_result_values = json.dumps(temp)
        super().save()

    def get_free_cash_flow(self):
        temp = parser_get_free_cash_flow()
        self.free_cash_flow_values = json.dumps(temp)
        super().save()

    def get_net_margin(self):
        temp = parser_get_net_margin()
        self.net_margin_values = json.dumps(temp)
        super().save()

    def get_net_result(self):
        temp = parser_get_net_result()
        self.net_results_values = json.dumps(temp)
        super().save()

    def get_turnover(self):
        temp = parser_get_turnover()
        self.turnover_values = json.dumps(temp)
        super().save()

    def get_capex(self):
        temp = parser_get_capex()
        self.capex_values = json.dumps(temp)
        super().save()

    def get_all_financials_data(self):
        self.get_bna()
        self.get_per()
        self.get_roe()
        self.get_roa()
        self.get_free_cash_flow()
        self.get_capex()
        self.get_bvps()
        self.get_turnover()
        self.get_yield()
        self.get_net_margin()
        self.get_net_result()
        self.get_operating_margin()
        self.get_operating_result()

    def decode(self):
        pass
        #jsonDec = json.decoder.JSONDecoder()
        #myPythonList = jsonDec.decode(myModel.myList)