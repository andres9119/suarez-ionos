"""
Instrucciones para ejecutar:
python optimize_images.py
"""

import os
from PIL import Image

def optimize_images():
    # Rutas a procesar
    base_dir = os.path.dirname(os.path.abspath(__file__))
    targets = [
        os.path.join(base_dir, 'static', 'img'),
        os.path.join(base_dir, 'media')
    ]
    
    widths = [400, 800, 1200]
    quality = 75
    valid_extensions = ('.jpg', '.jpeg', '.png')
    
    print(f"Iniciando optimización de imágenes en: {', '.join(targets)}")
    
    for target_dir in targets:
        if not os.path.exists(target_dir):
            print(f"Aviso: La ruta {target_dir} no existe. Saltando...")
            continue
            
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                if file.lower().endswith(valid_extensions):
                    input_path = os.path.join(root, file)
                    base_name = os.path.splitext(file)[0]
                    
                    # Generar versiones WebP para cada tamaño
                    try:
                        with Image.open(input_path) as img:
                            # Convertir a RGB si es necesario (para evitar errores con PNG/RGBA en WebP)
                            if img.mode in ('RGBA', 'P'):
                                img = img.convert('RGB')
                                
                            original_width, original_height = img.size
                            
                            for width in widths:
                                # Mantener proporción
                                if original_width > width:
                                    height = int((width / original_width) * original_height)
                                    resized_img = img.resize((width, height), Image.Resampling.LANCZOS)
                                    output_filename = f"{base_name}_{width}.webp"
                                else:
                                    # Si la imagen es más pequeña que el target, guardamos tamaño original
                                    resized_img = img
                                    output_filename = f"{base_name}_{width}.webp"
                                    
                                output_path = os.path.join(root, output_filename)
                                resized_img.save(output_path, 'WEBP', quality=quality)
                                print(f"Creado: {output_path}")
                                
                            # También generamos la versión WebP original (sin resize) para compatibilidad
                            output_path_orig = os.path.join(root, f"{base_name}.webp")
                            img.save(output_path_orig, 'WEBP', quality=quality)
                            print(f"Convertido: {output_path_orig}")
                            
                    except Exception as e:
                        print(f"Error procesando {input_path}: {e}")

if __name__ == "__main__":
    optimize_images()
    print("Optimización completada.")
