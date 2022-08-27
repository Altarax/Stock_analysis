from parsers.bsoup_parser import *
from utils import STOCK_LIST

for i in STOCK_LIST:
        name = i[0]
        isin = i[1]
        market = i[-1]
        symbol = i[2]

        temp = market.split(',')
        market = temp[0]
        
        if "amsterdam" in str(market).lower():
                symbol+=".AS"
        elif "brussels" in str(market).lower():
                symbol+=".BR"
        elif "dublin" in str(market).lower():
                symbol+=".IR"
        elif "lisbon" in str(market).lower():
                symbol+=".LS"
        elif "oslo" in str(market).lower():
                symbol+=".OL"
        elif "paris" in str(market).lower():
                symbol+=".PA"

        if parser_get_financials_url(isin) == None:
            print(name)
        else:
            print(parser_get_financials_url(isin))