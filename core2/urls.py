from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # /core2/
    path('home/', views.home_core2, name='home_core2'),  
]