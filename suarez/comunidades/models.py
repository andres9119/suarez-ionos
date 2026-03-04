from django.db import models
from django.utils.text import slugify
from suarez.image_optimizer import OptimizedImageField

class Comunidad(models.Model):
    TIPO_CHOICES = [
        ('indigena', 'Indígena'),
        ('afro', 'Afrodescendiente'),
        ('campesina', 'Campesina'),
    ]
    nombre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=False, blank=True, null=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    resena_cultural = models.TextField()
    historia = models.TextField()
    logo_o_emblema = OptimizedImageField(upload_to='comunidades/logos/', max_width=400, max_height=400, quality=90, help_text="Logo o emblema de la comunidad")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"

class ImagenComunidad(models.Model):
    comunidad = models.ForeignKey(Comunidad, related_name='imagenes', on_delete=models.CASCADE)
    imagen = OptimizedImageField(upload_to='comunidades/galeria/', max_width=1200, max_height=800, quality=85, create_thumbnail=True)
    imagen_thumbnail = models.ImageField(upload_to='comunidades/galeria/thumbnails/', blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Imagen de {self.comunidad.nombre}"
