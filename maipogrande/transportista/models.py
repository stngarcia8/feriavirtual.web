import uuid
import datetime
from django.db import models
from django.contrib.auth.models import User
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
    AuctionId = models.UUIDField(default=uuid.uuid4, blank=True)
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
        ordering = ('Status', 'AuctionDate', )

    def __str__(self):
        return self.AuctionDate

    def get_participar_url(self):
        "Define la ruta de participación de la subasta."
        return reverse('participarSubasta', args=[self.id])            

    def get_mostrar_resultado_pujas_url(self):
        "Define la ruta de participación de la subasta."
        return reverse('resultadosSubasta', args=[self.id])            




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
      hour = timezone.localtime(timezone.now())
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
        ordering = ('Value', )


class OrderDispatch(models.Model):
    "Clase que representa una orden de despacho."
    DispatchId = models.UUIDField(default=uuid.uuid4, unique=True, blank=True)
    OrderId = models.CharField(max_length=40, blank=True, null=True)
    ClientId = models.CharField(max_length=40, blank=True, null=True)
    DispatchDate = models.DateField(default=datetime.date.today)
    DispatchValue = models.FloatField(default=0)
    DispatchWeight = models.FloatField(default=0)
    Observation = models.CharField(max_length=100, blank=True, null=True)
    CompanyName = models.CharField(max_length=100, blank=True, null=True)
    Destination = models.CharField(max_length=200, blank=True, null=True)
    PhoneNumber = models.CharField(max_length=50, blank=True, null=True)
    Status = models.IntegerField(default=0)
    CarrierObservation = models.CharField(max_length=100, blank=True, null=True, verbose_name='Observación')
    User = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ('Status', 'DispatchDate', )

    def __str__(self):
        return self.ClientId

    def get_cambiar_estado_url(self):
        "Define la ruta de detalle despacho"
        return reverse('detalleDespacho', args=[self.id])

    def get_deliver_dispatch_url(self):
        "Genera la url para finalizar un despacho."
        return reverse('finalizarDespacho', args=[self.id])

    def get_cancel_dispatch_url(self):
        "Genera la url para cancelar un despacho."
        return reverse('cancelarDespacho', args=[self.id])


class DispatchProducts(models.Model):
    "Clase que representa el detalle de una orden de despacho"
    Product = models.CharField(blank=True, max_length=50, null=True)
    UnitValue = models.FloatField(default=0)
    Quantity = models.FloatField(default=0)
    TotalValue = models.FloatField(default=0)
    OrderDispatch = models.ForeignKey(OrderDispatch, null=True, on_delete=models.CASCADE)

    class meta:
        ordering = ('Product',)
    
    def __str__(self):
        return self.Product
