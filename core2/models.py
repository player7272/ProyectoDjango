from django.db import models
from django.contrib.auth.models import User
from core1.models import Categoria
from decimal import Decimal
from datetime import date

class Empleado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='empleado')
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=True)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=200, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    fecha_ingreso = models.DateField(default=date.today)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    activo = models.BooleanField(default=True)
    datos_completados = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.cedula}"
    
    def dias_en_empresa(self):
        """Calcula los días que lleva el empleado en la empresa"""
        if self.fecha_ingreso:
            return (date.today() - self.fecha_ingreso).days
        return 0
    
    def anos_en_empresa(self):
        """Calcula los años que lleva el empleado en la empresa"""
        return self.dias_en_empresa() // 365


class TipoPermiso(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    dias_maximos = models.IntegerField(default=0, help_text="0 = ilimitado")
    requiere_aprobacion = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre


class Permiso(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('APROBADO', 'Aprobado'),
        ('RECHAZADO', 'Rechazado'),
    ]
    
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='permisos')
    tipo_permiso = models.ForeignKey(TipoPermiso, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    motivo = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_respuesta = models.DateTimeField(null=True, blank=True)
    observaciones = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.empleado.nombre} - {self.tipo_permiso.nombre} ({self.estado})"
    
    def dias_solicitados(self):
        """Calcula los días solicitados"""
        return (self.fecha_fin - self.fecha_inicio).days + 1


class PeriodoNomina(models.Model):
    TIPO_PERIODO = [
        ('QUINCENAL', 'Quincenal'),
        ('MENSUAL', 'Mensual'),
    ]
    
    tipo = models.CharField(max_length=20, choices=TIPO_PERIODO, default='QUINCENAL')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    fecha_pago = models.DateField()
    cerrado = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-fecha_inicio']
    
    def __str__(self):
        return f"{self.tipo} - {self.fecha_inicio} a {self.fecha_fin}"


class Nomina(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='nominas')
    periodo = models.ForeignKey(PeriodoNomina, on_delete=models.CASCADE, related_name='nominas')
    salario_base = models.DecimalField(max_digits=10, decimal_places=2)
    bonificaciones = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deducciones = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    horas_extra = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    valor_hora_extra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_devengado = models.DecimalField(max_digits=10, decimal_places=2)
    total_deducciones = models.DecimalField(max_digits=10, decimal_places=2)
    neto_pagar = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    pagado = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-periodo__fecha_inicio']
        unique_together = ['empleado', 'periodo']
    
    def calcular_totales(self):
        """Calcula los totales de la nómina"""
        horas_extra_total = self.horas_extra * self.valor_hora_extra
        self.total_devengado = self.salario_base + self.bonificaciones + horas_extra_total
        self.total_deducciones = self.deducciones
        self.neto_pagar = self.total_devengado - self.total_deducciones
    
    def save(self, *args, **kwargs):
        self.calcular_totales()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Nómina {self.empleado.nombre} - {self.periodo}"


class ConceptoNomina(models.Model):
    TIPO_CHOICES = [
        ('DEVENGADO', 'Devengado'),
        ('DEDUCCION', 'Deducción'),
    ]
    
    nomina = models.ForeignKey(Nomina, on_delete=models.CASCADE, related_name='conceptos')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    concepto = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.concepto} - ${self.valor}"