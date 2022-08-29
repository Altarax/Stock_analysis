# Find the financials data of the company on Zonebourse with beautiful soup
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup as bs
from numpy import mean

# Colors list for lines in plot
colors_list = ["r", "b", "g", "k", "m", "y", "c"]

# Global values
years = []
semesters = []
soup_global = bs()
table = []
company_name_global = ""
yield_values_global = []
per_values_global = []
bna_values_global = []
bvps_values_global = []
last_table = []
second_table = []


def add_value_label(x_list, y_list):
    for i in range(len(x_list)):
        plt.text(
            i,
            y_list[i] // 2,
            y_list[i],
            fontdict={"weight": "bold", "size": 15},
            ha="center",
        )


def create_graph(x, values_list, value_name):
    plt.figure(figsize=(18, 8))
    plt.grid(True)
    plt.bar(x, values_list)
    add_value_label(x, values_list)
    plt.title(f"{value_name.capitalize()} Values")
    plt.xlabel("Date")
    plt.ylabel(f"{value_name.capitalize()}")
    plt.savefig(
        f"stocks/static/images/{value_name}_values_{company_name_global}.png",
        bbox_inches="tight",
    )


def parser_get_financials_url(isin):
    stock_page = requests.get(
        f"https://www.zonebourse.com/recherche/instruments?q={str(isin)}"
    )
    soup = bs(stock_page.content, "html.parser")
    stock_list = soup.find_all("td", {"class": "table-child--left"})

    t = [i.find("a") for i in stock_list]
    for line in t:
        temp = str(line).split('"')
        for j in temp:
            if "/cours" in j:
                return "https://www.zonebourse.com" + j + "fondamentaux/"


def parser_initialize(financials_url, company_name):
    global company_name_global
    global years
    global semesters
    global table
    global last_table
    global second_table
    global soup_global
    company_name_global = company_name
    financials_page = requests.get(financials_url)
    soup = bs(financials_page.content, "html.parser")
    soup_global = soup
    table_list = soup.find_all("table", {"class": "BordCollapseYear2"})

    temp = table_list[0].tr.find_all("td")
    years = [t.get_text() for t in temp]
    del years[0]

    table_semesters = table_list[2]
    temp = table_semesters.tr.find_all("td")
    semesters = [t.get_text() for t in temp]
    del semesters[0]

    table = soup.find_all("td", attrs={"class": "bc2T"})
    temp = table_list[-1].tr.find_all("td")
    last_table = [t.get_text() for t in temp]
    del last_table[0]

    table = soup.find_all("td", attrs={"class": "bc2T"})
    temp = table_list[1].tr.find_all("td")
    second_table = [t.get_text() for t in temp]
    del second_table[0]


def parser_get_last_table():
    return last_table


def parser_get_second_table():
    return second_table


def parser_get_years():
    return years


def parser_get_bna():
    global bna_values_global
    bna_values = []
    for i in table:
        if i.get_text() == "BNA2":
            bnas = i.find_next_siblings("td")
            for bna in bnas:
                if bna.get_text() == "-":
                    bna_values.append(0)
                else:
                    bna_values.append(
                        round(
                            float(bna.get_text().replace(" ", "").replace(",", ".")), 2
                        )
                    )
    bna_values = bna_values[0 : len(second_table)]
    bna_values_global = bna_values
    # create_graph(second_table, bna_values, "bna")
    return bna_values


def parser_get_per():
    global bna_values_global
    per_values = []
    for i in table:
        if i.get_text() == "PER":
            pers = i.find_next_siblings("td")
            for per in pers:
                if per.get_text() == "-":
                    per_values.append(0)
                else:
                    per_values.append(
                        round(
                            float(
                                per.get_text()
                                .replace(" ", "")
                                .replace(",", ".")
                                .replace("x", "")
                            ),
                            2,
                        )
                    )
    per_values = per_values[0 : len(years)]
    calculated_per = []
    for i1, i2 in zip(per_values, bna_values_global):
        calculated_per.append(i1 * i2)
    per_values = calculated_per
    global per_values_global
    per_values_global = per_values
    # create_graph(years, per_values, "per")
    return per_values


def parser_get_roe():
    roe_values = [] = []
    for i in table:
        if i.get_text() == "ROE (RN / Capitaux Propres)":
            roes = i.find_next_siblings("td")
            for roe in roes:
                if roe.get_text() == "-":
                    roe_values.append(0)
                else:
                    roe_values.append(
                        float(
                            roe.get_text()
                            .replace(" ", "")
                            .replace("%", "")
                            .replace(",", ".")
                        )
                    )
    roe_values = roe_values[0 : len(last_table)]
    # create_graph(last_table, roe_values, "roe")
    return roe_values


def parser_get_roa():
    roa_values = []
    for i in table:
        if i.get_text() == "ROA (RN / Total Actif)":
            roas = i.find_next_siblings("td")
            for roa in roas:
                if roa.get_text() == "-":
                    roa_values.append(0)
                else:
                    roa_values.append(
                        float(
                            roa.get_text()
                            .replace(" ", "")
                            .replace("%", "")
                            .replace(",", ".")
                        )
                    )
    roa_values = roa_values[0 : len(last_table)]
    # create_graph(last_table, roa_values, "roa")
    return roa_values


