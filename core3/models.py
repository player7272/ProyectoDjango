from django.db import models
from django.contrib.auth.models import User
from core1.models import Solicitud, Persona, Categoria, Estado
from core2.models import Empleado, Permiso, Nomina, PeriodoNomina
from decimal import Decimal
from datetime import date

class ProcesoContratacion(models.Model):
    ESTADO_CHOICES = [
        ('EN_REVISION', 'En Revisión'),
        ('APROBADO', 'Aprobado para Contratación'),
        ('RECHAZADO', 'Rechazado'),
        ('CONTRATADO', 'Contratado'),
    ]
    
    solicitud = models.OneToOneField(Solicitud, on_delete=models.CASCADE, related_name='proceso_contratacion')
    estado_proceso = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='EN_REVISION')
    fecha_revision = models.DateTimeField(auto_now_add=True)
    fecha_decision = models.DateTimeField(null=True, blank=True)
    observaciones_rrhh = models.TextField(blank=True)
    revisado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='procesos_revisados')
    empleado_creado = models.OneToOneField(Empleado, on_delete=models.SET_NULL, null=True, blank=True, related_name='proceso_origen')
    
    def __str__(self):
        return f"Proceso {self.solicitud.persona.nombre} - {self.get_estado_proceso_display()}"
    
    class Meta:
        ordering = ['-fecha_revision']
        verbose_name = 'Proceso de Contratación'
        verbose_name_plural = 'Procesos de Contratación'


class ConfiguracionNomina(models.Model):
    porcentaje_seguridad_social = models.DecimalField(max_digits=5, decimal_places=2, default=4.0)
    porcentaje_salud = models.DecimalField(max_digits=5, decimal_places=2, default=4.0)
    porcentaje_pension = models.DecimalField(max_digits=5, decimal_places=2, default=4.0)
    valor_auxilio_transporte = models.DecimalField(max_digits=10, decimal_places=2, default=140606)
    salario_minimo_legal = models.DecimalField(max_digits=10, decimal_places=2, default=1300000)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Configuración Nómina - {self.fecha_creacion.strftime('%Y-%m-%d')}"
    
    class Meta:
        verbose_name = 'Configuración de Nómina'
        verbose_name_plural = 'Configuraciones de Nómina'
        ordering = ['-fecha_creacion']