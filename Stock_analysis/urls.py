from django.contrib import admin
from django.urls import path
import stocks.views as views

urlpatterns = [
    path('', views.index, name="home"),
    path('visualize-data/', views.visualize_data, name="visualize-data"),
    path('admin/', admin.site.urls),
]
