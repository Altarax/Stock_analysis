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
    second_stock = request.POST.get('second-stock')
    Stock.objects.create(name=first_stock, symbol=first_stock)
    Stock.objects.create(name=second_stock, symbol=second_stock)
    Stock.objects.all()[0].get_price_hist()
    Stock.objects.all()[1].get_price_hist()
    Stock.objects.all()[0].get_dividend_hist()
    Stock.objects.all()[1].get_dividend_hist()
    Stock.objects.all()[0].get_fundamentals_data()
    Stock.objects.all()[1].get_fundamentals_data()
    return redirect('home')