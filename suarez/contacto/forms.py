from django import forms
from django.core.validators import EmailValidator, MinLengthValidator
from .models import MensajeContacto
import re

class ContactoForm(forms.ModelForm):
    # Honeypot field (invisible para usuarios, visible para bots)
    website = forms.CharField(required=False, widget=forms.HiddenInput())
    
    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'email', 'asunto', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control form-control-lg rounded-4 border-0 bg-light p-3',
                'placeholder': 'Tu nombre',
                'maxlength': '100'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control form-control-lg rounded-4 border-0 bg-light p-3',
                'placeholder': 'email@ejemplo.com',
                'maxlength': '254'
            }),
            'asunto': forms.TextInput(attrs={
                'class': 'form-control form-control-lg rounded-4 border-0 bg-light p-3',
                'placeholder': 'Motivo de tu mensaje',
                'maxlength': '200'
            }),
            'mensaje': forms.Textarea(attrs={
                'class': 'form-control form-control-lg rounded-4 border-0 bg-light p-3',
                'placeholder': 'Escribe aquí tu mensaje...',
                'rows': 5,
                'maxlength': '2000'
            }),
        }
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if not nombre:
            raise forms.ValidationError('El nombre no puede estar vacío.')
        if len(nombre) < 3:
            raise forms.ValidationError('El nombre debe tener al menos 3 caracteres.')
        # Solo letras, espacios, tildes y algunos caracteres especiales
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s\'-]+$', nombre):
            raise forms.ValidationError('El nombre solo puede contener letras.')
        return nombre
    
    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if not email:
            raise forms.ValidationError('El email no puede estar vacío.')
        # Validación adicional de email
        validator = EmailValidator()
        validator(email)
        return email
    
    def clean_asunto(self):
        asunto = self.cleaned_data.get('asunto', '').strip()
        if not asunto:
            raise forms.ValidationError('El asunto no puede estar vacío.')
        if len(asunto) < 5:
            raise forms.ValidationError('El asunto debe tener al menos 5 caracteres.')
        return asunto
    
    def clean_mensaje(self):
        mensaje = self.cleaned_data.get('mensaje', '').strip()
        if not mensaje:
            raise forms.ValidationError('El mensaje no puede estar vacío.')
        if len(mensaje) < 10:
            raise forms.ValidationError('El mensaje debe tener al menos 10 caracteres.')
        if len(mensaje) > 2000:
            raise forms.ValidationError('El mensaje no puede exceder 2000 caracteres.')
        return mensaje
    
    def clean_website(self):
        # Honeypot: si este campo tiene valor, es un bot
        website = self.cleaned_data.get('website')
        if website:
            raise forms.ValidationError('Spam detectado.')
        return website
