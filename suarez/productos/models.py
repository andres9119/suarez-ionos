from django.db import models
from django.utils.text import slugify
from suarez.image_optimizer import OptimizedImageField


class Producto(models.Model):
    titulo = models.CharField(max_length=200, help_text="Nombre del producto o servicio")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    descripcion = models.TextField(help_text="Descripción detallada del producto/servicio")
    orden = models.IntegerField(default=0, help_text="Orden de presentación")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['orden', '-fecha_creacion']
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo

    @property
    def primera_imagen(self):
        """Retorna la primera imagen del producto"""
        return self.imagenes.first()


class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, related_name='imagenes', on_delete=models.CASCADE)
    imagen = OptimizedImageField(
        upload_to='productos/imagenes/',
        max_width=1200,
        max_height=800,
        quality=85,
        create_thumbnail=True
    )
    orden = models.IntegerField(default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['producto', 'orden', '-fecha_creacion']
        verbose_name = "Imagen de Producto"
        verbose_name_plural = "Imágenes de Productos"

    def __str__(self):
        return f"{self.producto.titulo} - Imagen {self.orden}"
