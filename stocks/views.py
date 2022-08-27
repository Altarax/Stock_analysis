from time import sleep
from django.http import HttpResponse
from django.shortcuts import render, redirect
from stocks.utils import *
from stocks.models import *
import os

# Create your views here.
def index(request):
    stocks = {"Stocks": Stock.objects.order_by("name")}
    images = os.listdir('stocks/static/images/')
    stock_names = []
    for i in STOCK_LIST:
        stock_names.append(str(i[0]))
    return render(request, 'stocks/index.html', context={"STOCK_LIST": stock_names, "stocks": stocks["Stocks"], "images": images})


def visualize_data(request):
    first_stock = request.POST.get('first-stock')
    second_stock = request.POST.get('second-stock')

    first_stock = Stock.objects.get(name=first_stock)
    second_stock = Stock.objects.get(name=second_stock)

    fs_mean_values, fs_years = get_per_mean(first_stock.sector)
    ss_mean_values, ss_years = get_per_mean(second_stock.sector)

    context = {
        "fs_mean_per":fs_mean_values,
        "fs_mean_per_dates":fs_years,
        "fs_name":first_stock.name,
        "fs_floating_stock":first_stock.floating_stock,
        "fs_dividend_distribution_rate":first_stock.dividend_distribution_rate,
        "fs_sector":first_stock.sector,
        "fs_stock_values":first_stock.stock_values,
        "fs_date_hist":first_stock.date_hist,
        "fs_dividend_values":first_stock.dividend_values,
        "fs_date_dividend":first_stock.date_dividend,
        "fs_bna":first_stock.bna_values,
        "fs_per":first_stock.per_values,
        "fs_roe":first_stock.roe_values,
        "fs_roa":first_stock.roa_values,
        "fs_free_cash_flow":first_stock.free_cash_flow_values,
        "fs_bvps":first_stock.bvps_values,
        "fs_turnover":first_stock.turnover_values,
        "fs_yield":first_stock.yield_values,
        "fs_debt":first_stock.debt_values,
        "fs_capex":first_stock.capex_values,
        "fs_equity":first_stock.equity_values,
        "fs_leverage":first_stock.leverage_values,
        "fs_treasury":first_stock.treasury_values,
        "fs_net_margin":first_stock.net_margin_values,
        "fs_net_results":first_stock.net_results_values,
        "fs_capitalization":first_stock.capitalization_values,
        "fs_operating_margin":first_stock.operating_margin_values,
        "fs_operating_result":first_stock.operating_result_values,
        "fs_last_table_date":first_stock.last_table_date,
        "fs_second_table_date":first_stock.second_table_date,
        "fs_years_date":first_stock.years_date,

        "ss_mean_per":ss_mean_values,
        "ss_mean_per_dates":ss_years,
        "ss_name":second_stock.name,
        "ss_floating_stock":second_stock.floating_stock,
        "ss_dividend_distribution_rate":second_stock.dividend_distribution_rate,
        "ss_sector":second_stock.sector,
        "ss_stock_values":second_stock.stock_values,
        "ss_dividend_values":second_stock.dividend_values,
        "ss_date_hist":second_stock.date_hist,
        "ss_date_dividend":second_stock.date_dividend,
        "ss_bna":second_stock.bna_values,
        "ss_per":second_stock.per_values,
        "ss_roe":second_stock.roe_values,
        "ss_roa":second_stock.roa_values,
        "ss_free_cash_flow":second_stock.free_cash_flow_values,
        "ss_bvps":second_stock.bvps_values,
        "ss_turnover":second_stock.turnover_values,
        "ss_yield":second_stock.yield_values,
        "ss_debt":second_stock.debt_values,
        "ss_capex":second_stock.capex_values,
        "ss_equity":second_stock.equity_values,
        "ss_leverage":second_stock.leverage_values,
        "ss_treasury":second_stock.treasury_values,
        "ss_net_margin":second_stock.net_margin_values,
        "ss_net_results":second_stock.net_results_values,
        "ss_capitalization":second_stock.capitalization_values,
        "ss_operating_margin":second_stock.operating_margin_values,
        "ss_operating_result":second_stock.operating_result_values,
        "ss_last_table_date":second_stock.last_table_date,
        "ss_second_table_date":second_stock.second_table_date,
        "ss_years_date":second_stock.years_date,
    }

    return render(request, 'stocks/data.html', context=context)

def visualize_news(requestion):
    pass

def get_per_mean(sector):
    all_entries = Stock.objects.filter(sector__exact=sector)
    jsonDec = json.decoder.JSONDecoder()
    per_2014 = []
    per_2015 = []
    per_2016 = []
    per_2017 = []
    per_2018 = []
    per_2019 = []
    per_2020 = []
    per_2021 = []
    per_2022 = []
    per_2023 = []
    per_2024 = []
    per_2025 = []
    years = ['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025']

    for i in all_entries:
        if i.per_values != None:
            temp_val = jsonDec.decode(i.per_values)
            temp_dates = json.loads(json.dumps(i.years_date))
            dic_temp = dict(zip(ast.literal_eval(temp_dates), temp_val))
            for y in years:
                    if y == '2014':
                        per_2014.append(dic_temp.get(y))
                    if y == '2015':
                        per_2015.append(dic_temp.get(y))
                    if y == '2016':
                        per_2016.append(dic_temp.get(y))
                    if y == '2017':
                        per_2017.append(dic_temp.get(y))
                    if y == '2018':
                        per_2018.append(dic_temp.get(y))
                    if y == '2019':
                        per_2019.append(dic_temp.get(y))
                    if y == '2020':
                        per_2020.append(dic_temp.get(y))
                    if y == '2021':
                        per_2021.append(dic_temp.get(y))
                    if y == '2022':
                        per_2022.append(dic_temp.get(y))
                    if y == '2023':
                        per_2023.append(dic_temp.get(y))
                    if y == '2024':
                        per_2024.append(dic_temp.get(y))
                    if y == '2025':
                        per_2025.append(dic_temp.get(y))
    per_2014 = [i if i is not None else 0 for i in per_2014]
    per_2015 = [i if i is not None else 0 for i in per_2015]
    per_2016 = [i if i is not None else 0 for i in per_2016]
    per_2017 = [i if i is not None else 0 for i in per_2017]
    per_2018 = [i if i is not None else 0 for i in per_2018]
    per_2019 = [i if i is not None else 0 for i in per_2019]
    per_2020 = [i if i is not None else 0 for i in per_2020]
    per_2021 = [i if i is not None else 0 for i in per_2021]
    per_2022 = [i if i is not None else 0 for i in per_2022]
    per_2023 = [i if i is not None else 0 for i in per_2023]
    per_2024 = [i if i is not None else 0 for i in per_2024]
    per_2025 = [i if i is not None else 0 for i in per_2025]
    fs_mean_values =    [mean(per_2014), mean(per_2015), mean(per_2016), mean(per_2017), mean(per_2018), mean(per_2019), 
                                mean(per_2020), mean(per_2021), mean(per_2022), mean(per_2023), mean(per_2024), mean(per_2025)]
    return fs_mean_values, years