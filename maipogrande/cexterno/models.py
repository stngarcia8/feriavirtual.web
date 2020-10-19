import uuid
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from productor.models import Producto


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
    OrderID = models.CharField(max_length=40, default=uuid.uuid4())
    ClientID = models.CharField(max_length=40, blank=True, null=True)
    PaymentCondition = models.ForeignKey(PaymentCondition, null=True, on_delete=models.SET_NULL, verbose_name='Condiciones de pago')
    OrderDate = models.DateField(auto_now_add=False )
    OrderDiscount = models.FloatField(
        default=0, verbose_name='¿Tiene descuento?')
    Observation = models.CharField(
        max_length=100, null=True, blank=True, verbose_name='Observación')
    User = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Orden de compra'
        verbose_name_plural = 'Ordenes de compras'
        ordering = ('id',)

    def __str__(self):
        return self.OrderID

class OrderDetail(models.Model):
    OrderDetailID = models.CharField(max_length=40, default=uuid.uuid4())
    Order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE)
    Product = models.ForeignKey(Producto, null=True, on_delete=models.SET_NULL, verbose_name='Seleccione producto')
    Quantity = models.FloatField(default=0, verbose_name='Cantidad de productos (medido en KG)')

    class Meta:
        verbose_name = 'Detalle de orden'
        verbose_name_plural = 'Detalles de ordenes'
        ordering = ('id',)

    def __str(self):
        return self.OrderDetailID
