from django.forms import ModelForm, Textarea, TextInput, NumberInput, HiddenInput
from .models import Producto


class ProductoForm(ModelForm):
    "Formulario para los productos"

    class Meta:
        model = Producto
        fields = (
            'ProductID', 'ClientID', 'ProductName',
            'Observation', 'ProductValue', 'ProductQuantity',
        )
        widgets = {
            'ProductID': HiddenInput(),
            'ClientID': HiddenInput(),
            'ProductName': TextInput(attrs={'size': '32'}),
            'Observation': Textarea(attrs={'cols': 30, 'rows': 3}),
            'ProductValue': NumberInput(),
            'ProductQuantity': NumberInput(),
        }
