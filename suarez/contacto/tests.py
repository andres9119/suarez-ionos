from django.test import TestCase, Client
from django.urls import reverse
from django.core.cache import cache
from .models import MensajeContacto

class ContactoFormSecurityTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('contacto:index')
        # Limpiar caché antes de cada test
        cache.clear()
    
    def tearDown(self):
        # Limpiar caché después de cada test
        cache.clear()
    
    def test_formulario_vacio_rechazado(self):
        """Verificar que no se puede enviar formulario vacío"""
        response = self.client.post(self.url, {})
        self.assertEqual(MensajeContacto.objects.count(), 0)
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any('vacío' in str(m).lower() or 'required' in str(m).lower() for m in messages))
    
    def test_formulario_con_espacios_rechazado(self):
        """Verificar que no se aceptan solo espacios en blanco"""
        response = self.client.post(self.url, {
            'nombre': '   ',
            'email': '   ',
            'asunto': '   ',
            'mensaje': '   ',
            'website': ''  # Honeypot vacío
        })
        self.assertEqual(MensajeContacto.objects.count(), 0)
    
    def test_nombre_muy_corto_rechazado(self):
        """Verificar que nombre debe tener al menos 3 caracteres"""
        response = self.client.post(self.url, {
            'nombre': 'AB',
            'email': 'test@example.com',
            'asunto': 'Asunto de prueba',
            'mensaje': 'Este es un mensaje de prueba válido.',
            'website': ''
        })
        self.assertEqual(MensajeContacto.objects.count(), 0)
    
    def test_nombre_con_numeros_rechazado(self):
        """Verificar que nombre solo acepta letras"""
        response = self.client.post(self.url, {
            'nombre': 'Juan123',
            'email': 'test@example.com',
            'asunto': 'Asunto de prueba',
            'mensaje': 'Este es un mensaje de prueba válido.',
            'website': ''
        })
        self.assertEqual(MensajeContacto.objects.count(), 0)
    
    def test_email_invalido_rechazado(self):
        """Verificar que email debe tener formato válido"""
        response = self.client.post(self.url, {
            'nombre': 'Juan Pérez',
            'email': 'email-invalido',
            'asunto': 'Asunto de prueba',
            'mensaje': 'Este es un mensaje de prueba válido.',
            'website': ''
        })
        self.assertEqual(MensajeContacto.objects.count(), 0)
    
    def test_asunto_muy_corto_rechazado(self):
        """Verificar que asunto debe tener al menos 5 caracteres"""
        response = self.client.post(self.url, {
            'nombre': 'Juan Pérez',
            'email': 'juan@example.com',
            'asunto': 'Test',
            'mensaje': 'Este es un mensaje de prueba válido.',
            'website': ''
        })
        self.assertEqual(MensajeContacto.objects.count(), 0)
    
    def test_mensaje_muy_corto_rechazado(self):
        """Verificar que mensaje debe tener al menos 10 caracteres"""
        response = self.client.post(self.url, {
            'nombre': 'Juan Pérez',
            'email': 'juan@example.com',
            'asunto': 'Asunto de prueba',
            'mensaje': 'Corto',
            'website': ''
        })
        self.assertEqual(MensajeContacto.objects.count(), 0)
    
    def test_formulario_valido_aceptado(self):
        """Verificar que formulario válido se guarda correctamente"""
        response = self.client.post(self.url, {
            'nombre': 'Juan Pérez',
            'email': 'juan@example.com',
            'asunto': 'Consulta general',
            'mensaje': 'Este es un mensaje de prueba válido con suficiente contenido.',
            'website': ''  # Honeypot vacío
        })
        self.assertEqual(MensajeContacto.objects.count(), 1)
        mensaje = MensajeContacto.objects.first()
        self.assertEqual(mensaje.nombre, 'Juan Pérez')
        self.assertEqual(mensaje.email, 'juan@example.com')
        self.assertIsNotNone(mensaje.ip_address)
    
    def test_honeypot_detecta_spam(self):
        """Verificar que honeypot detecta bots"""
        response = self.client.post(self.url, {
            'nombre': 'Bot Name',
            'email': 'bot@example.com',
            'asunto': 'Bot Subject',
            'mensaje': 'Bot message content here.',
            'website': 'http://spam-site.com'  # Bot llenó el honeypot
        })
        self.assertEqual(MensajeContacto.objects.count(), 0)
    
    def test_rate_limiting_funciona(self):
        """Verificar que rate limiting bloquea después de 3 envíos"""
        data = {
            'nombre': 'Test User',
            'email': 'test@example.com',
            'asunto': 'Test Subject',
            'mensaje': 'Test message content with enough characters.',
            'website': ''
        }
        
        # Enviar 3 veces (debería funcionar)
        for i in range(3):
            response = self.client.post(self.url, data)
            self.assertEqual(response.status_code, 302)  # Redirect
        
        # El cuarto intento debería ser bloqueado
        response = self.client.post(self.url, data)
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any('excedido' in str(m).lower() or 'límite' in str(m).lower() for m in messages))
        
        # Solo deben haberse guardado 3
        self.assertEqual(MensajeContacto.objects.count(), 3)
    
    def test_nombre_con_tildes_aceptado(self):
        """Verificar que nombres con tildes son válidos"""
        response = self.client.post(self.url, {
            'nombre': 'José María',
            'email': 'jose@example.com',
            'asunto': 'Consulta importante',
            'mensaje': 'Este es un mensaje válido con suficiente contenido.',
            'website': ''
        })
        self.assertEqual(MensajeContacto.objects.count(), 1)
        mensaje = MensajeContacto.objects.first()
        self.assertEqual(mensaje.nombre, 'José María')
    
    def test_mensaje_largo_rechazado(self):
        """Verificar que mensajes muy largos son rechazados"""
        mensaje_largo = 'a' * 2001  # Más de 2000 caracteres
        response = self.client.post(self.url, {
            'nombre': 'Juan Pérez',
            'email': 'juan@example.com',
            'asunto': 'Asunto de prueba',
            'mensaje': mensaje_largo,
            'website': ''
        })
        self.assertEqual(MensajeContacto.objects.count(), 0)
