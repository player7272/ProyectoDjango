from django.urls import path
from . import views

urlpatterns = [
    # Dashboard RRHH
    path('', views.dashboard_rrhh, name='dashboard_rrhh'),
    
    # Gestión de Solicitudes/Contratación
    path('solicitudes/', views.lista_solicitudes, name='lista_solicitudes_rrhh'),
    path('solicitudes/<int:solicitud_id>/revisar/', views.revisar_solicitud, name='revisar_solicitud'),
    path('solicitudes/<int:solicitud_id>/contratar/', views.contratar_empleado, name='contratar_empleado'),
    
    # Gestión de Permisos
    path('permisos/', views.lista_permisos, name='lista_permisos_rrhh'),
    path('permisos/<int:permiso_id>/revisar/', views.revisar_permiso, name='revisar_permiso'),
    
    # Gestión de Empleados
    path('empleados/', views.lista_empleados, name='lista_empleados_rrhh'),
    path('empleados/<int:empleado_id>/', views.detalle_empleado_rrhh, name='detalle_empleado_rrhh'),
    path('empleados/<int:empleado_id>/editar/', views.editar_empleado_rrhh, name='editar_empleado_rrhh'),
    path('empleados/<int:empleado_id>/desactivar/', views.desactivar_empleado, name='desactivar_empleado'),
    
    # Gestión de Nóminas
    path('nominas/', views.lista_nominas_rrhh, name='lista_nominas_rrhh'),
    path('nominas/periodo/nuevo/', views.crear_periodo_nomina, name='crear_periodo_nomina'),
    path('nominas/periodo/<int:periodo_id>/', views.detalle_periodo_nomina, name='detalle_periodo_nomina'),
    path('nominas/periodo/<int:periodo_id>/generar/', views.generar_nominas, name='generar_nominas'),
    path('nominas/<int:nomina_id>/editar/', views.editar_nomina, name='editar_nomina_rrhh'),
    path('nominas/<int:nomina_id>/agregar-concepto/', views.agregar_concepto, name='agregar_concepto'),
    path('nominas/<int:nomina_id>/marcar-pagado/', views.marcar_pagado, name='marcar_pagado'),
    
    # Configuración
    path('configuracion/', views.configuracion_nomina, name='configuracion_nomina'),
    
    # Reportes
    path('reportes/', views.reportes_rrhh, name='reportes_rrhh'),
]