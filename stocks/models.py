from datetime import date
import json
from django.db import models
import yfinance as yf
import matplotlib.pyplot as plt
from stocks.parsers.bsoup_parser import *
import json
from stocks.utils import *
from datetime import date

# Choosing my plt style
plt.style.use("classic")

# Colors list for lines in plot
colors_list = ["r", "b", "g", "k", "m", "y", "c"]

# Create your models here.
class Stock(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length=60)
    isin = models.CharField(max_length=60)
    symbol = models.CharField(max_length=10)
    financial_url = models.CharField(max_length=60)
    date_dividend = models.TextField(null=True)
    date_hist = models.TextField(null=True)
    pbr_values = models.TextField(null=True)
    per_values = models.TextField(null=True)
    roa_values = models.TextField(null=True)
    roe_values = models.TextField(null=True)
    bna_values = models.TextField(null=True)
    bvps_values = models.TextField(null=True)
    debt_values = models.TextField(null=True)
    stock_values = models.TextField(null=True)
    capex_values = models.TextField(null=True)
    yield_values = models.TextField(null=True)
    equity_values = models.TextField(null=True)
    own_evaluation = models.TextField(null=True)
    dividend_values = models.TextField(null=True)
    leverage_values = models.TextField(null=True)
    treasury_values = models.TextField(null=True)
    turnover_values = models.TextField(null=True)
    net_margin_values = models.TextField(null=True)
    net_results_values = models.TextField(null=True)
    free_cash_flow_values = models.TextField(null=True)
    capitalization_values = models.TextField(null=True)
    operating_margin_values = models.TextField(null=True)
    operating_result_values = models.TextField(null=True)
    last_table_date = models.TextField(null=True)
    second_table_date = models.TextField(null=True)
    years_date = models.TextField(null=True)
    sector = models.TextField(null=True)
    floating_stock = models.IntegerField(null=True)
    dividend_distribution_rate = models.IntegerField(null=True)

    def get_current_price(self):
        action = yf.Ticker(str(self.symbol))
        return action.info

    def get_dates(self):
        self.last_table_date = parser_get_last_table()
        self.second_table_date = parser_get_second_table()
        self.years_date = parser_get_years()
        super().save()

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

        if hist.empty:
            self.date_hist = "0"
            self.stock_values = "0"
            super().save()
            """
            # Create empty plot
            plt.figure()
            plt.plot(NULL)
            plt.savefig(f'stocks/static/images/hist_price_{self.name}.png')
            """
        else:
            current_year = date.today().year
            hist.index = hist.index.date
            hist_date = [i.strftime("%m/%d/%Y") for i in hist.index.tolist()]
            try:
                val = hist_date.index(f"01/02/{current_year-10}") or hist_date.index(
                    "01/02/2012"
                )
            except:
                val = 0

            self.date_hist = json.dumps(hist_date[val:-1])
            temp = hist["Open"].tolist()[val:-1]
            temp_formated = ["%.2f" % elem for elem in temp]
            self.stock_values = json.dumps(temp_formated)
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

        if len(action_list) == 0:
            self.date_dividend = "0"
            self.dividend_values = "0"
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
            self.dividend_values = json.dumps(action.dividends.tolist())
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
        self.financial_url = parser_get_financials_url(self.isin)
        parser_initialize(self.financial_url, self.name)
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
        temp = parser_get_roa()
        self.roa_values = json.dumps(temp)
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
        self.leverage_values = json.dumps(temp)
        super().save()

    def get_floating_stock(self):
        temp = parser_get_floating_stock()
        self.floating_stock = temp
        super().save()

    def get_pbr(self):
        temp = parser_get_pbr()
        self.pbr_values = temp
        super().save()

    def get_evaluation(self):
        jsonDec = json.decoder.JSONDecoder()
        try:
            yield_val = jsonDec.decode(self.yield_values)
        except:
            yield_val = 0

        try:
            per_values = jsonDec.decode(self.per_values)
        except:
            per_values = 0

        temp = parser_calculate_own_evaluations(yield_val, per_values)
        self.own_evaluation = temp
        super().save()

    def get_all_financials_data(self):
        self.get_dates()
        self.get_sector()
        self.get_price_hist()
        self.get_dividend_hist()
        self.get_bna()
        self.get_per()
        self.get_roe()
        self.get_roa()
        self.get_free_cash_flow()
        self.get_bvps()
        self.get_turnover()
        self.get_yield()
        self.get_net_margin()
        self.get_net_result()
        self.get_operating_margin()
        self.get_operating_result()
        self.get_capex()
        self.get_debt()
        self.get_treasury()
        self.get_equity()
        self.get_cap()
        self.get_leverage()
        self.get_floating_stock()
        self.get_pbr()
        self.get_evaluation()

    def get_last_news(self, isin):
        return parser_get_last_news(isin)

    def get_majority_shareholders(self, isin):
        return parser_get_majoritary_shareholders(isin)

    def decode_stock_values(self):
        jsonDec = json.decoder.JSONDecoder()
        return jsonDec.decode(self.stock_values)
