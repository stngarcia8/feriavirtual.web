from django.db import models
from django.urls import reverse
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
    User = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)

    def get_absolute_url(self):
        return reverse('detalleProducto', args=[self.id])    

    # Por cada uno de los objetos de producto a cada uno le genera una url
    # Le pasamos por parametro la vista
    def get_update_url(self):
        return reverse('editarProducto', args=[self.id])

    def get_delete_url(self):
        return reverse('eliminarProducto', args=[self.id])    

    def __str(self):
        return self.ProductName

    def get_confirmdelete_url(self):
        return reverse('confirmDeleteProduct', args=[self.id])    

