from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='index'),
    
    
    path('aplicar/', views.aplicar, name='aplicar'),
    path('estado/', views.estado, name='estado'),
    
    path('categorias/', views.categorias, name='categorias'),
    path('gracias/', views.gracias, name='gracias'),
    path('formulario/', views.aplicar, name='formulario'),
]