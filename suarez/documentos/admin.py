from django.contrib import admin
from .models import CategoriaDocumento, DocumentoPublico

@admin.register(CategoriaDocumento)
class CategoriaDocumentoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(DocumentoPublico)
class DocumentoPublicoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'fecha_subida')
    list_filter = ('categoria', 'fecha_subida')
    search_fields = ('titulo', 'descripcion')
