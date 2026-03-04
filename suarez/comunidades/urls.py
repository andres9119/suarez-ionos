from django.urls import path
from . import views

app_name = 'comunidades'

urlpatterns = [
    path('', views.lista_comunidades, name='lista'),
    path('<slug:slug>/', views.detalle_comunidad, name='detalle'),
]
