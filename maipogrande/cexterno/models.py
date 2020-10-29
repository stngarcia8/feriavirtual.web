from django.db import models
from django.contrib.auth.models import User


class ExportProduct(models.Model):
    "Representa los datos mínimos que un cliente puede seleccionar para una orden de compra."
    ProductName = models.CharField(
        max_length=50, verbose_name='Producto')
    User = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ('ProductName',)

    def __str__(self):
        return self.ProductName
