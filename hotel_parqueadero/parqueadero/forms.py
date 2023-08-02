from django import forms
from .models import Parqueadero, Vehiculo

# forms.py
class ParqueaderoForm(forms.ModelForm):
    class Meta:
        model = Parqueadero
        fields = ['nombre', 'cupo_maximo']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Parqueadero', 'class': 'form-control'}),
            'cupo_maximo': forms.NumberInput(attrs={'placeholder': 'Cupo Máximo', 'class': 'form-control'}),
        }

# forms.py
class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['placa', 'parqueadero', 'propietario']
        widgets = {
            'placa': forms.TextInput(attrs={'placeholder': 'Placa del Vehículo', 'class': 'form-control'}),
            'propietario': forms.TextInput(attrs={'placeholder': 'Propietario', 'class': 'form-control'}),
        }

    # Definir el campo parqueadero usando ModelChoiceField
    parqueadero = forms.ModelChoiceField(
        queryset=Parqueadero.objects.all(),
        empty_label='Seleccionar Parqueadero',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