def parser_get_bvps():
    global bvps_values_global
    bvps_values = []
    for i in table:
        if "BVPS" in i.get_text():
            bvpss = i.find_next_siblings("td")
            for bvps in bvpss:
                if bvps.get_text() == "-":
                    bvps_values.append(0)
                else:
                    bvps_values.append(
                        float(bvps.get_text().replace(" ", "").replace(",", "."))
                    )
    bvps_values = bvps_values[0 : len(last_table)]
    bvps_values_global = bvps_values
    # create_graph(last_table, bvps_values, "bvps")
    return bvps_values


def parser_get_yield():
    yield_values = []
    for i in table:
        if i.get_text() == "Rendement":
            yields = i.find_next_siblings("td")
            for y in yields:
                if y.get_text() == "-":
                    yield_values.append(0)
                else:
                    yield_values.append(
                        float(
                            y.get_text()
                            .replace(" ", "")
                            .replace("%", "")
                            .replace(",", ".")
                        )
                    )
    yield_values = yield_values[0 : len(years)]
    global yield_values_global
    yield_values_global = yield_values
    # create_graph(years, yield_values, "yield")
    return yield_values


def parser_get_capex():
    capex_values = []
    for i in table:
        if i.get_text() == "Capex1" or i.get_text() == "Capex":
            capexs = i.find_next_siblings("td")
            for capex in capexs:
                if capex.get_text() == "-":
                    capex_values.append(0)
                else:
                    capex_values.append(
                        float(capex.get_text().replace(" ", "").replace(",", "."))
                    )
    capex_values = capex_values[0 : len(last_table)]
    # create_graph(last_table, capex_values, "capex")
    return capex_values


def parser_get_turnover():
    turnover_values = []
    for i in table:
        if i.get_text() == "Chiffre d'affaires1":
            turnovers = i.find_next_siblings("td")
            for turnover in turnovers:
                if turnover.get_text() == "-":
                    turnover_values.append(0)
                else:
                    turnover_values.append(
                        float(turnover.get_text().replace(" ", "").replace(",", "."))
                    )
    turnover_values = turnover_values[0 : len(years)]
    # create_graph(years, turnover_values, "turnover")
    return turnover_values


def parser_get_net_margin():
    net_margin_values = []
    for i in table:
        if i.get_text() == "Marge nette":
            net_margins = i.find_next_siblings("td")
            for net_margin in net_margins:
                if net_margin.get_text() == "-":
                    net_margin_values.append(0)
                else:
                    net_margin_values.append(
                        float(
                            net_margin.get_text()
                            .replace(" ", "")
                            .replace("%", "")
                            .replace(",", ".")
                        )
                    )
    net_margin_values = net_margin_values[0 : len(years)]
    # create_graph(years, net_margin_values, "net_margin")
    return net_margin_values


def parser_get_net_result():
    net_results_values = []
    for i in table:
        if i.get_text() == "Résultat net1" or i.get_text() == "Résultat net":
            net_results = i.find_next_siblings("td")
            for net_result in net_results:
                if net_result.get_text() == "-":
                    net_results_values.append(0)
                else:
                    net_results_values.append(
                        float(net_result.get_text().replace(" ", "").replace(",", "."))
                    )
    net_results_values = net_results_values[0 : len(years)]
    # create_graph(years, net_results_values, "net_result")
    return net_results_values


def parser_get_free_cash_flow():
    free_cash_flow_values = []
    for i in table:
        if i.get_text() == "Free Cash Flow1" or i.get_text() == "Free Cash Flow":
            free_cash_flows = i.find_next_siblings("td")
            for free_cash_flow in free_cash_flows:
                if free_cash_flow.get_text() == "-":
                    free_cash_flow_values.append(0)
                else:
                    free_cash_flow_values.append(
                        float(
                            free_cash_flow.get_text().replace(" ", "").replace(",", ".")
                        )
                    )
    free_cash_flow_values = free_cash_flow_values[0 : len(last_table)]
    # create_graph(last_table, free_cash_flow_values, "free_cash_flow")
    return free_cash_flow_values


def parser_get_operating_margin():
    operating_margin_values = []
    for i in table:
        if i.get_text() == "Marge d'exploitation":
            oms = i.find_next_siblings("td")
            for operating_margin in oms:
                if operating_margin.get_text() == "-":
                    operating_margin_values.append(0)
                else:
                    operating_margin_values.append(
                        float(
                            operating_margin.get_text()
                            .replace(" ", "")
                            .replace("%", "")
                            .replace(",", ".")
                        )
                    )
    operating_margin_values = operating_margin_values[0 : len(years)]
    # create_graph(years, operating_margin_values, "operating_margin")
    return operating_margin_values


