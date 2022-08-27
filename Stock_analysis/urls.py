from django.contrib import admin
from django.urls import path
import stocks.views as views

urlpatterns = [
    path('', views.index, name="home"),
    path('visualize-data/', views.visualize_data, name="visualize-data"),
    path('last-news/', views.visualize_news, name="last-news"),
    path('admin/', admin.site.urls),
]
