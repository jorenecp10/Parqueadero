from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Parqueadero, Vehiculo
from django.contrib import messages
from .forms import ParqueaderoForm



from django.shortcuts import render
from .models import Parqueadero

def pagina_inicio(request):
    parqueaderos = Parqueadero.objects.all()

    disponibilidad_parqueaderos = {}
    for parqueadero in parqueaderos:
        disponibilidad_parqueaderos[parqueadero.nombre] = parqueadero.cupo_maximo - parqueadero.vehiculo_set.count()

    return render(request, 'pagina_inicio.html', {'disponibilidad_parqueaderos': disponibilidad_parqueaderos})


@login_required


@user_passes_test(lambda u: u.is_superuser)
def crear_parqueadero(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        cupo_maximo = request.POST['cupo_maximo']

        if not Parqueadero.objects.filter(nombre=nombre).exists():
            parqueadero = Parqueadero(nombre=nombre, cupo_maximo=cupo_maximo)
            parqueadero.save()
            messages.success(request, f'Parqueadero "{nombre}" creado correctamente.')
            return redirect('listar_vehiculos')

        messages.error(request, f'El parqueadero "{nombre}" ya existe.')
    return render(request, 'crear_parqueadero.html')


@login_required
def listar_vehiculos(request):
    vehiculos = Vehiculo.objects.all()
    parqueaderos = Parqueadero.objects.all()  # Asegúrate de incluir esta línea para obtener los parqueaderos disponibles
    return render(request, 'listar_vehiculos.html', {'vehiculos': vehiculos, 'parqueaderos': parqueaderos})


@login_required
@login_required
def buscar_eliminar_vehiculo(request):
    if request.method == 'POST':
        placa = request.POST['placa']
        vehiculos = Vehiculo.objects.filter(placa=placa)
    else:
        vehiculos = Vehiculo.objects.all()

    return render(request, 'buscar_eliminar_vehiculo.html', {'vehiculos': vehiculos})
def eliminar_vehiculos(request):
    if request.method == 'POST':
        vehiculos_a_eliminar = request.POST.getlist('eliminar_vehiculo')
        Vehiculo.objects.filter(id__in=vehiculos_a_eliminar).delete()
        messages.success(request, 'Los vehículos seleccionados han sido eliminados correctamente.')

    return redirect('buscar_eliminar_vehiculo')

@login_required
def ver_disponibilidad(request):
    if request.method == 'POST':
        parqueadero_id = request.POST['parqueadero_id']
        parqueadero = get_object_or_404(Parqueadero, id=parqueadero_id)
        vehiculos_en_parqueadero = Vehiculo.objects.filter(parqueadero=parqueadero).count()
        cupos_disponibles = parqueadero.cupo_maximo - vehiculos_en_parqueadero
        messages.info(request, f'En el parqueadero "{parqueadero.nombre}" hay {cupos_disponibles} cupos disponibles.')

    return redirect('listar_vehiculos')

@login_required
def ingresar_vehiculo(request):
    parqueaderos = Parqueadero.objects.all()

    if request.method == 'POST':
        placa = request.POST['placa']
        parqueadero_id = request.POST['parqueadero_id']
        parqueadero = get_object_or_404(Parqueadero, id=parqueadero_id)

        vehiculos_en_parqueadero = Vehiculo.objects.filter(parqueadero=parqueadero).count()
        if vehiculos_en_parqueadero >= parqueadero.cupo_maximo:
            messages.error(request, f'El parqueadero "{parqueadero.nombre}" está lleno. No se puede ingresar el vehículo.')
        else:
            vehiculo = Vehiculo(placa=placa, parqueadero=parqueadero)
            vehiculo.save()
            messages.success(request, f'Vehículo con placa "{placa}" ingresado al parqueadero "{parqueadero.nombre}".')

    return render(request, 'ingresar_vehiculo.html', {'parqueaderos': parqueaderos})

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

@login_required
def eliminar_parqueadero(request, parqueadero_id):
    parqueadero = get_object_or_404(Parqueadero, pk=parqueadero_id)

    if request.method == 'POST':
        parqueadero.delete()
        return redirect('pagina_inicio')

    return render(request, 'eliminar_parqueadero.html', {'parqueadero': parqueadero})

def listar_parqueaderos(request):
    parqueaderos = Parqueadero.objects.all()
    return render(request, 'listar_parqueaderos.html', {'parqueaderos': parqueaderos})