from django.contrib import admin
from .models import Comunidad, ImagenComunidad

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
