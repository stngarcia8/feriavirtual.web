import uuid
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class VehicleType(models.Model):
    "Representa el tipo de transporte"
    VehicleTypeID = models.IntegerField(default=1)
    VehicleTypeDescription = models.CharField(
        max_length=100, verbose_name='Tipo transporte')

    class Meta:
        ordering = ('VehicleTypeID',)

    def __str__(self):
        return self.VehicleTypeDescription


class Vehicle(models.Model):
    "Representa un vehiculo del transportista."
    disponibilidad = ((1, 'Disponible'), (0, 'Inhabilitado'))

    VehicleID = models.UUIDField(default=uuid.uuid4, unique=True)
    ClientID = models.CharField(max_length=40, blank=True, null=True)
    VehicleType = models.ForeignKey(
        VehicleType, null=True, on_delete=models.SET_NULL, verbose_name='Seleccione tipo de transporte')
    VehiclePatent = models.CharField(
        max_length=10, verbose_name='Patente del vehículo')
    VehicleModel = models.CharField(
        max_length=100, verbose_name='Modelo')
    VehicleCapacity = models.IntegerField(
        default=0, help_text='(ej: 5200)', verbose_name='Capacidad de carga(KG)')
    VehicleAvailable = models.IntegerField(default=1, choices=disponibilidad,
                                           verbose_name='Disponibilidad')
    Observation = models.CharField(
        max_length=100, null=True, blank=True, verbose_name='Observación')
    User = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.VehiclePatent = self.VehiclePatent.upper()
        self.VehicleModel = self.VehicleModel.upper()
        self.Observation = self.Observation.upper()
        super(Vehicle, self).save(*args, **kwargs)

    class meta:
        ordering = ('id',)

    def __str__(self):
        return self.VehiclePatent

    def get_absolute_url(self):
        "Define la ruta absoluta del vehiculo."
        return reverse('detalleVehiculo', args=[self.id])

    def get_update_url(self):
        "Define la ruta de actualización del vehiculo."
        return reverse('editarVehiculo', args=[self.id])

    def get_delete_url(self):
        "Define la ruta de eliminación del vehiculo."
        return reverse('eliminarVehiculo', args=[self.id])


