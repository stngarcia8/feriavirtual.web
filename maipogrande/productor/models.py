from django.db import models
from django.contrib.auth.models import User


# Producto
# Clase que representa un producto relacionado a un productor en el sistema
class Producto(models.Model):
    ProductID = models.CharField(max_length=40, blank=True)
    ClientID = models.CharField(max_length=40, blank=True)
    ProductName = models.CharField(
        max_length=50, verbose_name='Nombre producto')
    Observation = models.CharField(max_length=100, verbose_name='Observación')
    ProductValue = models.DecimalField(
        max_digits=9, decimal_places=2, verbose_name='Valor del producto')
    ProductQuantity = models.DecimalField(
        max_digits=9, decimal_places=2, verbose_name='Cantidad de productos (medido en KG)')
    User = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ('id',)

    def __str(self):
        return self.ProductName
