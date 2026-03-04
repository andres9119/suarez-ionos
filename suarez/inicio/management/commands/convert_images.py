from django.core.management.base import BaseCommand
from django.conf import settings
import os
from PIL import Image

class Command(BaseCommand):
    help = 'Converts media images to WebP format for optimization'

    def handle(self, *args, **options):
        media_root = settings.MEDIA_ROOT
        for root, dirs, files in os.walk(media_root):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')) and not file.lower().endswith('.webp'):
                    file_path = os.path.join(root, file)
                    file_name, file_ext = os.path.splitext(file_path)
                    webp_path = f"{file_name}.webp"

                    if not os.path.exists(webp_path):
                        try:
                            with Image.open(file_path) as img:
                                self.stdout.write(f"Converting {file} to WebP...")
                                img.save(webp_path, 'WEBP', quality=85)
                                self.stdout.write(self.style.SUCCESS(f"Successfully converted {file}"))
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f"Failed to convert {file}: {e}"))
                    else:
                        self.stdout.write(f"Skipping {file} (WebP already exists)")
