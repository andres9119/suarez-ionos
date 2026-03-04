from django.db import models
from django.utils.text import slugify
from suarez.image_optimizer import OptimizedImageField

class ExperienciaCafetera(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=False, blank=True, null=True)
    historia = models.TextField()
    proceso = models.TextField(help_text="Descripción del proceso de producción o preparación")
    imagen_principal = OptimizedImageField(upload_to='cafe/imagenes/', max_width=1200, max_height=800, quality=85, create_thumbnail=True)
    imagen_thumbnail = models.ImageField(upload_to='cafe/imagenes/thumbnails/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True, help_text="URL de video relacionado")
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)
