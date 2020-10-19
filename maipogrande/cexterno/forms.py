from django.forms import ModelForm, Textarea, TextInput, NumberInput, HiddenInput, Select, DateInput
from django.forms.models import modelformset_factory, inlineformset_factory
from .models import Order, OrderDetail


class OrderForm(ModelForm):
    "Formulario para encabezado de orden de compra."

    class Meta:
        model = Order
        fields = (
            'OrderID', 'ClientID', 'PaymentCondition',
            'OrderDate', 'OrderDiscount', 'Observation', )
        widgets = {
            'OrderID': HiddenInput(),
            'ClientID': HiddenInput(),
            'PaymentCondition': Select(),
            'OrderDate': DateInput(),
            'OrderDiscount': NumberInput(),
            'Observation': TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })



class OrderDetailForm(ModelForm):
    "Formulario para detalle de orden de compra."

    class Meta:
        model = OrderDetail
        fields = ('OrderDetailID', 'Product', 'Quantity', )
        widgets = {
            'OrderDetailID': HiddenInput(),
            'Product': Select(),
            'Quantity': NumberInput(),
        }

    def __init__(self, *args, **kwargs):
        super(OrderDetailForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })



OrderDetailFormSet = inlineformset_factory(Order, OrderDetail, form=OrderDetailForm, extra=4)
