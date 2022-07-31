from django.http import HttpResponse
from django.shortcuts import render, redirect
from matplotlib.style import context
from stocks.utils import *
from stocks.models import *
import os

# Create your views here.
def index(request):
    stocks = {"Stocks": Stock.objects.order_by("name")}
    images = os.listdir('stocks/static/images/')
    return render(request, 'stocks/index.html', context={"SBF120": SBF120, "stocks": stocks["Stocks"], "images": images})


def visualize_data(request):
    Stock.objects.all().delete()
    first_stock = request.POST.get('first-stock')
    first_stock = Stock(name=first_stock, symbol=first_stock)
    second_stock = request.POST.get('second-stock')
    second_stock = Stock(name=second_stock, symbol=second_stock)
    first_stock.get_price_hist()
    first_stock.get_dividend_hist()
    first_stock.initialize_fundamentals_data()
    second_stock.get_price_hist()
    second_stock.get_dividend_hist()
    second_stock.initialize_fundamentals_data()
    first_stock.get_all_financials_data()
    second_stock.get_all_financials_data()

    return redirect('home')