import datetime
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Contract(models.Model):
    "Define la clase de los contratos del transportista."
    ContractId = models.CharField(max_length=40, blank=True, null=True)
    ClientId = models.CharField(max_length=40, blank=True, null=True)
    Customername = models.CharField(max_length=101, blank=True, null=True)
    CustomerDni = models.CharField(max_length=20, blank=True, null=True)
    CustomerEmail = models.CharField(max_length=255, blank=True, null=True)
    ContractObservation = models.CharField(max_length=100, blank=True, null=True)
    CustomerObservation = models.CharField(max_length=100, blank=True, null=True, verbose_name='ingrese observación')
    StartDate = models.DateField(default=datetime.date.today)
    EndDate = models.DateField(default=datetime.date.today)
    IsValid = models.IntegerField(default=0)
    ValidDescription = models.CharField(max_length=30, blank=True, null=True)
    ContractDescription = models.CharField(max_length=100, blank=True, null=True)
    CommisionValue = models.FloatField(default=0)
    AdditionalValue = models.FloatField(default=0)
    FineValue = models.FloatField(default=0)
    Status = models.IntegerField(default=0)
    StatusDescription = models.CharField(max_length=30, blank=True, null=True)
    ProfileId = models.IntegerField(default=0)
    User = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-StartDate', 'Status')

    def get_absolute_url(self):
        "Genera la url para la visualización de cada contrato."
        return reverse('detalleContrato', args=[self.id])

    def get_accept_contract_url(self):
        "Genera la url para aceptar un contrato."
        return reverse('aceptarContrato', args=[self.id])

    def get_refuse_contract_url(self):
        "Genera la url para rechazar un contrato."
        return reverse('rechazarContrato', args=[self.id])

    def __str__(self):
        return self.ContractDescription
