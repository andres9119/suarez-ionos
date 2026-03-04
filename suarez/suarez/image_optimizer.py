from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import models
from .image_utils import ImageOptimizer
import logging

logger = logging.getLogger(__name__)

@receiver(pre_save)
def optimize_image_on_save(sender, **kwargs):
    """
    Señal que optimiza automáticamente las imágenes antes de guardar
    """
    instance = kwargs.get('instance')
    
    if not instance:
        return
    
    # Revisar todos los campos ImageField del modelo
    for field in instance._meta.get_fields():
        if isinstance(field, models.ImageField):
            image_field = getattr(instance, field.name)
            
            # Solo optimizar si la imagen ha cambiado o es nueva
            if image_field and hasattr(image_field, 'file') and image_field.file:
                # Optimizar imagen principal
                ImageOptimizer.optimize_image(image_field)
                
                # Crear thumbnail si el campo existe
                thumbnail_field_name = f"{field.name}_thumbnail"
                if hasattr(instance, thumbnail_field_name):
                    thumbnail = ImageOptimizer.create_thumbnail(image_field)
                    if thumbnail:
                        setattr(instance, thumbnail_field_name, thumbnail)

class OptimizedImageField(models.ImageField):
    """
    Campo de imagen personalizado que se optimiza automáticamente
    """
    
    def __init__(self, *args, **kwargs):
        # Parámetros de optimización por defecto
        self.max_width = kwargs.pop('max_width', 1920)
        self.max_height = kwargs.pop('max_height', 1080)
        self.quality = kwargs.pop('quality', 85)
        self.create_thumbnail = kwargs.pop('create_thumbnail', False)
        
        super().__init__(*args, **kwargs)
    
    def pre_save(self, model_instance, add):
        """
        Optimiza la imagen antes de guardar
        """
        file = super().pre_save(model_instance, add)
        
        if file and hasattr(file, 'file'):
            # Optimizar imagen principal
            ImageOptimizer.optimize_image(
                file, 
                max_width=self.max_width,
                max_height=self.max_height,
                quality=self.quality
            )
            
            # Crear thumbnail si se solicita
            if self.create_thumbnail:
                thumbnail = ImageOptimizer.create_thumbnail(file)
                if thumbnail:
                    # Guardar thumbnail en un campo separado
                    thumbnail_field_name = f"{self.name}_thumbnail"
                    if hasattr(model_instance, thumbnail_field_name):
                        setattr(model_instance, thumbnail_field_name, thumbnail)
        
        return file
