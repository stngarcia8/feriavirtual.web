import uuid
import datetime
from django.db import models
from productor.models import Producto
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from django.contrib.auth.models import User


class ExportProduct(models.Model):
    "Representa los datos mínimos que un cliente puede seleccionar para una orden de compra."
    ProductName = models.CharField(
        max_length=50, verbose_name='Producto')
    User = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ('ProductName',)

    def __str__(self):
        return self.ProductName.upper()


class PaymentCondition(models.Model):
    "Representa un metodo de pago de la orden de compra"
    ConditionId = models.IntegerField(default=1)
    ConditionDescription = models.CharField(
        max_length=25, verbose_name='Condición de pago')

    class Meta:
        ordering = ('ConditionId',)

    def __str__(self):
        return self.ConditionDescription


class Order(models.Model):
    "Representa la orden de compra de productos"
    OrderId = models.UUIDField(default=uuid.uuid4, unique=True, blank=True)
    ClientId = models.CharField(
        max_length=40, blank=True, null=True)
    PaymentCondition = models.ForeignKey(
        PaymentCondition, null=True, on_delete=models.SET_NULL,
        verbose_name='Condiciones de pago')
    ConditionId = models.IntegerField(default=1)
    ConditionDescription = models.CharField(max_length=25, blank=True)
    OrderDate = models.DateField(
        default=datetime.date.today,
        help_text='Formato: dd/mm/aaaa',
        verbose_name='Fecha orden de compra')
    OrderDiscount = models.FloatField(
        default=0, verbose_name='¿Tiene descuento?',
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    Observation = models.CharField(
        max_length=100, null=True, blank=True, help_text='(ej: 12345678-K)',verbose_name='Observación')
    Status = models.IntegerField(default=1)
    User = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.ConditionId = self.PaymentCondition.ConditionId
        self.ConditionDescription = self.PaymentCondition.ConditionDescription
        self.Observation = self.Observation.upper() if self.Observation else ''
        super(Order, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Orden de compra'
        verbose_name_plural = 'Ordenes de compras'
        ordering = ('id',)

    def get_absolute_url(self):
        "Define la ruta absoluta de las ordenes de compra."
        return reverse('verOrden', args=[self.id])

    def get_update_url(self):
        "Define la ruta de actualizacion de las ordenes de compra."
        return reverse('editarOrden', args=[self.id])

    def get_delete_url(self):
        "Define la ruta de eliminación de las ordenes de compra."
        return reverse('eliminarOrden', args=[self.id])

    def __str__(self):
        return self.OrderId


class OrderDetail(models.Model):
    "Clase que define el detalle de la orden de compra."
    OrderDetailId = models.UUIDField(default=uuid.uuid4, unique=True, blank=True)
    Order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE)
    OrderId = models.CharField(max_length=40, blank=True, null=True)
    Product = models.ForeignKey(Producto, null=True, on_delete=models.SET_NULL)
    ProductName = models.CharField(max_length=50, blank=True, null=True)
    Quantity = models.FloatField(default=0, verbose_name='Cantidad de productos (medido en KG)',
                                 validators=[MinValueValidator(1), MaxValueValidator(9999)])

    def save(self):
        self.OrderId = self.Order.OrderId
        self.ProductName = self.Product.ProductName.upper()
        super(OrderDetail, self).save()

    class Meta:
        verbose_name = 'Detalle de orden'
        verbose_name_plural = 'Detalles de ordenes'
        ordering = ('id',)

    def __str(self):
        return self.OrderDetailId
