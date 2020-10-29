from django.forms import ModelForm, HiddenInput
from django.forms.models import inlineformset_factory
from .models import InternalOrder, OrderDetail


class OrderForm(ModelForm):
    "Formulario para encabezado de orden de compra."

    class Meta:
        model = InternalOrder
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
    InternalOrder, OrderDetail,
    form=OrderDetailForm, extra=1,
    fields=('Product', 'Quantity', ),
    can_delete=True)