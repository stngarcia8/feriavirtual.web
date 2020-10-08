from django.forms import ModelForm
from .models import Producto

# ProductoForm
# Formulario de los productos
class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = ('ProductName', 'Observation',
                  'ProductValue', 'ProductQuantity')
