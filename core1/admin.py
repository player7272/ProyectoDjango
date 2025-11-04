from django.contrib import admin
from .models import Estado, Persona, Categoria, Solicitud

@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')


@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido', 'cedula', 'correo')
    search_fields = ('nombre', 'apellido', 'correo', 'cedula')


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'salario_base')
    search_fields = ('nombre',)


@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('id', 'persona', 'mensaje', 'estado', 'fecha_creacion')
    list_filter = ('estado', 'fecha_creacion')
    search_fields = ('persona__nombre', 'persona__apellido', 'persona__correo', 'persona__cedula')
