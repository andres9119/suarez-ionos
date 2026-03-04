from django.urls import path
from . import views

app_name = 'experiencias_cafeteras'

urlpatterns = [
    path('', views.lista_experiencias, name='lista'),
    path('<slug:slug>/', views.detalle_experiencia, name='detalle'),
]
