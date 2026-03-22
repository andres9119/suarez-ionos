import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'suarez.settings')
django.setup()

from experiencias_cafeteras.models import ExperienciaCafetera, ContenidoExperiencia

print("Checking ExperienciaCafetera objects...")
experiencias = ExperienciaCafetera.objects.all()
print(f"Total experiences: {experiencias.count()}")

for exp in experiencias:
    print(f"ID: {exp.id}, Title: {exp.titulo}, Slug: {exp.slug}")
    print(f"  Content blocks: {exp.contenido.count()}")
    for block in exp.contenido.all():
        print(f"    - Type: {block.tipo}, Order: {block.orden}")

if not experiencias.exists():
    print("No experiences found in database.")
