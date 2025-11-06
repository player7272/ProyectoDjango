from django.contrib import admin
from .models import ProcesoContratacion, ConfiguracionNomina

@admin.register(ProcesoContratacion)
class ProcesoContratacionAdmin(admin.ModelAdmin):
    list_display = ('solicitud', 'estado_proceso', 'fecha_revision', 'revisado_por')
    list_filter = ('estado_proceso', 'fecha_revision')
    search_fields = ('solicitud__persona__nombre', 'solicitud__persona__apellido')

@admin.register(ConfiguracionNomina)
class ConfiguracionNominaAdmin(admin.ModelAdmin):
    list_display = ('salario_minimo_legal', 'valor_auxilio_transporte', 'activo', 'fecha_creacion')
    list_filter = ('activo',)