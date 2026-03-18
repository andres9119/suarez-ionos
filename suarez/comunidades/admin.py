from django.contrib import admin
from django.utils.html import format_html
from .models import Comunidad, ImagenComunidad, GaleriaMunicipio, SeccionTexto
import os

class ImagenComunidadInline(admin.TabularInline):
    model = ImagenComunidad
    extra = 1

@admin.register(Comunidad)
class ComunidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug', 'tipo')
    list_filter = ('tipo',)
    search_fields = ('nombre', 'resena_cultural', 'slug')
    prepopulated_fields = {'slug': ('nombre',)}
    inlines = [ImagenComunidadInline]

@admin.register(SeccionTexto)
class SeccionTextoAdmin(admin.ModelAdmin):
    list_display = ('get_orden', 'titulo', 'fecha_creacion')
    list_filter = ('fecha_creacion',)
    list_editable = ('titulo',)
    search_fields = ('titulo', 'contenido')
    ordering = ('orden', '-fecha_creacion')
    
    fieldsets = (
        ('Información', {
            'fields': ('titulo', 'contenido', 'orden')
        }),
    )
    
    def get_orden(self, obj):
        return f"#{obj.orden}"
    get_orden.short_description = "Posición"

@admin.register(GaleriaMunicipio)
class GaleriaMunicipioAdmin(admin.ModelAdmin):
    list_display = ('get_imagen_preview', 'titulo', 'get_orden', 'fecha_creacion')
    list_filter = ('fecha_creacion',)
    list_editable = ('titulo',)
    search_fields = ('titulo', 'descripcion', 'slug')
    ordering = ('orden', '-fecha_creacion')
    
    fieldsets = (
        ('Imagen', {
            'fields': ('imagen',),
            'description': 'Carga tu imagen. El título y slug se generarán automáticamente del nombre del archivo.'
        }),
        ('Información (Auto-Generada)', {
            'fields': ('titulo', 'slug'),
            'classes': ('collapse',),
            'description': 'Se generan automáticamente. Puedes editar el título si lo deseas.'
        }),
        ('Orden', {
            'fields': ('orden',),
            'description': 'Número menor = primero en la galería'
        }),
        ('Descripción (Opcional)', {
            'fields': ('descripcion',),
            'classes': ('collapse',),
            'description': 'Añade una descripción si deseas (no será visible en la galería pública)'
        }),
        ('Thumbnail (Auto-Generado)', {
            'fields': ('imagen_thumbnail',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('imagen_thumbnail', 'slug')
    
    def get_orden(self, obj):
        return f"#{obj.orden}"
    get_orden.short_description = "Pos"
    
    def get_imagen_preview(self, obj):
        if obj.imagen:
            return format_html('✓ Imagen <br><small>{}</small>', 
                             os.path.basename(obj.imagen.name)[:30])
        return "Sin imagen"
    get_imagen_preview.short_description = "Preview"
