# Find the financials data of the company on Zonebourse with beautiful soup
from asyncio.windows_events import NULL
from tkinter import font
from bs4 import BeautifulSoup as bs
import requests
import matplotlib.pyplot as plt
import random

# Colors list for lines in plot
colors_list = ["r", "b", "g", "k", "m", "y", "c"]

def add_value_label(x_list,y_list):
    for i in range(len(x_list)):
        plt.text(i, y_list[i], y_list[i], fontdict={'weight':'bold', 'size':15}, ha='center')

def save_graphs(financials_url, company_name):
    financials_page = requests.get(financials_url)
    soup = bs(financials_page.content, 'html.parser')

    years = [soup.find('td', class_=f"bc2Y tableCol{i}").get_text() for i in range(0,8)]

    table_list = soup.find_all('table',{'class': 'BordCollapseYear2'})
    table_semesters = table_list[2]
    temp = table_semesters.tr.find_all('td')
    semesters = [t.get_text() for t in temp]
    del semesters[0]

    roe_values = []
    roa_values = []
    per_values = []
    bna_values = []
    bvps_values = []
    yield_values = []
    turnover_values = []
    net_margin_values = []
    net_results_values = []
    free_cash_flow_values = []
    operating_margin_values = []
    operating_result_values = []

    table = soup.find_all('td', attrs={'class':'bc2T'})
    for i in table:
        if i.get_text() == "PER":
            pers = i.find_next_siblings("td")
            for per in pers:
                if per.get_text() == '-':
                    per_values.append(0)
                else:
                    per_values.append(float(per.get_text().replace(' ', '').replace('x', '').replace(',', '.')))
        if i.get_text() == "Rendement":
            yields = i.find_next_siblings("td")
            for y in yields:
                if y.get_text() == '-':
                    yield_values.append(0)
                else:
                    yield_values.append(float(y.get_text().replace(' ', '').replace('%', '').replace(',', '.')))
        if i.get_text() == "Chiffre d'affaires1":
            turnovers = i.find_next_siblings("td")
            for turnover in turnovers:
                if turnover.get_text() == '-':
                    turnover_values.append(0)
                else:
                    turnover_values.append(int(turnover.get_text().replace(' ', '')))
        if i.get_text() == "Résultat d'exploitation (EBIT)1":
            ors = i.find_next_siblings("td")
            for operating_result in ors:
                if operating_result.get_text() == '-':
                    operating_result_values.append(0)
                else:
                    operating_result_values.append(float(operating_result.get_text().replace(' ', '').replace('%', '').replace(',', '.')))
        if i.get_text() == "Marge d'exploitation":
            oms = i.find_next_siblings("td")
            for operating_margin in oms:
                if operating_margin.get_text() == '-':
                    operating_margin_values.append(0)
                else:
                    operating_margin_values.append(float(operating_margin.get_text().replace(' ', '').replace('%', '').replace(',', '.')))
        if i.get_text() == "Résultat net1":
            net_results = i.find_next_siblings("td")
            for net_result in net_results:
                if net_result.get_text() == '-':
                    net_results_values.append(0)
                else:
                    net_results_values.append(float(net_result.get_text().replace(' ', '').replace(',', '.')))
        if i.get_text() == "BNA2":
            bnas = i.find_next_siblings("td")
            for bna in bnas:
                if bna.get_text() == '-':
                    bna_values.append(0)
                else:
                    bna_values.append(float(bna.get_text().replace(' ', '').replace(',', '.')))
        if i.get_text() == "Free Cash Flow1" or i.get_text() == "Free Cash Flow":
            free_cash_flows = i.find_next_siblings("td")
            for free_cash_flow in free_cash_flows:
                if free_cash_flow.get_text() == '-':
                    free_cash_flow_values.append(0)
                else:
                    free_cash_flow_values.append(float(free_cash_flow.get_text().replace(' ', '').replace(',', '.')))
        if i.get_text() == "ROE (RN / Capitaux Propres)":
            roes = i.find_next_siblings("td")
            for roe in roes:
                if roe.get_text() == '-':
                    roe_values.append(0)
                else:
                    roe_values.append(float(roe.get_text().replace(' ', '').replace('%', '').replace(',', '.')))
        if i.get_text() == "ROA (RN / Total Actif)":
            roas = i.find_next_siblings("td")
            for roa in roas:
                if roa.get_text() == '-':
                    roa_values.append(0)
                else:
                    roa_values.append(float(roa.get_text().replace(' ', '').replace('%', '').replace(',', '.')))
        if i.get_text() == "BVPS (Actif net par Action)2":
            bvpss = i.find_next_siblings("td")
            for bvps in bvpss:
                if bvps.get_text() == '-':
                    bvps_values.append(0)
                else:
                    bvps_values.append(float(bvps.get_text().replace(' ', '').replace(',', '.')))
        if i.get_text() == "Marge Nette":
            net_margins = i.find_next_siblings("td")
            for net_margin in net_margins:
                if net_margin.get_text() == '-':
                    net_margin_values.append(0)
                else:
                    net_margin_values.append(float(net_margin.get_text().replace(' ', '').replace('%', '').replace(',', '.')))

    if len(bna_values) > 8:
        del bna_values[7:-1]

    if len(free_cash_flow_values) > 8:
        del free_cash_flow_values[7:-1]

    if len(operating_margin_values) > 8:
        del operating_margin_values[0:8]

    if len(operating_result_values) > 21:
        del operating_result_values[0:8]

    if len(net_results_values) > 21:
        del net_results_values[0:8]

    if len(turnover_values) > 21:
        del turnover_values[0:8]

    plt.figure(figsize=(18, 8))
    plt.grid(True)
    plt.bar(years, roe_values)
    add_value_label(years, roe_values)
    plt.title(f"Roe Values")
    plt.xlabel('Date')
    plt.ylabel(f'Roe')
    plt.savefig(f'stocks/static/images/roe_values_{company_name}.png', bbox_inches='tight')

    plt.figure(figsize=(18, 8))
    plt.grid(True)
    plt.bar(years, roa_values)
    add_value_label(years, roa_values)
    plt.title(f"Roa Values")
    plt.xlabel('Date')
    plt.ylabel(f'Roa')
    plt.savefig(f'stocks/static/images/roa_values_{company_name}.png', bbox_inches='tight')

    plt.figure(figsize=(18, 8))
    plt.grid(True)
    plt.bar(years, per_values)
    add_value_label(years, per_values)
    plt.title(f"Per Values")
    plt.xlabel('Date')
    plt.ylabel(f'Per')
    plt.savefig(f'stocks/static/images/per_values_{company_name}.png', bbox_inches='tight')

    plt.figure(figsize=(18, 8))
    plt.grid(True)
    plt.bar(years, bna_values)
    add_value_label(years, bna_values)
    plt.title(f"BNA Values")
    plt.xlabel('Date')
    plt.ylabel(f'BNA')
    plt.savefig(f'stocks/static/images/bna_values_{company_name}.png', bbox_inches='tight')

    plt.figure(figsize=(18, 8))
    plt.grid(True)
    plt.bar(years, bvps_values)
    add_value_label(years, bvps_values)
    plt.title(f"BVPS Values")
    plt.xlabel('Date')
    plt.ylabel(f'BVPS')
    plt.savefig(f'stocks/static/images/bvps_values_{company_name}.png', bbox_inches='tight')

    plt.figure(figsize=(18, 8))
    plt.grid(True)
    plt.bar(years, yield_values)
    add_value_label(years, yield_values)
    plt.title(f"Yield Values")
    plt.xlabel('Date')
    plt.ylabel(f'Yield')
    plt.savefig(f'stocks/static/images/yield_values_{company_name}.png', bbox_inches='tight')

    plt.figure(figsize=(18, 8))
    plt.grid(True)
    plt.bar(semesters, turnover_values)
    add_value_label(semesters, turnover_values)
    plt.title(f"Turnover Values")
    plt.xlabel('Date')
    plt.ylabel(f'Turnover')
    plt.savefig(f'stocks/static/images/turnover_values_{company_name}.png', bbox_inches='tight')
    
    plt.figure(figsize=(18, 8))
    plt.grid(True)
    plt.bar(semesters, net_results_values)
    add_value_label(semesters, net_results_values)
    plt.title(f"Net result Values")
    plt.xlabel('Date')
    plt.ylabel(f'Net result (€)')
    plt.savefig(f'stocks/static/images/net_result_values_{company_name}.png', bbox_inches='tight')

    plt.figure(figsize=(18, 8))
    plt.grid(True)
    plt.bar(years, free_cash_flow_values)
    add_value_label(years, free_cash_flow_values)
    plt.title(f"Free Cash Flow Values")
    plt.xlabel('Date')
    plt.ylabel(f'Free Cash Flow')
    plt.savefig(f'stocks/static/images/free_cash_flow_values_{company_name}.png', bbox_inches='tight')

    plt.figure(figsize=(18, 8))
    plt.grid(True)
    plt.bar(semesters, operating_margin_values)
    add_value_label(semesters, operating_margin_values)
    plt.title(f"Operating Margin Values")
    plt.xlabel('Date')
    plt.ylabel(f'Operating Margin')
    plt.savefig(f'stocks/static/images/operating_margin_values_{company_name}.png', bbox_inches='tight')

    plt.figure(figsize=(18, 8))
    plt.grid(True)
    plt.bar(semesters, operating_result_values, label=company_name, color=random.choice(colors_list))
    add_value_label(semesters, operating_result_values)
    plt.title(f"Operating Results Values")
    plt.xlabel('Date')
    plt.ylabel(f'Operating Result')
    plt.savefig(f'stocks/static/images/operating_result_values_{company_name}.png', bbox_inches='tight')

    plt.figure(figsize=(18, 8))
    plt.grid(True)
    plt.bar(semesters, operating_result_values, label=company_name, color=random.choice(colors_list))
    add_value_label(semesters, operating_result_values)
    plt.title(f"Net Marging Values")
    plt.xlabel('Date')
    plt.ylabel(f'Net Margin (%)')
    plt.savefig(f'stocks/static/images/net_margin_values_{company_name}.png', bbox_inches='tight')

save_graphs("https://www.zonebourse.com/cours/action/AIRBUS-SE-4637/fondamentaux/", "Coface")