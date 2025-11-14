from django.contrib import admin
from .models import (
    Empleado,
    TipoPermiso,
    Permiso,
    PeriodoNomina,
    Nomina,
    ConceptoNomina
)


# ------------------------------------
#  EMPLEADO
# ------------------------------------
@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido', 'cedula', 'correo', 'categoria', 'activo')
    list_display_links = ('id', 'nombre', 'apellido')
    search_fields = ('nombre', 'apellido', 'cedula', 'correo')
    list_filter = ('categoria', 'activo', 'fecha_ingreso')
    ordering = ('id',)
    list_per_page = 20

    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'apellido', 'cedula', 'correo')
        }),
        ('Información Laboral', {
            'fields': ('categoria', 'fecha_ingreso', 'activo')
        }),
    )


# ------------------------------------
#  TIPO PERMISO
# ------------------------------------
@admin.register(TipoPermiso)
class TipoPermisoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'dias_maximos', 'requiere_aprobacion')
    list_display_links = ('id', 'nombre')
    search_fields = ('nombre',)
    ordering = ('id',)
    list_per_page = 20

    fieldsets = (
        ('Configuración del Tipo de Permiso', {
            'fields': ('nombre', 'dias_maximos', 'requiere_aprobacion')
        }),
    )


# ------------------------------------
#  PERMISO
# ------------------------------------
@admin.register(Permiso)
class PermisoAdmin(admin.ModelAdmin):
    list_display = ('id', 'empleado', 'tipo_permiso', 'estado', 'fecha_inicio', 'fecha_fin')
    list_display_links = ('id', 'empleado')
    list_filter = ('estado', 'tipo_permiso', 'fecha_inicio')
    search_fields = ('empleado__nombre', 'empleado__apellido', 'empleado__cedula')
    ordering = ('-fecha_inicio',)
    list_per_page = 20

    readonly_fields = ('fecha_solicitud',)

    fieldsets = (
        ('Información del Permiso', {
            'fields': ('empleado', 'tipo_permiso', 'estado')
        }),
        ('Fechas del Permiso', {
            'fields': ('fecha_inicio', 'fecha_fin')
        }),
        ('Registro del Sistema', {
            'fields': ('fecha_solicitud',),
            'classes': ('collapse',)
        }),
    )


# ------------------------------------
#  PERIODO DE NOMINA
# ------------------------------------
@admin.register(PeriodoNomina)
class PeriodoNominaAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo', 'fecha_inicio', 'fecha_fin', 'fecha_pago', 'cerrado')
    list_display_links = ('id', 'tipo')
    list_filter = ('tipo', 'cerrado')
    ordering = ('-fecha_inicio',)
    list_per_page = 20

    readonly_fields = ('cerrado',)

    fieldsets = (
        ('Rango del Periodo', {
            'fields': ('tipo', 'fecha_inicio', 'fecha_fin')
        }),
        ('Pago y Cierre', {
            'fields': ('fecha_pago', 'cerrado'),
            'classes': ('collapse',)
        }),
    )


# ------------------------------------
#  NOMINA
# ------------------------------------
@admin.register(Nomina)
class NominaAdmin(admin.ModelAdmin):
    list_display = ('id', 'empleado', 'periodo', 'neto_pagar', 'pagado')
    list_display_links = ('id', 'empleado')
    list_filter = ('periodo', 'pagado')
    search_fields = (
        'empleado__nombre',
        'empleado__apellido',
        'empleado__cedula'
    )
    ordering = ('-periodo',)
    list_per_page = 20

    readonly_fields = ('fecha_generacion',)

    fieldsets = (
        ('Información de la Nómina', {
            'fields': ('empleado', 'periodo', 'pagado')
        }),
        ('Detalles de Valores', {
            'fields': ('neto_pagar',)
        }),
        ('Tiempos del Sistema', {
            'fields': ('fecha_generacion',),
            'classes': ('collapse',)
        }),
    )


# ------------------------------------
#  CONCEPTO DE NOMINA
# ------------------------------------
@admin.register(ConceptoNomina)
class ConceptoNominaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nomina', 'concepto', 'tipo', 'valor')
    list_display_links = ('id', 'nomina')
    list_filter = ('tipo', 'concepto')
    ordering = ('nomina',)
    list_per_page = 20

    fieldsets = (
        ('Detalle del Concepto de Nómina', {
            'fields': ('nomina', 'concepto', 'tipo', 'valor')
        }),
    )
