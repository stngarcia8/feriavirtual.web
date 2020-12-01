import uuid
import datetime
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    "Representa la categoría de un producto."
    CategoryId = models.IntegerField(default=1)
    CategoryName = models.CharField(
        max_length=25, verbose_name='Categoría de producto')

    class Meta:
        ordering = ('CategoryId',)

    def __str__(self):
        return self.CategoryName


class Producto(models.Model):
    "Modelo que representa un producto en el sistema"
    ProductId = models.UUIDField(default=uuid.uuid4, unique=True)
    ClientId = models.CharField(max_length=40, blank=True, null=True)
    ProductName = models.CharField(
        max_length=50,verbose_name='Nombre producto')
    Category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, verbose_name='Seleccione categoría de producto')
    ProductValue = models.FloatField(
        default=0, verbose_name='Valor del producto (por KG)')
    ProductQuantity = models.FloatField(
        default=0, verbose_name='Cantidad de productos (medido en KG)')
    Observation = models.CharField(
        max_length=100, null=True, blank=True, verbose_name='Observación')
    User = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.ProductName = self.ProductName.upper()
        self.Observation = self.Observation.upper() if self.Observation else ''
        super(Producto, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'producto'
        verbose_name_plural = 'productos'
        ordering = ('id',)

    def get_absolute_url(self):
        "Genera la url para la visualización de cada instancia de un producto."
        return reverse('detalleProducto', args=[self.id])

    def get_update_url(self):
        "Genera la url para la actualización de cada instancia de un producto."
        return reverse('editarProducto', args=[self.id])

    def get_delete_url(self):
        "Genera la url para la eliminación de cada instancia del modelo."
        return reverse('eliminarProducto', args=[self.id])

    def __str__(self):
        "Define el metodo __str__ del modelo mostrando el nombre del producto."
        return self.ProductName.upper()


class Venta(models.Model):
    "Modelo que representa las ventas del productor"
    PaymentId = models.CharField(max_length=40, blank=True, null=True)
    ClientId = models.CharField(max_length=40, blank=True, null=True)
    SalesDate = models.DateField(default=datetime.date.today)
    Quantity = models.FloatField(default=0)
    ProductName = models.CharField(max_length=50)
    UnitPrice = models.FloatField(default=0)
    ProductPrice = models.FloatField(default=0)
