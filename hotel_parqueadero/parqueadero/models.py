from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Parqueadero(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    cupo_maximo = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre

from django.db import models

class Vehiculo(models.Model):
    placa = models.CharField(max_length=10)
    parqueadero = models.ForeignKey(Parqueadero, on_delete=models.CASCADE)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    propietario = models.CharField(max_length=100)  # Nuevo campo para el propietario

    def __str__(self):
        return self.placa

