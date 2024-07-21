from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('calculate/', views.calculate, name='calculate'),
    path('download-history/', views.download_history, name='download_history'),  # PDF download URL
]
