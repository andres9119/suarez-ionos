from django.contrib import admin
from .models import ExperienciaCafetera, ContenidoExperiencia

class ContenidoExperienciaInline(admin.StackedInline):
    model = ContenidoExperiencia
    extra = 1
    fields = ('tipo', 'orden', 'titulo_texto', 'contenido_texto', 'url_video', 'imagen', 'descripcion_imagen')
    ordering = ('orden',)
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            ('Contenido', {
                'fields': ('tipo', 'orden')
            }),
            ('Texto (si tipo es Texto)', {
                'fields': ('titulo_texto', 'contenido_texto'),
                'classes': ('collapse',)
            }),
            ('Video (si tipo es Video)', {
                'fields': ('url_video',),
                'classes': ('collapse',),
                'description': 'URL de YouTube (ej: https://www.youtube.com/watch?v=VIDEO_ID)'
            }),
            ('Imagen (si tipo es Imagen)', {
                'fields': ('imagen', 'descripcion_imagen'),
                'classes': ('collapse',)
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
