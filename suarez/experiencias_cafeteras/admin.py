from django.contrib import admin
from .models import ExperienciaCafetera, ContenidoExperiencia

class ContenidoExperienciaInline(admin.TabularInline):
    model = ContenidoExperiencia
    extra = 1
    fields = ('tipo', 'orden', 'titulo_texto', 'contenido_texto', 'url_video', 'imagen', 'descripcion_imagen')
    ordering = ('orden',)
    
    def formfield_for_choice_field(self, db_field, request, **kwargs):
        formfield = super().formfield_for_choice_field(db_field, request, **kwargs)
        return formfield

@admin.register(ExperienciaCafetera)
class ExperienciaCafeteraAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'slug', 'fecha_publicacion', 'get_contenido_count')
    list_filter = ('fecha_publicacion',)
    search_fields = ('titulo', 'descripcion_breve', 'slug')
    prepopulated_fields = {'slug': ('titulo',)}
    inlines = [ContenidoExperienciaInline]
    
    fieldsets = (
        ('Información Principal', {
            'fields': ('titulo', 'slug', 'imagen_principal')
        }),
        ('Descripción', {
            'fields': ('descripcion_breve',),
            'description': 'Descripción breve que aparecerá en la lista de experiencias'
        }),
        ('Thumbnail (Auto-Generado)', {
            'fields': ('imagen_thumbnail',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('imagen_thumbnail',)
    
    def get_contenido_count(self, obj):
        return obj.contenido.count()
    get_contenido_count.short_description = "Bloques de contenido"

@admin.register(ContenidoExperiencia)
class ContenidoExperienciaAdmin(admin.ModelAdmin):
    list_display = ('experiencia', 'get_tipo_display', 'orden', 'titulo_texto', 'fecha_creacion')
    list_filter = ('tipo', 'experiencia', 'fecha_creacion')
    list_editable = ('orden',)
    search_fields = ('experiencia__titulo', 'titulo_texto', 'contenido_texto')
    ordering = ('experiencia', 'orden')
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('experiencia', 'tipo', 'orden')
        }),
        ('Contenido - Texto', {
            'fields': ('titulo_texto', 'contenido_texto'),
            'classes': ('collapse',)
        }),
        ('Contenido - Video', {
            'fields': ('url_video',),
            'classes': ('collapse',),
            'description': 'URL de YouTube o Vimeo (ej: https://www.youtube.com/embed/VIDEO_ID)'
        }),
        ('Contenido - Imagen', {
            'fields': ('imagen', 'descripcion_imagen'),
            'classes': ('collapse',)
        }),
    )
