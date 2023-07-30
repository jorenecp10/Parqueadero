from django import forms
from .models import Parqueadero,Vehiculo

class ParqueaderoForm(forms.ModelForm):
    class Meta:
        model = Parqueadero
        fields = ['nombre', 'cupo_maximo']
class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['placa', 'parqueadero', 'propietario']  # Agregar 'propietario' al formulario