from django.contrib import admin
from .models import Estado, Persona, Categoria, Solicitud


# -------------------------------
#  ESTADO
# -------------------------------
@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    list_display_links = ('id', 'nombre')
    search_fields = ('nombre',)
    ordering = ('id',)
    list_per_page = 20


# -------------------------------
#  PERSONA
# -------------------------------
@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido', 'cedula', 'correo')
    list_display_links = ('id', 'nombre', 'apellido')
    search_fields = ('nombre', 'apellido', 'cedula', 'correo')
    ordering = ('id',)
    list_per_page = 20

    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'apellido', 'cedula')
        }),
        ('Contacto', {
            'fields': ('correo',)
        }),
    )


# -------------------------------
#  CATEGORIA
# -------------------------------
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'salario_base')
    list_display_links = ('id', 'nombre')
    search_fields = ('nombre',)
    ordering = ('id',)
    list_per_page = 20

    fieldsets = (
        ('Información de la Categoría', {
            'fields': ('nombre', 'salario_base'),
        }),
    )


# -------------------------------
#  SOLICITUD
# -------------------------------
@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('id', 'persona', 'estado', 'short_mensaje', 'fecha_creacion')
    list_display_links = ('id', 'persona')
    list_filter = ('estado', 'fecha_creacion')
    search_fields = (
        'persona__nombre', 
        'persona__apellido', 
        'persona__correo', 
        'persona__cedula',
        'mensaje'
    )
    ordering = ('-fecha_creacion',)
    list_per_page = 20

    readonly_fields = ('fecha_creacion',)

    fieldsets = (
        ('Información de la Solicitud', {
            'fields': ('persona', 'mensaje', 'estado')
        }),
        ('Tiempos', {
            'fields': ('fecha_creacion',),
            'classes': ('collapse',)
        }),
    )

    # Para que no se vea gigante el mensaje en la tabla
    def short_mensaje(self, obj):
        return (obj.mensaje[:50] + '...') if len(obj.mensaje) > 50 else obj.mensaje
    short_mensaje.short_description = "Mensaje"
