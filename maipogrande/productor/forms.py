from django.forms import ModelForm, Textarea, TextInput, NumberInput, HiddenInput, Select
from .models import Producto, Category


class ProductoForm(ModelForm):
    "Formulario para los productos"

    class Meta:
        model = Producto
        fields = (
            'ProductID', 'ClientID', 'ProductName',
            'Category', 'ProductValue', 'ProductQuantity',
            'Observation', )
        widgets = {
            'ProductID': HiddenInput(),
            'ClientID': HiddenInput(),
            'ProductName': TextInput(attrs={'size': '32', 'autofocus': '', 'minlength':3, 'pattern': "[ña-zÑA-ZáéíóúÁÉÍÓÚ]+$",
            'oninvalid':"setCustomValidity('Ingrese un nombre válido')", 'oninput':"setCustomValidity('')"}),
            'Category': Select(),
            'ProductValue': NumberInput(attrs={'min': 0.1, 'max': 999999999, 'onkeypress':"return event.charCode >= 46", 
                'oninvalid': "setCustomValidity('Ingrese un número válido')", 'oninput': "setCustomValidity('')"}),
            'ProductQuantity': NumberInput(attrs={'min': 0.1, 'max': 999999999, 'onkeypress':"return event.charCode >= 46", 
                'oninvalid': "setCustomValidity('Ingrese un número válido')", 'oninput': "setCustomValidity('')"}),
            'Observation': Textarea(attrs={'cols': 30, 'rows': 3}),
        }