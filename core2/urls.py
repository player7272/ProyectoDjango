from django.urls import path
from . import views

urlpatterns = [
    # Vista de inicio
    path('', views.index, name='index_core2'),
    path('home/', views.home_core2, name='home_core2'),
    
    # Dashboard principal
    path('dashboard/', views.dashboard_empleado, name='dashboard_empleado'),
    
    # Completar datos por primera vez
    path('completar-datos/', views.completar_datos, name='completar_datos'),
    
    # Nóminas
    path('nominas/', views.mis_nominas, name='mis_nominas'),
    path('nominas/<int:nomina_id>/', views.detalle_nomina, name='detalle_nomina'),
    
    # Permisos
    path('permisos/', views.mis_permisos, name='mis_permisos'),
    path('permisos/solicitar/', views.solicitar_permiso, name='solicitar_permiso'),
    
    # Perfil
    path('perfil/', views.perfil_empleado, name='perfil_empleado'),
]