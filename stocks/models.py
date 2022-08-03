from datetime import date
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
from stocks.utils import *

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
    date_dividend = models.TextField(null=True)
    date_hist = models.TextField(null=True)
    stock_hist = models.TextField(null=True)
    dividend_hist = models.TextField(null=True)
    per_values = models.TextField(null=True)
    roa_values = models.TextField(null=True)
    roe_values = models.TextField(null=True)
    bna_values = models.TextField(null=True)
    bvps_values = models.TextField(null=True)
    debt_values = models.TextField(null=True)
    capex_values = models.TextField(null=True)
    yield_values = models.TextField(null=True)
    equity_values = models.TextField(null=True)
    leverage_values = models.TextField(null=True)
    treasury_values = models.TextField(null=True)
    turnover_values = models.TextField(null=True)
    net_margin_values = models.TextField(null=True)
    net_results_values = models.TextField(null=True)
    free_cash_flow_values = models.TextField(null=True)
    capitalization_values = models.TextField(null=True)
    operating_margin_values = models.TextField(null=True)
    operating_result_values = models.TextField(null=True)  
    sector = models.TextField(null=True)
    floating_stock = models.IntegerField(null=True)
    dividend_distribution_rate = models.IntegerField(null=True)

    def get_current_price(self):
        action = yf.Ticker(str(self.symbol))
        return action.info

    def get_sector(self):
        action = yf.Ticker(str(self.symbol))
        temp = ""
        try:
            temp += action.info["sector"]
        except KeyError:
            temp += "Unknown"
        self.sector = temp
        super().save()
        

    def get_price_hist(self):
        action = yf.Ticker(str(self.symbol))
        hist = action.history(period="max")

        if (hist.empty):
            self.date_hist = '0'
            self.stock_hist = '0'
            super().save()
            """
            # Create empty plot
            plt.figure()
            plt.plot(NULL)
            plt.savefig(f'stocks/static/images/hist_price_{self.name}.png')
            """
        else:
            hist.index = hist.index.date
            hist_data = [i.strftime("%m/%d/%Y") for i in hist.index.tolist()]
            self.date_hist = json.dumps(hist_data)
            self.stock_hist = json.dumps(hist["Open"].tolist())
            super().save()
            """
            # Save hist price
            plt.rcParams.update({'font.size': 22})
            plt.figure(figsize=(18, 8))
            plt.grid(False)
            plt.plot(hist.index, hist["Open"], label=self.name, color=random.choice(colors_list))
            plt.legend(loc='upper right')
            plt.title(f"Montant par action de {action.info['shortName']} depuis {hist.index[0]}")
            plt.xlabel('Date')
            plt.ylabel(f'Prix de {self.symbol}')
            plt.savefig(f'stocks/static/images/hist_price_{self.name}.png', bbox_inches='tight')
            """

    def get_dividend_hist(self):
        action = yf.Ticker(str(self.symbol))
        action_list = action.dividends

        if (len(action_list) == 0):
            self.date_dividend = '0'
            self.dividend_hist = '0'
            super().save()
            """
            # Create empty plot
            plt.figure()
            plt.plot(NULL)
            plt.savefig(f'stocks/static/images/dividend_price_{self.name}.png')
            """
        else:
            div_data = [i.strftime("%m/%d/%Y") for i in action.dividends.index.tolist()]
            self.date_dividend = json.dumps(div_data)
            self.dividend_hist = json.dumps(action.dividends.tolist())
            super().save()
            """
            # Save dividend price
            plt.figure(figsize=(18, 8))
            plt.grid(False)
            plt.bar(action.dividends.index, action.dividends, label=self.name, color=random.choice(colors_list), width=50)
            plt.legend(loc='upper left')
            plt.title(f"Montant du dividende par action de {action.info['shortName']} depuis {action.dividends.index[0]}")
            plt.xlabel('Date')
            plt.ylabel(f'Prix de {self.name}')
            plt.savefig(f'stocks/static/images/dividend_price_{self.name}.png')
            """

    def initialize_fundamentals_data(self):
        action = yf.Ticker(str(self.symbol))
        name = ""
        try:
            name += action.info["longName"]
        except:
            name += action.info["shortName"]
        self.financial_url = get_financials_url(name.replace(' SA', ''))
        parser_initialize(self.financial_url, name.replace(' SA', ''))
        super().save()

    def get_bna(self):
        temp = parser_get_bna()
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

    def get_debt(self):
        temp = parser_get_debt()
        self.debt_values = json.dumps(temp)
        super().save()

    def get_treasury(self):
        temp = parser_get_treasury()
        self.treasury_values = json.dumps(temp)
        super().save()

    def get_equity(self):
        temp = parser_get_equity()
        self.equity_values = json.dumps(temp)
        super().save()

    def get_cap(self):
        temp = parser_get_cap()
        self.capitalization_values = json.dumps(temp)
        super().save()

    def get_leverage(self):
        temp = parser_get_leverage()
        self.capitalization_values = json.dumps(temp)
        super().save()

    def get_floating_stock(self):
        temp = parser_get_floating_stock()
        self.floating_stock = temp
        super().save()

    def get_floating_stock(self):
        temp = parser_get_floating_stock()
        self.floating_stock = temp
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