from django.urls import path
from . import views

app_name = 'inicio'

urlpatterns = [
    path('', views.home, name='home'),
    path('buscar/', views.buscar, name='buscar'),
    path('historia-suarez-cauca/', views.historia, name='historia'),
]
