from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
from .models import MensajeContacto
from .forms import ContactoForm
import logging

logger = logging.getLogger(__name__)

def get_client_ip(request):
    """Obtener IP del cliente"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def contacto(request):
    if request.method == 'POST':
        # Rate limiting: máximo 3 envíos por hora por IP
        client_ip = get_client_ip(request)
        cache_key = f'contact_form_{client_ip}'
        submission_count = cache.get(cache_key, 0)
        
        if submission_count >= 3:
            messages.error(request, 'Has excedido el límite de envíos. Por favor, intenta más tarde.')
            return redirect('contacto:index')
        
        form = ContactoForm(request.POST)
        
        if form.is_valid():
            # Incrementar contador de envíos
            cache.set(cache_key, submission_count + 1, 3600)  # 1 hora
            
            # Guardar en base de datos con IP
            mensaje_obj = form.save(commit=False)
            mensaje_obj.ip_address = client_ip
            mensaje_obj.save()
            
            # Enviar correo
            try:
                cuerpo_email = f"""
Nuevo mensaje de contacto desde el sitio web de Suárez 100% café:

Nombre: {mensaje_obj.nombre}
Correo: {mensaje_obj.email}
Asunto: {mensaje_obj.asunto}

Mensaje:
{mensaje_obj.mensaje}

---
IP: {client_ip}
Fecha: {mensaje_obj.fecha_envio}
                """
                
                send_mail(
                    subject=f"Portal Web: {mensaje_obj.asunto}",
                    message=cuerpo_email,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
                
                # Confirmación al usuario
                send_mail(
                    subject="Confirmación de Recibido - Suárez 100% café",
                    message=f"""Hola {mensaje_obj.nombre},

Hemos recibido tu mensaje con el asunto "{mensaje_obj.asunto}".

Gracias por ponerte en contacto con Suárez 100% café.
Nuestro equipo revisará tu solicitud y te responderemos a la brevedad posible.

Atentamente,
Suárez 100% café - Cauca
                    """,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[mensaje_obj.email],
                    fail_silently=True,
                )
                
                messages.success(request, 'Tu mensaje ha sido enviado correctamente.')
                return redirect('contacto:index')
                
            except Exception as e:
                logger.error(f"Error enviando email: {e}")
                messages.warning(request, 'Tu mensaje fue guardado pero hubo un problema al enviar el correo.')
                return redirect('contacto:index')
        else:
            # Mostrar errores del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = ContactoForm()
    
    return render(request, 'contacto/index.html', {'form': form})
