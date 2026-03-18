from django.shortcuts import render
from .models import Producto


def lista_productos(request):
    productos = Producto.objects.all().order_by('-fecha_creacion')
    whatsapp_numero = '+57 311 794 4573'
    whatsapp_url = f'https://wa.me/573117944573?text=Hola,%20me%20interesa%20conocer%20m%C3%A1s%20sobre%20sus%20productos%20y%20servicios'
    
    return render(request, 'productos/lista.html', {
        'productos': productos,
        'whatsapp_numero': whatsapp_numero,
        'whatsapp_url': whatsapp_url
    })