def parser_get_operating_result():
    operating_result_values = []
    for i in table:
        if i.get_text() == "Résultat d'exploitation (EBIT)1":
            ors = i.find_next_siblings("td")
            for operating_result in ors:
                if operating_result.get_text() == "-":
                    operating_result_values.append(0)
                else:
                    operating_result_values.append(
                        float(
                            operating_result.get_text()
                            .replace(" ", "")
                            .replace("%", "")
                            .replace(",", ".")
                        )
                    )
    operating_result_values = operating_result_values[0 : len(years)]
    # create_graph(years, operating_result_values, "operating_result")
    return operating_result_values


def parser_get_debt():
    debt_values = []
    for i in table:
        if "Dette Nette" in i.get_text():
            debts = i.find_next_siblings("td")
            for debt in debts:
                if debt.get_text() == "-":
                    debt_values.append(0)
                else:
                    debt_values.append(
                        float(debt.get_text().replace(" ", "").replace(",", "."))
                    )
    debt_values = debt_values[0 : len(last_table)]
    # create_graph(last_table, debt_values, "debt")
    return debt_values


def parser_get_treasury():
    treasury_values = []
    for i in table:
        if i.get_text() == "Trésorerie Nette1" or i.get_text() == "Trésorerie Nette":
            treasurys = i.find_next_siblings("td")
            for treasury in treasurys:
                if treasury.get_text() == "-":
                    treasury_values.append(0)
                else:
                    treasury_values.append(
                        float(treasury.get_text().replace(" ", "").replace(",", "."))
                    )
    treasury_values = treasury_values[0 : len(last_table)]
    # create_graph(last_table, treasury_values, "treasury")
    return treasury_values


def parser_get_equity():
    equity_values = []
    for i in table:
        if i.get_text() == "Capitaux Propres1" or i.get_text() == "Capitaux Propres":
            equities = i.find_next_siblings("td")
            for equity in equities:
                if equity.get_text() == "-":
                    equity_values.append(0)
                else:
                    equity_values.append(
                        float(equity.get_text().replace(" ", "").replace(",", "."))
                    )
    equity_values = equity_values[0 : len(last_table)]
    # create_graph(last_table, equity_values, "equity")
    return equity_values


def parser_get_cap():
    cap_values = []
    for i in table:
        if i.get_text() == "Capitalisation1" or i.get_text() == "Capitalisation":
            caps = i.find_next_siblings("td")
            for cap in caps:
                if cap.get_text() == "-":
                    cap_values.append(0)
                else:
                    cap_values.append(
                        float(cap.get_text().replace(" ", "").replace(",", "."))
                    )
    cap_values = cap_values[0 : len(years)]
    # create_graph(years, cap_values, "capitalization")
    return cap_values


def parser_get_leverage():
    leverage_values = []
    for i in table:
        if "Leverage" in i.get_text():
            leverages = i.find_next_siblings("td")
            for leverage in leverages:
                if leverage.get_text() == "-":
                    leverage_values.append(0)
                else:
                    leverage_values.append(
                        float(
                            leverage.get_text()
                            .replace(" ", "")
                            .replace("x", "")
                            .replace(",", ".")
                        )
                    )
    leverage_values = leverage_values[0 : len(last_table)]
    # create_graph(last_table, leverage_values, "leverage")
    return leverage_values


def parser_get_floating_stock():
    try:
        value = soup_global.find("td", text="Flottant").find_next_sibling("td").text
        value = float(value.replace(" ", "").replace("%", "").replace(",", "."))
    except:
        value = 0
    return value


def parser_get_pbr():
    global bvps_values_global
    stock_values = []
    bpr_values = []
    for i in table:
        if "Cours de référence" in i.get_text():
            values = i.find_next_siblings("td")
            for s in values:
                if s.get_text() == "-":
                    stock_values.append(0)
                else:
                    stock_values.append(
                        float(s.get_text().replace(" ", "").replace(",", "."))
                    )
    stock_values = stock_values[0 : len(years)]
    try:
        bpr_values = [i / j for i, j in zip(stock_values, bvps_values_global)]
    except:
        bpr_values = 0
    return bpr_values


def calculate_own_indicators():
    my_own_indicators = {}

    mean_yield = mean(yield_values_global[0:5])
    actual_yield = yield_values_global[-1]
    yield_result = actual_yield * 100 / mean_yield - 100
    my_own_indicators["Yield Evolution"] = f"{yield_result}%"
    if actual_yield > mean_yield:
        my_own_indicators["Yield Evaluation"] = "Underestimated"
    else:
        my_own_indicators["Yield Evaluation"] = "Overestimated"

    mean_per = mean(per_values_global[0:5])
    actual_per = per_values_global[-1]
    per_result = actual_per * 100 / mean_per - 100
    my_own_indicators["PER Evolution"] = f"{per_result}%"
    if actual_per < mean_per:
        my_own_indicators["PER Evaluation"] = "Underestimated"
    else:
        my_own_indicators["PER Evaluation"] = "Overestimated"

    return my_own_indicators
