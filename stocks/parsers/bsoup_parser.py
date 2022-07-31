# Find the financials data of the company on Zonebourse with beautiful soup
from asyncio.windows_events import NULL
from unicodedata import decimal
from bs4 import BeautifulSoup as bs
from numpy import mean
import requests
import matplotlib.pyplot as plt
from decimal import Decimal


# Colors list for lines in plot
colors_list = ["r", "b", "g", "k", "m", "y", "c"]

# Global values
years = []
semesters = []
soup = bs()
table = []
company_name_global = ""
yield_values_global = []
per_values_global = []
bna_values_global = []

def add_value_label(x_list,y_list):
    for i in range(len(x_list)):
        plt.text(i, y_list[i]//2, y_list[i], fontdict={'weight':'bold', 'size':15}, ha='center')

def create_graph(x, values_list, value_name):
    plt.figure(figsize=(18, 8))
    plt.grid(True)
    plt.bar(x, values_list)
    add_value_label(x, values_list)
    plt.title(f"{value_name.capitalize()} Values")
    plt.xlabel('Date')
    plt.ylabel(f'{value_name.capitalize()}')
    plt.savefig(f'stocks/static/images/{value_name}_values_{company_name_global}.png', bbox_inches='tight')

def parser_initialize(financials_url, company_name):
    global company_name_global
    global years
    global semesters
    global table
    company_name_global = company_name
    financials_page = requests.get(financials_url)
    soup = bs(financials_page.content, 'html.parser')
    years= [soup.find('td', class_=f"bc2Y tableCol{i}").get_text() for i in range(0,6)]
    table_list = soup.find_all('table',{'class': 'BordCollapseYear2'})
    table_semesters = table_list[2]
    temp = table_semesters.tr.find_all('td')
    semesters = [t.get_text() for t in temp]
    del semesters[0]
    table = soup.find_all('td', attrs={'class':'bc2T'})

def parser_get_bna():
    global bna_values_global
    bna_values = []
    for i in table:
        if i.get_text() == "BNA2":
            bnas = i.find_next_siblings("td")
            for bna in bnas:
                if bna.get_text() == '-':
                    bna_values.append(0)
                else:
                    bna_values.append(float(bna.get_text().replace(' ', '').replace(',', '.')))
    bna_values = bna_values[0:6]
    bna_values_global = bna_values
    create_graph(years, bna_values, "bna")
    return bna_values

def parser_get_per():
    per_values = []
    global bna_values_global
    for i in table:
        if i.get_text() == "PER":
            pers = i.find_next_siblings("td")
            for per in pers:
                if per.get_text() == '-':
                    per_values.append(0)
                else:
                    per_values.append(float(per.get_text().replace(' ', '').replace('x', '').replace(',', '.')))
    per_values = per_values[0:6]
    calculated_per = []
    for i1, i2 in zip(per_values, bna_values_global):
        calculated_per.append(i1*i2)
    per_values = calculated_per
    global per_values_global
    per_values_global = per_values
    create_graph(years, per_values, "per")
    return per_values

def parser_get_roe():
    roe_values = [] = []
    for i in table:
       if i.get_text() == "ROE (RN / Capitaux Propres)":
            roes = i.find_next_siblings("td")
            for roe in roes:
                if roe.get_text() == '-':
                    roe_values.append(0)
                else:
                    roe_values.append(float(roe.get_text().replace(' ', '').replace('%', '').replace(',', '.')))
    roe_values = roe_values[0:6]
    create_graph(years, roe_values, "roe")
    return roe_values

def parser_get_roa():
    roa_values = []
    for i in table:
        if i.get_text() == "ROA (RN / Total Actif)":
            roas = i.find_next_siblings("td")
            for roa in roas:
                if roa.get_text() == '-':
                    roa_values.append(0)
                else:
                    roa_values.append(float(roa.get_text().replace(' ', '').replace('%', '').replace(',', '.')))
    roa_values = roa_values[0:6]
    create_graph(years, roa_values, "roa")
    return roa_values

def parser_get_bvps():
    bvps_values = []
    for i in table:
        if i.get_text() == "BVPS (Actif net par Action)2":
            bvpss = i.find_next_siblings("td")
            for bvps in bvpss:
                if bvps.get_text() == '-':
                    bvps_values.append(0)
                else:
                    bvps_values.append(float(bvps.get_text().replace(' ', '').replace(',', '.')))
    bvps_values = bvps_values[0:6]
    create_graph(years, bvps_values, "bvps")
    return bvps_values

def parser_get_yield():
    yield_values = []
    for i in table:
       if i.get_text() == "Rendement":
            yields = i.find_next_siblings("td")
            for y in yields:
                if y.get_text() == '-':
                    yield_values.append(0)
                else:
                    yield_values.append(float(y.get_text().replace(' ', '').replace('%', '').replace(',', '.')))
    yield_values = yield_values[0:6]
    global yield_values_global
    yield_values_global = yield_values
    create_graph(years, yield_values, "yield")
    return yield_values

def parser_get_capex():
    capex_values = []
    for i in table:
        if i.get_text() == "Capex1" or i.get_text() == "Capex":
            capexs = i.find_next_siblings("td")
            for capex in capexs:
                if capex.get_text() == '-':
                    capex_values.append(0)
                else:
                    capex_values.append(float(capex.get_text().replace(' ', '').replace(',', '.')))
    capex_values = capex_values[0:6]
    create_graph(years, capex_values, "capex")
    return capex_values

def parser_get_turnover():
    turnover_values = []
    for i in table:
       if i.get_text() == "Chiffre d'affaires1":
            turnovers = i.find_next_siblings("td")
            for turnover in turnovers:
                if turnover.get_text() == '-':
                    turnover_values.append(0)
                else:
                    turnover_values.append(int(turnover.get_text().replace(' ', '')))
    turnover_values = turnover_values[0:6]
    create_graph(years, turnover_values, "turnover")
    return turnover_values

def parser_get_net_margin():
    net_margin_values = []
    for i in table:
        if i.get_text() == "Marge nette":
            net_margins = i.find_next_siblings("td")
            for net_margin in net_margins:
                if net_margin.get_text() == '-':
                    net_margin_values.append(0)
                else:
                    net_margin_values.append(float(net_margin.get_text().replace(' ', '').replace('%', '').replace(',', '.')))
    net_margin_values = net_margin_values[0:6]
    create_graph(years, net_margin_values, "net_margin")
    return net_margin_values

def parser_get_net_result():
    net_results_values = []
    for i in table:
        if i.get_text() == "Résultat net1" or i.get_text() == "Résultat net":
            net_results = i.find_next_siblings("td")
            for net_result in net_results:
                if net_result.get_text() == '-':
                    net_results_values.append(0)
                else:
                    net_results_values.append(float(net_result.get_text().replace(' ', '').replace(',', '.')))
    net_results_values = net_results_values[0:6]
    create_graph(years, net_results_values, "net_result")
    return net_results_values

def parser_get_free_cash_flow():
    free_cash_flow_values = []
    for i in table:
        if i.get_text() == "Free Cash Flow1" or i.get_text() == "Free Cash Flow":
            free_cash_flows = i.find_next_siblings("td")
            for free_cash_flow in free_cash_flows:
                if free_cash_flow.get_text() == '-':
                    free_cash_flow_values.append(0)
                else:
                    free_cash_flow_values.append(float(free_cash_flow.get_text().replace(' ', '').replace(',', '.')))
    free_cash_flow_values = free_cash_flow_values[0:6]
    create_graph(years, free_cash_flow_values, "free_cash_flow")
    return free_cash_flow_values

def parser_get_operating_margin():
    operating_margin_values = []
    for i in table:
       if i.get_text() == "Marge d'exploitation":
            oms = i.find_next_siblings("td")
            for operating_margin in oms:
                if operating_margin.get_text() == '-':
                    operating_margin_values.append(0)
                else:
                    operating_margin_values.append(float(operating_margin.get_text().replace(' ', '').replace('%', '').replace(',', '.')))
    operating_margin_values = operating_margin_values[0:6]
    create_graph(years, operating_margin_values, "operating_margin")
    return operating_margin_values

def parser_get_operating_result():
    operating_result_values = []
    for i in table:
         if i.get_text() == "Résultat d'exploitation (EBIT)1":
            ors = i.find_next_siblings("td")
            for operating_result in ors:
                if operating_result.get_text() == '-':
                    operating_result_values.append(0)
                else:
                    operating_result_values.append(float(operating_result.get_text().replace(' ', '').replace('%', '').replace(',', '.')))
    operating_result_values = operating_result_values[0:6]
    create_graph(years, operating_result_values, "operating_result")
    return operating_result_values

def calculate_own_indicators():
    my_own_indicators = {}

    mean_yield = mean(yield_values_global[0:5])
    actual_yield = yield_values_global[-1]
    yield_result = actual_yield*100/mean_yield-100
    my_own_indicators["Yield Evolution"] = f'{yield_result}%'
    if (actual_yield > mean_yield):
        my_own_indicators["Yield Evaluation"] = "Underestimated"
    else:
        my_own_indicators["Yield Evaluation"] = "Overestimated"

    mean_per = mean(per_values_global[0:5])
    actual_per = per_values_global[-1]
    per_result = actual_per*100/mean_per-100
    my_own_indicators["PER Evolution"] = f'{per_result}%'
    if (actual_per < mean_per):
        my_own_indicators["PER Evaluation"] = "Underestimated"
    else:
        my_own_indicators["PER Evaluation"] = "Overestimated"
        
    print(my_own_indicators["Yield Evaluation"], my_own_indicators["Yield Evolution"])
    print(my_own_indicators["PER Evaluation"], my_own_indicators["PER Evolution"])

parser_initialize("https://www.zonebourse.com/cours/action/AIRBUS-SE-4637/fondamentaux/", "Airbus")
parser_get_bna()
parser_get_per()
parser_get_bvps()
parser_get_roe()
parser_get_roa()
parser_get_yield()
parser_get_operating_margin()
parser_get_operating_result()
parser_get_free_cash_flow()
parser_get_net_margin()
parser_get_net_result()
parser_get_turnover()
parser_get_capex()
calculate_own_indicators