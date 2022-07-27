from django.http import HttpResponse
from django.shortcuts import render, redirect
from stocks.utils import *
from stocks.models import *


# Create your views here.
def index(request):
    stocks = {"Stocks": Stock.objects.order_by("name")}
    return render(request, 'stocks/index.html', context={"SBF120": SBF120, "stocks": stocks["Stocks"]})


def visualize_data(request):
    first_stock = request.POST.get('first-stock')
    second_stock = request.POST.get('second-stock')
    Stock.objects.create(name=first_stock, symbol=first_stock)
    Stock.objects.create(name=second_stock, symbol=second_stock)
    print(Stock.name)
    return redirect('home')