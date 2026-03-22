from django.contrib import admin
from .models import ExperienciaCafetera, ContenidoExperiencia

class ContenidoExperienciaInline(admin.StackedInline):
    model = ContenidoExperiencia
    extra = 3
    fields = ('tipo', 'orden', 'titulo_bloque', 'contenido_texto', 'url_video', 'imagen', 'descripcion_imagen')
    ordering = ('orden',)
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            ('Configuración del Bloque', {
                'fields': ('tipo', 'orden', 'titulo_bloque')
            }),
            ('Contenido de Texto', {
                'fields': ('contenido_texto',),
            }),
            ('Contenido de Video', {
                'fields': ('url_video',),
                'description': 'URL de YouTube o Vimeo'
            }),
            ('Contenido de Imagen', {
                'fields': ('imagen', 'descripcion_imagen'),
            }),
        )
        return fieldsets

@admin.register(ExperienciaCafetera)
class ExperienciaCafeteraAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_publicacion', 'get_contenido_count')
    list_filter = ('fecha_publicacion',)
    search_fields = ('titulo', 'descripcion_breve')
    prepopulated_fields = {'slug': ('titulo',)}
    inlines = [ContenidoExperienciaInline]
    
    fieldsets = (
        ('Información Principal', {
            'fields': ('titulo', 'slug', 'descripcion_breve')
        }),
    )
    
    def get_contenido_count(self, obj):
        return obj.contenido.count()
    get_contenido_count.short_description = "Bloques de contenido"
