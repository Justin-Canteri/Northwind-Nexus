from django.urls import path
from . import views

urlpatterns = [
    path('', views.buscar),
    path('hola/', views.hola),
    path('crear/', views.crear_producto)
    ]