import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'suarez.settings')
django.setup()

from comunidades.models import Comunidad
from noticias.models import Noticia
from documentos.models import DocumentoPublico, CategoriaDocumento
from django.utils.text import slugify

def create_test_data():
    print("Creando datos de prueba...")
    
    # 1. Crear comunidades de prueba
    print("\n1. Creando comunidades...")
    comunidades_data = [
        {
            'nombre': 'Comunidad Indígena Nasa',
            'tipo': 'indigena',
            'resena_cultural': 'La comunidad Nasa es uno de los pueblos indígenas más grandes de Colombia, con una rica tradición cultural y espiritual.',
            'historia': 'Los Nasa han habitado las tierras del suroccidente colombiano por siglos, manteniendo sus tradiciones y luchando por la defensa de su territorio.'
        },
        {
            'nombre': 'Comunidad Afrodescendiente El Tambo',
            'tipo': 'afro',
            'resena_cultural': 'Comunidad afrocolombiana con profundas raíces africanas que han enriquecido la cultura del municipio con su música, danza y tradiciones.',
            'historia': 'Establecida en la región desde el siglo XIX, esta comunidad ha contribuido significativamente al desarrollo cultural y social de Suárez.'
        },
        {
            'nombre': 'Comunidad Campesina La Esperanza',
            'tipo': 'campesina',
            'resena_cultural': 'Comunidad dedicada a la agricultura tradicional, especialmente al cultivo de café, maíz y frijol.',
            'historia': 'Fundada por familias campesinas hace más de 50 años, ha sido pilar de la economía local y guardianes de las tradiciones agrícolas.'
        }
    ]
    
    for data in comunidades_data:
        slug = slugify(data['nombre'])
        comunidad, created = Comunidad.objects.get_or_create(
            slug=slug,
            defaults=data
        )
        if created:
            print(f"  ✓ Creada comunidad: {comunidad.nombre}")
        else:
            print(f"  - Ya existía: {comunidad.nombre}")
    
    # 2. Crear categorías de documentos
    print("\n2. Creando categorías de documentos...")
    categorias_data = [
        {'nombre': 'Decretos', 'descripcion': 'Decretos municipales emitidos por la Alcaldía'},
        {'nombre': 'Resoluciones', 'descripcion': 'Resoluciones administrativas y de gestión'},
        {'nombre': 'Acuerdos', 'descripcion': 'Acuerdos del Concejo Municipal'},
        {'nombre': 'Informes', 'descripcion': 'Informes de gestión y rendición de cuentas'},
    ]
    
    for data in categorias_data:
        categoria, created = CategoriaDocumento.objects.get_or_create(
            nombre=data['nombre'],
            defaults=data
        )
        if created:
            print(f"  ✓ Creada categoría: {categoria.nombre}")
        else:
            print(f"  - Ya existía: {categoria.nombre}")
    
    # 3. Crear noticias de prueba
    print("\n3. Creando noticias...")
    noticias_data = [
        {
            'titulo': 'Nueva obra de pavimentación en el centro del municipio',
            'slug': 'nueva-obra-pavimentacion-centro-municipio',
            'contenido': 'La Alcaldía de Suárez ha iniciado los trabajos de pavimentación en las principales calles del centro del municipio. Esta obra mejorará la movilidad de los peatones y vehículos, beneficiando a más de 5.000 habitantes. El proyecto tiene una duración estimada de 3 meses y contará con la mejor tecnología en materiales de construcción.',
            'es_evento': False
        },
        {
            'titulo': 'Festival Cultural de las Comunidades 2026',
            'slug': 'festival-cultural-comunidades-2026',
            'contenido': 'Se convoca a toda la comunidad a participar en el Festival Cultural que celebrará la diversidad étnica y cultural de nuestro municipio. Habrá presentaciones de grupos folclóricos, gastronomía local, artesanías y actividades para toda la familia. El evento se realizará en la plaza principal y contará con la participación de las comunidades indígenas, afrodescendientes y campesinas.',
            'es_evento': True,
            'fecha_evento': '2026-02-15'
        },
        {
            'titulo': 'Mejoramiento de servicios educativos en zona rural',
            'slug': 'mejoramiento-servicios-educativos-zona-rural',
            'contenido': 'La administración municipal ha destinado recursos para el mejoramiento de las instituciones educativas en la zona rural. Se entregarán dotaciones, se mejorarán las infraestructuras y se capacitará a los docentes en nuevas metodologías pedagógicas. Este beneficio alcanzará a más de 800 estudiantes de las veredas más apartadas del municipio.',
            'es_evento': False
        }
    ]
    
    for data in noticias_data:
        noticia, created = Noticia.objects.get_or_create(
            slug=data['slug'],
            defaults=data
        )
        if created:
            print(f"  ✓ Creada noticia: {noticia.titulo}")
        else:
            print(f"  - Ya existía: {noticia.titulo}")
    
    # 4. Crear documentos de prueba
    print("\n4. Creando documentos...")
    # Obtener categorías
    decretos = CategoriaDocumento.objects.get(nombre='Decretos')
    resoluciones = CategoriaDocumento.objects.get(nombre='Resoluciones')
    
    documentos_data = [
        {
            'titulo': 'Decreto 001 de 2026 - Plan de Desarrollo',
            'categoria': decretos,
            'descripcion': 'Decreto que adopta el Plan de Desarrollo Municipal 2026-2029'
        },
        {
            'titulo': 'Resolución 015 de 2026 - Presupuesto',
            'categoria': resoluciones,
            'descripcion': 'Resolución que aprueba el presupuesto general del municipio para la vigencia fiscal 2026'
        }
    ]
    
    for data in documentos_data:
        documento, created = DocumentoPublico.objects.get_or_create(
            titulo=data['titulo'],
            defaults=data
        )
        if created:
            print(f"  ✓ Creado documento: {documento.titulo}")
        else:
            print(f"  - Ya existía: {documento.titulo}")
    
    print("\n✅ Datos de prueba creados exitosamente!")
    print("\nAhora puedes verificar:")
    print("- Comunidades: http://localhost:8000/comunidades/")
    print("- Noticias: http://localhost:8000/noticias/")
    print("- Documentos: http://localhost:8000/documentos/")

if __name__ == '__main__':
    create_test_data()
