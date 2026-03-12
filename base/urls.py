from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio),
    path('buscar/', views.buscar),
    path('crear/', views.crear_producto),
    path('borrar/<int:id_producto>/', views.delete_producto),
    path('editar/<int:id_producto>/', views.editar_producto)
    ]