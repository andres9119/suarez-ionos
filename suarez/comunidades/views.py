from django.shortcuts import render, get_object_or_404
from .models import Comunidad, GaleriaMunicipio, SeccionTexto

def lista_comunidades(request):
    # Secciones de texto secuenciales
    secciones = SeccionTexto.objects.all()
    # Galería del municipio
    galeria = GaleriaMunicipio.objects.all()
    return render(request, 'comunidades/lista.html', {
        'secciones': secciones,
        'galeria': galeria
    })

def detalle_comunidad(request, slug):
    comunidad = get_object_or_404(Comunidad, slug=slug)
    return render(request, 'comunidades/detalle.html', {'comunidad': comunidad})
