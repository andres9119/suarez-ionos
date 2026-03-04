from django.db import models

class CategoriaDocumento(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class DocumentoPublico(models.Model):
    titulo = models.CharField(max_length=200)
    archivo = models.FileField(upload_to='documentos/publicos/')
    categoria = models.ForeignKey(CategoriaDocumento, on_delete=models.CASCADE, related_name='documentos')
    fecha_subida = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.titulo
