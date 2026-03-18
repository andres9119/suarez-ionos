from django.contrib import admin
from .models import Comunidad, ImagenComunidad, GaleriaMunicipio

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

@admin.register(GaleriaMunicipio)
class GaleriaMunicipioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'slug', 'orden', 'fecha_creacion')
    list_filter = ('fecha_creacion',)
    list_editable = ('orden',)
    search_fields = ('titulo', 'descripcion', 'slug')
    prepopulated_fields = {'slug': ('titulo',)}
    ordering = ('orden', '-fecha_creacion')
