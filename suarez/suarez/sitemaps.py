from django.contrib import sitemaps
from django.urls import reverse
from noticias.models import Noticia
from experiencias_cafeteras.models import ExperienciaCafetera
from comunidades.models import Comunidad

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['inicio:home', 'inicio:historia', 'noticias:lista', 'comunidades:lista', 'experiencias_cafeteras:lista', 'documentos:lista', 'contacto:index']

    def location(self, item):
        return reverse(item)

class NoticiaSitemap(sitemaps.Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Noticia.objects.all()

    def lastmod(self, obj):
        return obj.fecha_publicacion
    
    def location(self, obj):
        return reverse('noticias:detalle', args=[obj.slug])

class ExperienciaSitemap(sitemaps.Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return ExperienciaCafetera.objects.all()

    def location(self, obj):
        return reverse('experiencias_cafeteras:detalle', args=[obj.slug])

class ComunidadSitemap(sitemaps.Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Comunidad.objects.all()

    def location(self, obj):
        return reverse('comunidades:detalle', args=[obj.slug])
