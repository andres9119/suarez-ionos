from django.db import models
from suarez.image_optimizer import OptimizedImageField

class BannerPrincipal(models.Model):
    titulo = models.CharField(max_length=200, default="Bienvenidos a Suárez")
    subtitulo = models.TextField(default="Portal de la Tradición y Cultura Cafetera.")
    imagen_fondo = OptimizedImageField(upload_to='banner/', max_width=1920, max_height=800, quality=90, help_text="Imagen de gran tamaño para el fondo del banner")
    texto_boton = models.CharField(max_length=50, default="Ver Noticias")
    link_boton = models.CharField(max_length=200, default="/noticias/")
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Banner Principal"
        verbose_name_plural = "Banner Principal"

    def __str__(self):
        return self.titulo


class Video(models.Model):
    titulo = models.CharField(max_length=200)
    url_embebida = models.URLField(help_text="URL de YouTube para embeber (ej. https://www.youtube.com/embed/...)")
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class ImagenGaleria(models.Model):
    titulo = models.CharField(max_length=200, blank=True)
    imagen = OptimizedImageField(upload_to='galeria/', max_width=1200, max_height=800, quality=85, create_thumbnail=True)
    imagen_thumbnail = models.ImageField(upload_to='galeria/thumbnails/', blank=True, null=True)
    es_destacada = models.BooleanField(default=False, help_text="Si se marca, aparecerá en el carrusel de la página de inicio")
    fecha_carga = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.titulo or f"Imagen {self.id}"

class EventoDestacado(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    imagen = OptimizedImageField(upload_to='eventos_destacados/', max_width=800, max_height=600, quality=85, create_thumbnail=True)
    imagen_thumbnail = models.ImageField(upload_to='eventos_destacados/thumbnails/', blank=True, null=True)
    fecha_evento = models.DateField()
    link = models.URLField(blank=True, null=True, help_text="Link opcional a más información")

    def __str__(self):
        return self.titulo
