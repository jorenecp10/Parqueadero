from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Parqueadero(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    cupo_maximo = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre

class Vehiculo(models.Model):
    placa = models.CharField(max_length=10, unique=True)
    parqueadero = models.ForeignKey(Parqueadero, on_delete=models.CASCADE)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.placa
