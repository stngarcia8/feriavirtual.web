from django.forms import ModelForm, HiddenInput, NumberInput
from django.forms.models import inlineformset_factory
from .models import Order, OrderDetail


class OrderForm(ModelForm):
    "Formulario para encabezado de orden de compra."

    class Meta:
        model = Order
        fields = ('OrderID', 'ClientID', 'PaymentCondition', 'OrderDate',
                  'OrderDiscount', 'Observation', )
        widgets = {
            'OrderID': HiddenInput(),
            'ClientID': HiddenInput(),
            'User': HiddenInput(),
            'OrderDiscount': NumberInput(attrs={'min': 0, 'max': 100, 'onkeypress':"return event.charCode >= 46", 
                'oninvalid': "setCustomValidity('Ingrese un número válido')", 'oninput': "setCustomValidity('')"}),
        }


class OrderDetailForm(ModelForm):
    "Formulario para detalle de orden de compra."

    class Meta:
        model = OrderDetail
        fields = ('Product', 'Quantity', )
        widgets = {
            'Quantity': NumberInput(attrs={'min': 0.1, 'max': 999999999, 'onkeypress':"return event.charCode >= 46", 
                'oninvalid': "setCustomValidity('Ingrese un número válido')", 'oninput': "setCustomValidity('')"}),
        }


OrderDetailFormSet = inlineformset_factory(
    Order, OrderDetail,
    form=OrderDetailForm, extra=1,
    fields=('Product', 'Quantity', ),
    can_delete=True)
