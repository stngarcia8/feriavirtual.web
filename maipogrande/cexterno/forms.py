from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from .models import Order, OrderDetail


class OrderForm(ModelForm):
    "Formulario para encabezado de orden de compra."

    class Meta:
        model = Order
        fields = ('PaymentCondition', 'OrderDate', 'OrderDiscount', 'Observation', )


class OrderDetailForm(ModelForm):
    "Formulario para detalle de orden de compra."

    class Meta:
        model = OrderDetail
        fields = ('Product', 'Quantity', )


OrderDetailFormSet = inlineformset_factory(
    Order, OrderDetail,
    form=OrderDetailForm,
    extra=4, fields=('Product', 'Quantity', ))
