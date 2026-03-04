from django.db import models
from django.core.validators import MinLengthValidator, EmailValidator

class MensajeContacto(models.Model):
    nombre = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3, 'El nombre debe tener al menos 3 caracteres.')]
    )
    email = models.EmailField(
        validators=[EmailValidator('Ingresa un email válido.')]
    )
    asunto = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(5, 'El asunto debe tener al menos 5 caracteres.')]
    )
    mensaje = models.TextField(
        validators=[MinLengthValidator(10, 'El mensaje debe tener al menos 10 caracteres.')]
    )
    fecha_envio = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        verbose_name = 'Mensaje de Contacto'
        verbose_name_plural = 'Mensajes de Contacto'
        ordering = ['-fecha_envio']

    def __str__(self):
        return f"Mensaje de {self.nombre} - {self.asunto}"
