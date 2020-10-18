import uuid
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Producto(models.Model):
    "Modelo que representa un producto en el sistema"
    ProductID = models.UUIDField(default=uuid.uuid4, unique=True)
    ClientID = models.CharField(max_length=40, blank=True, null=True)
    ProductName = models.CharField(
        max_length=50, verbose_name='Nombre producto')
    Observation = models.CharField(
        max_length=100, null=True, blank=True, verbose_name='Observación')
    ProductValue = models.FloatField(
        default=0, verbose_name='Valor del producto')
    ProductQuantity = models.FloatField(
        default=0, verbose_name='Cantidad de productos (medido en KG)')
    User = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

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

    def __str(self):
        "Define el metodo __str del modelo mostrando el nombre del producto."
        return self.ProductName
