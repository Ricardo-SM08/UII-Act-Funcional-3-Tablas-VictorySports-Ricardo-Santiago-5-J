# app_victorysports/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Proveedor
from django.db import IntegrityError # Necesario para manejar el unique=True en nombre_empresa

# Función de inicio
def inicio_victorysports(request):
    """Muestra la página de inicio."""
    return render(request, 'inicio.html') # Asume que inicio.html extiende de base.html

# CREATE: Función para agregar proveedor
def agregar_proveedor(request):
    if request.method == 'POST':
        # No se usa forms.py, se accede directamente a request.POST
        try:
            Proveedor.objects.create(
                nombre_empresa=request.POST.get('nombre_empresa'),
                telefono_empresa=request.POST.get('telefono_empresa'),
                email_empresa=request.POST.get('email_empresa'),
                pais_origen=request.POST.get('pais_origen'),
                contacto_principal=request.POST.get('contacto_principal'),
                direccion=request.POST.get('direccion')
                # fecha_registro se añade automáticamente por auto_now_add
            )
            # Redirigir a la vista de lista después de crear
            return redirect(reverse('ver_proveedor'))
        except IntegrityError:
            # Manejar el error de nombre de empresa duplicado (unique=True)
            # Podrías pasar un mensaje de error a la plantilla si fuera necesario
            context = {'error_message': 'Ya existe un proveedor con ese nombre de empresa.'}
            return render(request, 'proveedor/agregar_proveedor.html', context)
        except Exception as e:
            # Manejar otros errores
            context = {'error_message': f'Ocurrió un error: {e}'}
            return render(request, 'proveedor/agregar_proveedor.html', context)

    # Si es GET, muestra el formulario
    return render(request, 'proveedor/agregar_proveedor.html')

# READ: Función para ver proveedores
def ver_proveedor(request):
    """Muestra todos los proveedores en una tabla."""
    proveedores = Proveedor.objects.all().order_by('nombre_empresa')
    context = {'proveedores': proveedores}
    # Muestra en tabla con botones ver, editar y borrar
    return render(request, 'proveedor/ver_proveedor.html', context)

# UPDATE (Formulario): Función para obtener el proveedor a actualizar
def actualizar_proveedor(request, pk):
    """Muestra el formulario precargado con los datos del proveedor para editar."""
    proveedor = get_object_or_404(Proveedor, pk=pk)
    context = {'proveedor': proveedor}
    return render(request, 'proveedor/actualizar_proveedor.html', context)

# UPDATE (Procesamiento): Función para realizar la actualización
def realizar_actualizacion_proveedor(request):
    if request.method == 'POST':
        # Se asume que el id_proveedor viene en un campo oculto en el POST
        proveedor_id = request.POST.get('id_proveedor')
        proveedor = get_object_or_404(Proveedor, pk=proveedor_id)

        try:
            # Actualiza los campos
            proveedor.nombre_empresa = request.POST.get('nombre_empresa')
            proveedor.telefono_empresa = request.POST.get('telefono_empresa')
            proveedor.email_empresa = request.POST.get('email_empresa')
            proveedor.pais_origen = request.POST.get('pais_origen')
            proveedor.contacto_principal = request.POST.get('contacto_principal')
            proveedor.direccion = request.POST.get('direccion')
            
            # Guarda los cambios en la base de datos
            proveedor.save()

            # Redirigir a la vista de lista después de actualizar
            return redirect(reverse('ver_proveedor'))
        except IntegrityError:
            # Manejar el error de nombre de empresa duplicado
            context = {'proveedor': proveedor, 'error_message': 'Ya existe un proveedor con ese nombre de empresa.'}
            return render(request, 'proveedor/actualizar_proveedor.html', context)
        except Exception as e:
            context = {'proveedor': proveedor, 'error_message': f'Ocurrió un error: {e}'}
            return render(request, 'proveedor/actualizar_proveedor.html', context)

    # Si se accede por GET directamente, redirigir a la lista
    return redirect(reverse('ver_proveedor'))

# DELETE: Función para borrar proveedor
def borrar_proveedor(request, pk):
    """Procesa la eliminación de un proveedor."""
    proveedor = get_object_or_404(Proveedor, pk=pk)
    
    if request.method == 'POST':
        # Solo permite POST para la acción de borrado
        proveedor.delete()
        # Redirigir a la vista de lista
        return redirect(reverse('ver_proveedor'))
    
    # Si es GET, muestra una página de confirmación de borrado
    context = {'proveedor': proveedor}
    return render(request, 'proveedor/borrar_proveedor.html', context)