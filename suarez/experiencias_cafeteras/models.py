from django.db import models
from django.utils.text import slugify
from suarez.image_optimizer import OptimizedImageField

class ExperienciaCafetera(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    descripcion_breve = models.TextField(blank=True, null=True, help_text="Descripción breve para la lista")
    imagen_principal = OptimizedImageField(upload_to='cafe/imagenes/', max_width=1200, max_height=800, quality=85, create_thumbnail=True, blank=True, null=True)
    imagen_thumbnail = models.ImageField(upload_to='cafe/imagenes/thumbnails/', blank=True, null=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_publicacion']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    @property
    def primera_imagen(self):
        """Retorna la primera imagen del contenido, o la imagen_principal si no hay contenido"""
        imagen_bloque = self.contenido.filter(tipo='imagen').first()
        if imagen_bloque and imagen_bloque.imagen:
            return imagen_bloque.imagen
        return self.imagen_principal if self.imagen_principal else None

    def __str__(self):
        return self.titulo


class ContenidoExperiencia(models.Model):
    TIPO_CHOICES = [
        ('texto', 'Texto'),
        ('video', 'Video'),
        ('imagen', 'Imagen'),
    ]
    
    experiencia = models.ForeignKey(ExperienciaCafetera, related_name='contenido', on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    orden = models.IntegerField(default=0, help_text="Orden de presentación (menor número = primero)")
    
    # Para contenidos (antes titulo_texto)
    titulo_bloque = models.CharField(max_length=200, blank=True, null=True, help_text="Opcional: Título para esta sección o bloque")
    contenido_texto = models.TextField(blank=True, null=True, help_text="Contenido del texto (si el tipo es Texto)")
    
    # Para videos
    url_video = models.URLField(blank=True, null=True, help_text="URL de YouTube o Vimeo")
    
    # Para imágenes
    imagen = OptimizedImageField(upload_to='cafe/galeria/', max_width=1200, max_height=800, quality=85, create_thumbnail=True, blank=True, null=True)
    descripcion_imagen = models.CharField(max_length=255, blank=True, null=True)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['experiencia', 'orden', '-fecha_creacion']
        verbose_name = "Contenido de Experiencia"
        verbose_name_plural = "Contenido de Experiencias"

    def __str__(self):
        return f"{self.experiencia.titulo} - {self.get_tipo_display()} ({self.orden})"
