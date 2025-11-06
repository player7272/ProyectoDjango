from django import forms
from core1.models import Solicitud, Estado
from core2.models import Empleado, Permiso, Nomina, PeriodoNomina, ConceptoNomina
from .models import ProcesoContratacion, ConfiguracionNomina
from django.contrib.auth.models import User
from datetime import date

class RevisionSolicitudForm(forms.ModelForm):
    """Formulario para revisar y aprobar/rechazar solicitudes"""
    decision = forms.ChoiceField(
        choices=[
            ('APROBAR', 'Aprobar para Contratación'),
            ('RECHAZAR', 'Rechazar Solicitud')
        ],
        widget=forms.RadioSelect(attrs={'class': 'decision-radio'})
    )
    
    class Meta:
        model = ProcesoContratacion
        fields = ['observaciones_rrhh']
        widgets = {
            'observaciones_rrhh': forms.Textarea(attrs={
                'class': 'input',
                'placeholder': 'Observaciones sobre la decisión',
                'rows': 4
            })
        }


class ContratacionForm(forms.ModelForm):
    """Formulario para crear el empleado desde una solicitud aprobada"""
    fecha_ingreso = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'input',
            'type': 'date'
        }),
        initial=date.today
    )
    
    class Meta:
        model = Empleado
        fields = ['nombre', 'apellido', 'cedula', 'correo', 'telefono', 
                  'direccion', 'fecha_nacimiento', 'fecha_ingreso', 'categoria']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Apellido'}),
            'cedula': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Cédula'}),
            'correo': forms.EmailInput(attrs={'class': 'input', 'placeholder': 'correo@ejemplo.com'}),
            'telefono': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Teléfono'}),
            'direccion': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Dirección'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'categoria': forms.Select(attrs={'class': 'input'}),
        }


class RevisionPermisoForm(forms.ModelForm):
    """Formulario para aprobar/rechazar permisos de empleados"""
    decision = forms.ChoiceField(
        choices=[
            ('APROBADO', 'Aprobar Permiso'),
            ('RECHAZADO', 'Rechazar Permiso')
        ],
        widget=forms.RadioSelect(attrs={'class': 'decision-radio'})
    )
    
    class Meta:
        model = Permiso
        fields = ['observaciones']
        widgets = {
            'observaciones': forms.Textarea(attrs={
                'class': 'input',
                'placeholder': 'Observaciones sobre la decisión',
                'rows': 4
            })
        }


class PeriodoNominaForm(forms.ModelForm):
    """Formulario para crear un nuevo periodo de nómina"""
    class Meta:
        model = PeriodoNomina
        fields = ['tipo', 'fecha_inicio', 'fecha_fin', 'fecha_pago']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'input'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'fecha_pago': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
        }


class NominaManualForm(forms.ModelForm):
    """Formulario para editar manualmente elementos de la nómina"""
    class Meta:
        model = Nomina
        fields = ['bonificaciones', 'deducciones', 'horas_extra', 'valor_hora_extra']
        widgets = {
            'bonificaciones': forms.NumberInput(attrs={'class': 'input', 'step': '0.01'}),
            'deducciones': forms.NumberInput(attrs={'class': 'input', 'step': '0.01'}),
            'horas_extra': forms.NumberInput(attrs={'class': 'input', 'step': '0.01'}),
            'valor_hora_extra': forms.NumberInput(attrs={'class': 'input', 'step': '0.01'}),
        }


class ConceptoNominaForm(forms.ModelForm):
    """Formulario para agregar conceptos adicionales a una nómina"""
    class Meta:
        model = ConceptoNomina
        fields = ['tipo', 'concepto', 'valor', 'descripcion']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'input'}),
            'concepto': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Ej: Bono de desempeño'}),
            'valor': forms.NumberInput(attrs={'class': 'input', 'step': '0.01'}),
            'descripcion': forms.Textarea(attrs={'class': 'input', 'rows': 3}),
        }


class ConfiguracionNominaForm(forms.ModelForm):
    """Formulario para configurar parámetros generales de nómina"""
    class Meta:
        model = ConfiguracionNomina
        fields = ['porcentaje_seguridad_social', 'porcentaje_salud', 'porcentaje_pension',
                  'valor_auxilio_transporte', 'salario_minimo_legal']
        widgets = {
            'porcentaje_seguridad_social': forms.NumberInput(attrs={'class': 'input', 'step': '0.01'}),
            'porcentaje_salud': forms.NumberInput(attrs={'class': 'input', 'step': '0.01'}),
            'porcentaje_pension': forms.NumberInput(attrs={'class': 'input', 'step': '0.01'}),
            'valor_auxilio_transporte': forms.NumberInput(attrs={'class': 'input', 'step': '0.01'}),
            'salario_minimo_legal': forms.NumberInput(attrs={'class': 'input', 'step': '0.01'}),
        }