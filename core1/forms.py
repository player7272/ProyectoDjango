from django import forms
from .models import Persona, Solicitud

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['nombre', 'apellido', 'cedula', 'correo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'input',
                'id': 'nombre',
                'placeholder': 'Nombre'
            }),
            'apellido': forms.TextInput(attrs={
                'class': 'input',
                'id': 'apellido',
                'placeholder': 'Apellido'
            }),
            'cedula': forms.TextInput(attrs={
                'class': 'input',
                'id': 'cedula',
                'placeholder': 'Cédula'
            }),
            'correo': forms.EmailInput(attrs={
                'class': 'input',
                'id': 'correo',
                'placeholder': 'tu@email.com'
            }),
        }


class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['mensaje']
        widgets = {
            'mensaje': forms.Textarea(attrs={
                'class': 'input',
                'id': 'mensaje',
                'placeholder': 'Describe tus capacidades o tu solicitud',
                'rows': 4
            }),
        }
