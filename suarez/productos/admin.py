from django.contrib import admin
from .models import Producto, ImagenProducto


class ImagenProductoInline(admin.TabularInline):
    model = ImagenProducto
    extra = 3
    fields = ('imagen',)
    verbose_name = "Imagen"
    verbose_name_plural = "Imágenes"


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'get_imagenes_count', 'fecha_creacion')
    list_filter = ('fecha_creacion',)
    search_fields = ('titulo', 'descripcion', 'slug')
    prepopulated_fields = {'slug': ('titulo',)}
    inlines = [ImagenProductoInline]

    fieldsets = (
        ('Información del Producto', {
            'fields': ('titulo', 'descripcion'),
            'description': 'Ingresa aquí el título y descripción. Las imágenes se optimizan automáticamente a WebP.'
        }),
        ('URL personalizada', {
            'fields': ('slug',),
            'classes': ('collapse',),
            'description': 'Se genera automáticamente. No es necesario modificar.'
        }),
    )

    def get_imagenes_count(self, obj):
        return obj.imagenes.count()
    get_imagenes_count.short_description = "Imágenes"

