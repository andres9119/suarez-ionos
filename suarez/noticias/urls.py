from django.urls import path
from . import views

app_name = 'noticias'

urlpatterns = [
    path('', views.lista_noticias, name='lista'),
    path('<slug:slug>/', views.detalle_noticia, name='detalle'),
]
