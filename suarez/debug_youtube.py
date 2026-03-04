import os
import django
import sys

# Setup Django
sys.path.append('c:\\Users\\LENOVO\\Desktop\\suarez_cauca\\suarez')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'suarez.settings')
django.setup()

from inicio.models import Video
from experiencias_cafeteras.models import Experiencia
from inicio.templatetags.youtube_tags import get_youtube_id

print("--- Videos Inicio ---")
for v in Video.objects.all():
    id = get_youtube_id(v.url_embebida)
    print(f"Titulo: {v.titulo}")
    print(f"URL: {v.url_embebida}")
    print(f"ID Extraído: {id}")
    print("-" * 20)

print("\n--- Experiencias ---")
for e in Experiencia.objects.all():
    id = get_youtube_id(e.video_url)
    print(f"Titulo: {e.titulo}")
    print(f"URL: {e.video_url}")
    print(f"ID Extraído: {id}")
    print("-" * 20)
