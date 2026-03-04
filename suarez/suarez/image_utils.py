import os
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class ImageOptimizer:
    """Clase para optimizar imágenes automáticamente"""
    
    @staticmethod
    def optimize_image(image_field, max_width=1920, max_height=1080, quality=85):
        """
        Optimiza una imagen automáticamente manteniendo la proporción
        
        Args:
            image_field: Campo ImageField de Django
            max_width: Ancho máximo permitido
            max_height: Altura máxima permitida
            quality: Calidad de compresión (1-100)
        
        Returns:
            bool: True si se optimizó, False si no fue necesario
        """
        try:
            # Abrir la imagen
            img = Image.open(image_field)
            
            # Convertir a RGB si es necesario (para JPEG)
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            # Obtener dimensiones originales
            original_width, original_height = img.size
            
            # Calcular nuevas dimensiones manteniendo proporción
            if original_width > max_width or original_height > max_height:
                ratio = min(max_width / original_width, max_height / original_height)
                new_width = int(original_width * ratio)
                new_height = int(original_height * ratio)
                
                # Redimensionar con alta calidad
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Guardar la imagen optimizada
                buffer = BytesIO()
                
                # Determinar formato de salida
                if img.format == 'PNG' and img.mode == 'RGBA':
                    img.save(buffer, format='PNG', optimize=True)
                else:
                    img.save(buffer, format='JPEG', quality=quality, optimize=True, progressive=True)
                
                # Actualizar el campo de imagen
                image_field.save(
                    os.path.basename(image_field.name),
                    ContentFile(buffer.getvalue()),
                    save=False
                )
                
                logger.info(f"Imagen optimizada: {image_field.name} - {original_width}x{original_height} -> {new_width}x{new_height}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error optimizando imagen {image_field.name}: {str(e)}")
            return False
    
    @staticmethod
    def create_thumbnail(image_field, size=(300, 300), quality=85):
        """
        Crea una versión thumbnail de la imagen
        
        Args:
            image_field: Campo ImageField de Django
            size: Dimensiones del thumbnail (ancho, alto)
            quality: Calidad de compresión
        
        Returns:
            ContentFile: Archivo de imagen thumbnail o None si hay error
        """
        try:
            img = Image.open(image_field)
            
            # Convertir a RGB si es necesario
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            # Crear thumbnail con recorte inteligente
            img.thumbnail(size, Image.Resampling.LANCZOS)
            
            # Crear imagen cuadrada si es necesario
            if img.size[0] != size[0] or img.size[1] != size[1]:
                # Centrar la imagen
                background = Image.new('RGB', size, (255, 255, 255))
                offset = ((size[0] - img.size[0]) // 2, (size[1] - img.size[1]) // 2)
                background.paste(img, offset)
                img = background
            
            # Guardar thumbnail
            buffer = BytesIO()
            img.save(buffer, format='JPEG', quality=quality, optimize=True)
            
            # Nombre basado en el original
            original_name = os.path.basename(image_field.name)
            name, ext = os.path.splitext(original_name)
            thumbnail_name = f"{name}_thumb{ext}"
            
            return ContentFile(buffer.getvalue(), name=thumbnail_name)
            
        except Exception as e:
            logger.error(f"Error creando thumbnail para {image_field.name}: {str(e)}")
            return None
    
    @staticmethod
    def get_image_info(image_field):
        """
        Obtiene información básica de la imagen
        
        Args:
            image_field: Campo ImageField de Django
        
        Returns:
            dict: Información de la imagen
        """
        try:
            img = Image.open(image_field)
            return {
                'width': img.width,
                'height': img.height,
                'format': img.format,
                'mode': img.mode,
                'size_bytes': image_field.size
            }
        except Exception as e:
            logger.error(f"Error obteniendo info de imagen {image_field.name}: {str(e)}")
            return {}
