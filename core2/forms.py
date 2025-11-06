from django import forms
from .models import Empleado, Permiso
from core1.models import Categoria

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombre', 'apellido', 'cedula', 'correo', 'telefono', 
                  'direccion', 'fecha_nacimiento', 'categoria']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Nombre'
            }),
            'apellido': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Apellido'
            }),
            'cedula': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Cédula'
            }),
            'correo': forms.EmailInput(attrs={
                'class': 'input',
                'placeholder': 'correo@ejemplo.com'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Teléfono'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Dirección'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'input',
                'type': 'date'
            }),
            'categoria': forms.Select(attrs={
                'class': 'input'
            }),
        }


class PermisoForm(forms.ModelForm):
    class Meta:
        model = Permiso
        fields = ['tipo_permiso', 'fecha_inicio', 'fecha_fin', 'motivo']
        widgets = {
            'tipo_permiso': forms.Select(attrs={
                'class': 'input',
            }),
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'input',
                'type': 'date'
            }),
            'fecha_fin': forms.DateInput(attrs={
                'class': 'input',
                'type': 'date'
            }),
            'motivo': forms.Textarea(attrs={
                'class': 'input',
                'placeholder': 'Describe el motivo de tu solicitud',
                'rows': 4
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        
        if fecha_inicio and fecha_fin:
            if fecha_fin < fecha_inicio:
                raise forms.ValidationError("La fecha de fin no puede ser anterior a la fecha de inicio")
        
        return cleaned_data