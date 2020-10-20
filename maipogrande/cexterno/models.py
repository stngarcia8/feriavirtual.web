import uuid
import datetime
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from django.contrib.auth.models import User
from productor.models import Producto


class ExportProduct(models.Model):
    "Representa los datos mínimos que un cliente puede seleccionar para una orden de compra."
    ProductName = models.CharField(
        max_length=50, verbose_name='Producto')
    User = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ('ProductName',)

    def __str__(self):
        return self.ProductName


class PaymentCondition(models.Model):
    "Representa un metodo de pago de la orden de compra"
    ConditionID = models.IntegerField(default=1)
    ConditionDescription = models.CharField(
        max_length=25, verbose_name='Condición de pago')

    class Meta:
        ordering = ('ConditionID',)

    def __str__(self):
        return self.ConditionDescription


class Order(models.Model):
    "Representa la orden de compra de productos"
    OrderID = models.UUIDField(default=uuid.uuid4, unique=True)
    ClientID = models.CharField(
        max_length=40, blank=True, null=True)
    PaymentCondition = models.ForeignKey(
        PaymentCondition, null=True, on_delete=models.SET_NULL,
        verbose_name='Condiciones de pago')
    OrderDate = models.DateField(
        default=datetime.date.today,
        help_text='Formato: dd/mm/aaaa',
        verbose_name='Fecha orden de compra')
    OrderDiscount = models.FloatField(
        default=0, verbose_name='¿Tiene descuento?',
        validators=[MinValueValidator(0), MaxValueValidator(10)])
    Observation = models.CharField(
        max_length=100, null=True, blank=True, verbose_name='Observación')
    User = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Orden de compra'
        verbose_name_plural = 'Ordenes de compras'
        ordering = ('id',)

    def get_absolute_url(self):
        "Define la ruta absoluta de las ordenes de compra."
        return reverse('verOrden', args=[self.id])        



    def __str__(self):
        return self.OrderID


class OrderDetail(models.Model):
    OrderDetailID = models.UUIDField(default=uuid.uuid4, unique=True)
    Order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE)
    Product = models.ForeignKey(
        ExportProduct, null=True, on_delete=models.SET_NULL, verbose_name='Seleccione producto')
    Quantity = models.FloatField(default=0, verbose_name='Cantidad de productos (medido en KG)',
                                 validators=[MinValueValidator(1), MaxValueValidator(99999)])

    class Meta:
        verbose_name = 'Detalle de orden'
        verbose_name_plural = 'Detalles de ordenes'
        ordering = ('id',)

    def __str(self):
        return self.OrderDetailID
