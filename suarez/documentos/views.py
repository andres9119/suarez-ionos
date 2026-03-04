from django.shortcuts import render
from .models import DocumentoPublico, CategoriaDocumento
from django.core.paginator import Paginator

def lista_documentos(request):
    categorias = CategoriaDocumento.objects.all()
    documentos_list = DocumentoPublico.objects.all().order_by('-fecha_subida')
    
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        documentos_list = documentos_list.filter(categoria__id=categoria_id)
    
    paginator = Paginator(documentos_list, 10) # 10 documents per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
        
    return render(request, 'documentos/lista.html', {
        'categorias': categorias,
        'documentos': page_obj,
        'categoria_activa': int(categoria_id) if categoria_id else None
    })
