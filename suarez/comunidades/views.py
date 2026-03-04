from django.shortcuts import render, get_object_or_404
from .models import Comunidad

def lista_comunidades(request):
    comunidades = Comunidad.objects.all()
    return render(request, 'comunidades/lista.html', {'comunidades': comunidades})

def detalle_comunidad(request, slug):
    comunidad = get_object_or_404(Comunidad, slug=slug)
    return render(request, 'comunidades/detalle.html', {'comunidad': comunidad})
