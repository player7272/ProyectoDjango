from django.urls import path
from . import views

urlpatterns = [
    # Vista principal unificada
    path('', views.inicio, name='index'),
    
    
    # Endpoints para procesar formularios
    path('aplicar/', views.aplicar, name='aplicar'),
    path('estado/', views.estado, name='estado'),
    
    # Rutas legacy (redirigen a la vista unificada)
    path('categorias/', views.categorias, name='categorias'),
    path('gracias/', views.gracias, name='gracias'),
    path('formulario/', views.aplicar, name='formulario'),
]