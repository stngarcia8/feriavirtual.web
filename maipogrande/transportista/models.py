import datetime
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class VehicleType(models.Model):
    "Representa el tipo de transporte"
    VehicleTypeId = models.IntegerField(default=1)
    VehicleTypeDescription = models.CharField(
        max_length=100, verbose_name='Tipo transporte')

    class Meta:
        ordering = ('VehicleTypeId',)

    def __str__(self):
        return self.VehicleTypeDescription


class Vehicle(models.Model):
    "Representa un vehiculo del transportista."
    disponibilidad = ((1, 'Disponible'), (0, 'Inhabilitado'))

    VehicleId = models.UUIDField(default=uuid.uuid4, unique=True)
    ClientId = models.CharField(max_length=40, blank=True, null=True)
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
        self.Observation = self.Observation.upper() if self.Observation else ''
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


class Auction(models.Model):
    "Clase que representa una subasta."
    AuctionId = models.UUIDField(default=uuid.uuid4, unique=True, blank=True)
    AuctionDate = models.DateField(default=datetime.date.today)
    Percent = models.FloatField(default=0)
    Value = models.FloatField(default=0)
    Weight = models.FloatField(default=0)
    LimitDate = models.DateField(default=datetime.date.today)
    Observation = models.CharField(max_length=100, blank=True, null=True)
    CompanyName = models.CharField(max_length=100, blank=True, null=True)
    Destination = models.CharField(max_length=200, blank=True, null=True)
    PhoneNumber = models.CharField(max_length=50, blank=True, null=True)
    Status = models.IntegerField(default=0)

    class Meta:
        ordering = ('AuctionDate',)

    def __str__(self):
        return self.AuctionDate

    def get_participar_url(self):
        "Define la ruta de participación de la subasta."
        return reverse('participarSubasta', args=[self.id])


class AuctionProduct(models.Model):
    "Representa un producto dentro de la subasta."
    Product = models.CharField(blank=True, max_length=50, null=True)
    UnitValue = models.FloatField(default=0)
    Quantity = models.FloatField(default=0)
    TotalValue = models.FloatField(default=0)
    Auction = models.ForeignKey(Auction, null=True, on_delete=models.CASCADE)

    class meta:
        ordering = ('Product',)

    def __str__(self):
        return self.Product


def get_default_my_hour():
    hour = timezone.now()
    formatedHour = hour.strftime("%H:%M:%S")
    return formatedHour


class BidModel(models.Model):
    "Clase que representa la puja en una subasta."
    ValueId = models.UUIDField(default=uuid.uuid4, unique=True, blank=True)
    AuctionId = models.CharField(max_length=40, blank=True, null=True)
    ClientId = models.CharField(max_length=40, blank=True, null=True)
    Value = models.IntegerField(default=0, verbose_name='Puja')
    Hour = models.CharField(max_length=50, default=get_default_my_hour, null=True)
    Date = models.DateField(default=datetime.date.today)
    Bidder = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ('Value',)
