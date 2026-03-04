from django.db import models
from suarez.image_optimizer import OptimizedImageField

class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, help_text="Identificador único para la URL (ej. nueva-obra-en-el-pueblo)")
    contenido = models.TextField()
    imagen_destacada = OptimizedImageField(upload_to='noticias/', max_width=1200, max_height=800, quality=85, create_thumbnail=True)
    imagen_thumbnail = models.ImageField(upload_to='noticias/thumbnails/', blank=True, null=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    es_evento = models.BooleanField(default=False, help_text="Marcar si es un evento municipal")
    fecha_evento = models.DateField(blank=True, null=True, help_text="Solo si es un evento")

    class Meta:
        ordering = ['-fecha_publicacion']

    def __str__(self):
        return self.titulo
