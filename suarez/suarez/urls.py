from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap, NoticiaSitemap, ExperienciaSitemap, ComunidadSitemap
import os

def robots_txt(request):
    """Serve robots.txt file"""
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /static/admin/",
        "",
        f"Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

sitemaps = {
    'static': StaticViewSitemap,
    'noticias': NoticiaSitemap,
    'experiencias': ExperienciaSitemap,
    'comunidades': ComunidadSitemap,
}

from django.urls import path, include, re_path
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', include('inicio.urls')),
    path('noticias/', include('noticias.urls')),
    path('comunidades/', include('comunidades.urls')),
    path('experiencias-cafeteras/', include('experiencias_cafeteras.urls')),
    path('documentos/', include('documentos.urls')),
    path('contacto/', include('contacto.urls')),
]

# Servir Media SIEMPRE (incluso en producción con DEBUG=False)
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

def custom_page_not_found(request, exception=None):
    from django.shortcuts import render
    return render(request, '404.html', status=404)

handler404 = custom_page_not_found
