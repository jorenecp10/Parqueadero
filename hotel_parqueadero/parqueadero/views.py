from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Parqueadero, Vehiculo,VehiculoEliminado
from django.shortcuts import render
from django.db.models import Q
from django.contrib import messages
from .forms import ParqueaderoForm,VehiculoForm
from django.core.exceptions import ValidationError


def pagina_inicio(request):
    parqueaderos = Parqueadero.objects.all()
    vehiculos = Vehiculo.objects.all().order_by('fecha_ingreso')  # Ordenar desde el último vehículo ingresado
    disponibilidad_parqueaderos = {}
    for parqueadero in parqueaderos:
        disponibilidad_parqueaderos[parqueadero.nombre] = parqueadero.cupo_maximo - parqueadero.vehiculo_set.count()
    if request.method == 'POST':
        placa = request.POST['placa']
        vehiculos = Vehiculo.objects.filter(Q(placa__iexact=placa) | Q(placa__iexact=placa.upper()))
    else:
        vehiculos = Vehiculo.objects.all()

    return render(request, 'pagina_inicio.html', {'disponibilidad_parqueaderos': disponibilidad_parqueaderos, 'vehiculos': vehiculos})
def buscar_eliminar_vehiculo(request):
    if request.method == 'POST':
        placa = request.POST['placa']
        vehiculos = Vehiculo.objects.filter(Q(placa__iexact=placa) | Q(placa__iexact=placa.upper()))
    else:
        vehiculos = Vehiculo.objects.all()

    return render(request, 'pagina_inicio.html', {'vehiculos': vehiculos})


def eliminar_vehiculos(request):
    if request.method == 'POST':
        vehiculos_a_eliminar = request.POST.getlist('eliminar_vehiculo')
        vehiculos_eliminados = Vehiculo.objects.filter(id__in=vehiculos_a_eliminar)
        vehiculo_ids = request.POST.getlist('eliminar_vehiculo')
        for vehiculo_eliminado in vehiculos_eliminados:
            VehiculoEliminado.objects.create(
                placa=vehiculo_eliminado.placa,
                propietario=vehiculo_eliminado.propietario,
                parqueadero=vehiculo_eliminado.parqueadero,
                fecha_ingreso=vehiculo_eliminado.fecha_ingreso
            )
        vehiculos_eliminados.delete()

        if not vehiculo_ids:
            messages.error(request, 'Debe seleccionar al menos un vehículo para sacar.')
        else:
            Vehiculo.objects.filter(id__in=vehiculo_ids).delete()
            messages.success(request, 'Los vehículos seleccionados han sido sacados exitosamente.')
    return redirect('pagina_inicio')
# views.py

from django.shortcuts import render
from .models import VehiculoEliminado

def vehiculos_eliminados(request):
    vehiculos_eliminados = VehiculoEliminado.objects.all().order_by('-fecha_eliminacion')
    return render(request, 'vehiculos_eliminados.html', {'vehiculos_eliminados': vehiculos_eliminados})






@login_required
def crear_parqueadero(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        cupo_maximo = request.POST['cupo_maximo']

        if not Parqueadero.objects.filter(nombre=nombre).exists():
            parqueadero = Parqueadero(nombre=nombre, cupo_maximo=cupo_maximo)
            parqueadero.save()
            messages.success(request, f'Parqueadero "{nombre}" creado correctamente.')
            return redirect('pagina_inicio')

        messages.error(request, f'El parqueadero "{nombre}" ya existe.')
    return render(request, 'crear_parqueadero.html')



def listar_vehiculos(request):
    vehiculos = Vehiculo.objects.all().order_by('-fecha_ingreso')  # Ordenar por fecha_ingreso en orden descendente (-)
    parqueaderos = Parqueadero.objects.all()  # Asegúrate de incluir esta línea para obtener los parqueaderos disponibles
    return render(request, 'listar_vehiculos.html', {'vehiculos': vehiculos, 'parqueaderos': parqueaderos})






def ver_disponibilidad(request):
    if request.method == 'POST':
        parqueadero_id = request.POST['parqueadero_id']
        parqueadero = get_object_or_404(Parqueadero, id=parqueadero_id)
        vehiculos_en_parqueadero = Vehiculo.objects.filter(parqueadero=parqueadero).count()
        cupos_disponibles = parqueadero.cupo_maximo - vehiculos_en_parqueadero
        messages.info(request, f'En el parqueadero "{parqueadero.nombre}" hay {cupos_disponibles} cupos disponibles.')

    return redirect('listar_vehiculos')




def ingresar_vehiculo(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            placa = form.cleaned_data['placa']
            parqueadero = form.cleaned_data['parqueadero']
            cupo_disponible = parqueadero.actualizar_cupo_disponible()

            if cupo_disponible > 0:
                # Verificar si ya existe un vehículo con la misma placa
                if Vehiculo.objects.filter(Q(placa=placa) | Q(placa=placa.upper())).exists():
                    messages.error(request, f'El vehículo con la placa "{placa}" ya está registrado.')
                else:
                    form.save()
                    parqueadero.actualizar_cupo_disponible()
                    messages.success(request, f'Vehículo ingresado exitosamente en {parqueadero.nombre}. Cupo disponible: {cupo_disponible - 1}')
                return redirect('pagina_inicio')
            else:
                messages.error(request, 'No hay cupo disponible en este parqueadero.')
    else:
        form = VehiculoForm()

    return render(request, 'ingresar_vehiculo.html', {'form': form})


def editar_eliminar_parqueadero(request, parqueadero_id):
    parqueadero = get_object_or_404(Parqueadero, pk=parqueadero_id)

    if request.method == 'POST':
        form = ParqueaderoForm(request.POST, instance=parqueadero)
        if form.is_valid():
            form.save()
            return redirect('pagina_inicio')
    else:
        form = ParqueaderoForm(instance=parqueadero)

    return render(request, 'editar_eliminar_parqueadero.html', {'form': form, 'parqueadero': parqueadero})


def eliminar_parqueadero(request, parqueadero_id):
    parqueadero = get_object_or_404(Parqueadero, pk=parqueadero_id)

    if request.method == 'POST':
        parqueadero.delete()
        return redirect('pagina_inicio')

    return render(request, 'eliminar_parqueadero.html', {'parqueadero': parqueadero})



@login_required
def listar_parqueaderos(request):
    parqueaderos = Parqueadero.objects.all()
    return render(request, 'listar_parqueaderos.html', {'parqueaderos': parqueaderos})
