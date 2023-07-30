from django import forms
from .models import Parqueadero

class ParqueaderoForm(forms.ModelForm):
    class Meta:
        model = Parqueadero
        fields = ['nombre', 'cupo_maximo']
