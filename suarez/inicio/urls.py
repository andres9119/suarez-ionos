from django.urls import path
from . import views

app_name = 'inicio'

urlpatterns = [
    path('', views.home, name='home'),
    path('buscar/', views.buscar, name='buscar'),
    path('historia-suarez-cauca/', views.historia, name='historia'),
    path('cafe-de-suarez-cauca/', views.cafe_suarez_cauca, name='cafe_suarez_cauca'),
    path('familias-cafeteras-suarez-cauca/', views.familias_cafeteras, name='familias_cafeteras'),
    path('turismo-cafetero-suarez-cauca/', views.turismo_cafetero, name='turismo_cafetero'),
]
