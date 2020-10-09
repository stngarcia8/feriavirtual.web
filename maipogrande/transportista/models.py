from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
# Country
# Modelo de datos que representa los paises de residencia de los clientes en el sistema.

class VehicleType(models.Model):
    VehicleTypeID = models.AutoField(primary_key=True)
    VehicleTypeDescription = models.CharField(
        max_length=100, verbose_name='Tipo transporte')

    class Meta:
        ordering = ('VehicleTypeID',)

    def __str__(self):
        return self.VehicleTypeDescription

# Vehicle:
# Modelo que representa los datos comerciales de los clientes
class Vehicle(models.Model):
    VehicleID = models.CharField(max_length=40)
    ClientID = models.CharField(max_length=40)
    VehicleType = models.ForeignKey(VehicleType, null=True, on_delete=models.SET_NULL, verbose_name='Seleccione tipo de transporte')
    VehiclePatent = models.CharField(
        max_length=10, verbose_name='Patente de vehículo')
    VehicleModel = models.CharField(
        max_length=100, verbose_name='Tipo vehículo')
    VehicleCapacity = models.IntegerField(
        default=0, help_text='(ej: 5200,5)', verbose_name='Capacidad de carga en Kg')
    VehicleAvailable = models.BooleanField(
        help_text='(ej: Si)', verbose_name='Vehículo disponible')
    User = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    class meta:
        ordering = ('id',)

    def __str__(self):
        return self.VehiclePatent

    def get_absolute_url(self):
            return reverse('detalleTransporte', args=[self.id])

    def get_update_url(self):
        return reverse('editarTransporte', args=[self.id])

    def get_confirmdelete_url(self):
        return reverse('confirmDeleteTransport', args=[self.id])

    def get_delete_url(self):
        return reverse('eliminarTransporte', args=[self.id])                         