from django.contrib import admin
from .models import Video, ImagenGaleria, EventoDestacado, BannerPrincipal

@admin.register(BannerPrincipal)
class BannerPrincipalAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'activo')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_publicacion')
    search_fields = ('titulo',)

@admin.register(ImagenGaleria)
class ImagenGaleriaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'es_destacada', 'fecha_carga')
    list_filter = ('es_destacada',)


@admin.register(EventoDestacado)
class EventoDestacadoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_evento')
    list_filter = ('fecha_evento',)
    search_fields = ('titulo', 'descripcion')
