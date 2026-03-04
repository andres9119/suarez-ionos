from django.contrib import admin
from .models import MensajeContacto

@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ('asunto', 'nombre', 'email', 'fecha_envio', 'leido')
    list_filter = ('leido', 'fecha_envio')
    search_fields = ('nombre', 'email', 'asunto', 'mensaje')
    readonly_fields = ('nombre', 'email', 'asunto', 'mensaje', 'fecha_envio')
    
    def has_add_permission(self, request):
        return False
