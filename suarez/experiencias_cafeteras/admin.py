from django.contrib import admin
from .models import ExperienciaCafetera

@admin.register(ExperienciaCafetera)
class ExperienciaCafeteraAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'slug', 'fecha_publicacion')
    search_fields = ('titulo', 'historia', 'slug')
    prepopulated_fields = {'slug': ('titulo',)}
