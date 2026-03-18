from django.contrib import admin
from .models import Producto, ImagenProducto


class ImagenProductoInline(admin.StackedInline):
    model = ImagenProducto
    extra = 1
    fields = ('imagen', 'orden')
    ordering = ('orden',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'orden', 'get_imagenes_count', 'fecha_creacion')
    list_filter = ('fecha_creacion',)
    list_editable = ('orden',)
    search_fields = ('titulo', 'descripcion', 'slug')
    prepopulated_fields = {'slug': ('titulo',)}
    inlines = [ImagenProductoInline]

    fieldsets = (
        ('Información del Producto', {
            'fields': ('titulo', 'slug', 'descripcion')
        }),
        ('Orden', {
            'fields': ('orden',),
            'description': 'Menor número = primero en la lista'
        }),
    )

    def get_imagenes_count(self, obj):
        return obj.imagenes.count()
    get_imagenes_count.short_description = "Imágenes"
