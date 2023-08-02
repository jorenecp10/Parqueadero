from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Parqueadero(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    cupo_maximo = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre

    def actualizar_cupo_disponible(self):
        cupo_actual = self.cupo_maximo - self.vehiculo_set.count()
        return max(0, cupo_actual)
    @property
    def cupo_disponible(self):
        return self.cupo_maximo - self.vehiculo_set.count()



class Vehiculo(models.Model):
    placa = models.CharField(max_length=10)
    parqueadero = models.ForeignKey(Parqueadero, on_delete=models.CASCADE)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    propietario = models.CharField(max_length=100)  # Nuevo campo para el propietario

    def __str__(self):
        return self.placa

class VehiculoEliminado(models.Model):
    placa = models.CharField(max_length=10)
    propietario = models.CharField(max_length=100)
    parqueadero = models.ForeignKey(Parqueadero, on_delete=models.CASCADE)
    fecha_ingreso = models.DateTimeField()
    fecha_eliminacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.placa

