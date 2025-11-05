from django.contrib import admin
from .models import (
    Empleado,
    TipoPermiso,
    Permiso,
    PeriodoNomina,
    Nomina,
    ConceptoNomina
)

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'cedula', 'correo', 'categoria', 'activo')
    search_fields = ('nombre', 'apellido', 'cedula', 'correo')
    list_filter = ('categoria', 'activo', 'fecha_ingreso')

@admin.register(TipoPermiso)
class TipoPermisoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'dias_maximos', 'requiere_aprobacion')
    search_fields = ('nombre',)

@admin.register(Permiso)
class PermisoAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'tipo_permiso', 'estado', 'fecha_inicio', 'fecha_fin')
    list_filter = ('estado', 'tipo_permiso')
    search_fields = ('empleado__nombre', 'empleado__apellido')

@admin.register(PeriodoNomina)
class PeriodoNominaAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'fecha_inicio', 'fecha_fin', 'fecha_pago', 'cerrado')
    list_filter = ('tipo', 'cerrado')

@admin.register(Nomina)
class NominaAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'periodo', 'neto_pagar', 'pagado')
    list_filter = ('periodo', 'pagado')
    search_fields = ('empleado__nombre', 'empleado__apellido')

@admin.register(ConceptoNomina)
class ConceptoNominaAdmin(admin.ModelAdmin):
    list_display = ('nomina', 'concepto', 'tipo', 'valor')
    list_filter = ('tipo',)
