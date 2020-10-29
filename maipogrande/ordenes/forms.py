from django.forms import ModelForm, HiddenInput
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
        }


class OrderDetailForm(ModelForm):
    "Formulario para detalle de orden de compra."

    class Meta:
        model = OrderDetail
        fields = ('Product', 'Quantity', )


OrderDetailFormSet = inlineformset_factory(
    Order, OrderDetail,
    form=OrderDetailForm, extra=1,
    fields=('Product', 'Quantity', ),
    can_delete=True)
