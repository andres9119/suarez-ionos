from django.shortcuts import render
from .models import Video, ImagenGaleria, EventoDestacado, BannerPrincipal

from django.db.models import Q
from noticias.models import Noticia
from experiencias_cafeteras.models import ExperienciaCafetera
from comunidades.models import Comunidad
from documentos.models import DocumentoPublico

def home(request):
    banner = BannerPrincipal.objects.filter(activo=True).first()
    videos = Video.objects.all()[:3]
    imagenes_carousel = ImagenGaleria.objects.filter(es_destacada=True)
    eventos = EventoDestacado.objects.all()[:3]
    
    return render(request, 'inicio/home.html', {
        'banner': banner,
        'videos': videos,
        'imagenes': imagenes_carousel,
        'eventos': eventos
    })

def historia(request):
    return render(request, 'inicio/historia.html')

def buscar(request):
    query = request.GET.get('q', '')
    filter_type = request.GET.get('type', 'all')
    
    resultados_noticias = []
    resultados_cafe = []
    resultados_comul = []
    resultados_docs = []
    
    if query:
        if filter_type in ['all', 'noticias']:
            resultados_noticias = Noticia.objects.filter(
                Q(titulo__icontains=query) | Q(contenido__icontains=query)
            )
            
        if filter_type in ['all', 'experiencias']:
            resultados_cafe = ExperienciaCafetera.objects.filter(
                Q(titulo__icontains=query) | Q(historia__icontains=query)
            )
            
        if filter_type in ['all', 'comunidades']:
            resultados_comul = Comunidad.objects.filter(
                Q(nombre__icontains=query) | Q(resena_cultural__icontains=query)
            )
            
        if filter_type in ['all', 'documentos']:
            resultados_docs = DocumentoPublico.objects.filter(
                Q(titulo__icontains=query)
            )
        
    return render(request, 'inicio/buscar.html', {
        'query': query,
        'filter_type': filter_type,
        'noticias': resultados_noticias,
        'experiencias': resultados_cafe,
        'comunidades': resultados_comul,
        'documentos': resultados_docs,
        'total_resultados': len(resultados_noticias) + len(resultados_cafe) + len(resultados_comul) + len(resultados_docs)
    })

