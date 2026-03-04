from django.shortcuts import render, get_object_or_404
from .models import Noticia

from django.core.paginator import Paginator

def lista_noticias(request):
    noticias_list = Noticia.objects.all().order_by('-fecha_publicacion')
    paginator = Paginator(noticias_list, 9) # Show 9 news per page
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'noticias/lista.html', {'noticias': page_obj})

def detalle_noticia(request, slug):
    noticia = get_object_or_404(Noticia, slug=slug)
    return render(request, 'noticias/detalle.html', {'noticia': noticia})
