from django.contrib import admin
from .models import Parqueadero, Vehiculo,VehiculoEliminado
# Register your models here.

admin.site.register(Parqueadero)
admin.site.register(Vehiculo)
admin.site.register(VehiculoEliminado)