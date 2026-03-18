from django.contrib import admin
from .models import Comunidad, ImagenComunidad, GaleriaMunicipio, SeccionTexto

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
    prepopulated_fields = {'slug': ('titulo',)}
    ordering = ('orden', '-fecha_creacion')
    
    fieldsets = (
        ('Información', {
            'fields': ('titulo', 'slug', 'orden')
        }),
        ('Imagen', {
            'fields': ('imagen', 'imagen_thumbnail')
        }),
        ('Descripción (Opcional)', {
            'fields': ('descripcion',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('imagen_thumbnail',)
    
    def get_orden(self, obj):
        return f"#{obj.orden}"
    get_orden.short_description = "Posición"
    
    def get_imagen_preview(self, obj):
        if obj.imagen:
            return f"✓ Imagen"
        return "Sin imagen"
    get_imagen_preview.short_description = "Estado"
