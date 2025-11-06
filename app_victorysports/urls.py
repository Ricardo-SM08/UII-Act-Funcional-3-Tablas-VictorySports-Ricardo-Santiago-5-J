# app_victorysports/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_victorysports, name='inicio_victorysports'),
    path('proveedores/', views.ver_proveedor, name='ver_proveedor'),
    path('proveedores/agregar/', views.agregar_proveedor, name='agregar_proveedor'),
    path('proveedores/actualizar/<int:pk>/', views.actualizar_proveedor, name='actualizar_proveedor'),
    path('proveedores/realizar_actualizacion/', views.realizar_actualizacion_proveedor, name='realizar_actualizacion_proveedor'),
    path('proveedores/borrar/<int:pk>/', views.borrar_proveedor, name='borrar_proveedor'),
]