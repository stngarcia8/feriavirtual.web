from django.forms import ModelForm, HiddenInput, NumberInput, Select, Textarea, TextInput
from django.forms.models import inlineformset_factory
from .models import Order, OrderDetail, Payment
from productor.models import Producto, Category


class OrderForm(ModelForm):
    "Formulario para encabezado de orden de compra."

    class Meta:
        model = Order
        fields = ('OrderId', 'ClientId', 'PaymentCondition', 'OrderDate',
                  'OrderDiscount', 'Observation',)
        widgets = {
            'OrderId': HiddenInput(),
            'ClientId': HiddenInput(),
            'User': HiddenInput(),
            'OrderDate': TextInput(attrs={'readonly':'readonly'}),
            'OrderDiscount': NumberInput(attrs={'min': 0, 'max': 5, 'onkeypress':"return event.charCode >= 46", 
                'oninvalid': "setCustomValidity('Descuento puede estar entre 0% y 5%')", 'oninput': "setCustomValidity('')"}),
            'Observation': Textarea(attrs={'cols': 30, 'rows': 3}),
        }


class OrderDetailForm(ModelForm):
    "Formulario para detalle de orden de compra."

    class Meta:
        model = OrderDetail
        fields = ('Product', 'Quantity', )
        widgets = {
            'Product': Select(attrs={'required': '', 'oninvalid': "setCustomValidity('Selecciona un producto de la lista')", 'oninput': "setCustomValidity('')"}),
            'Quantity': NumberInput(attrs={'min': 1, 'max': 9999, 'onkeypress':"return event.charCode >= 46", 
                'oninvalid': "setCustomValidity('El rango de productos permitidos es de 1 a 9999 kg')", 'oninput': "setCustomValidity('')"}),
        }


class OrderRefuseForm(ModelForm):
    "Formulario para rechazar un contrato"

    class Meta:
        model = Order
        fields = ( 'OrderId', 'ClientId', 'CustomerObservation', 'Status', )
        widgets = {
            'ClientId': HiddenInput(),
            'OrderId': HiddenInput(),
            'CustomerObservation': Textarea(attrs={'cols': 30, 'rows': 3}),
            'Status': HiddenInput(),
        }

class OrderAcceptForm(ModelForm):
    "Formulario para aceptar un contrato"

    class Meta:
        model = Payment
        fields = ( 'PaymentId', 'ClientId', 'OrderId', 'PaymentMethod',
                    'PaymentDate', 'Amount', 'Observation', )
        widgets = {
            'PaymentId': HiddenInput(),
            'ClientId': HiddenInput(),
            'OrderId': HiddenInput(),
            'PaymentMethod': Select(attrs={'required': '', 'oninvalid': "setCustomValidity('Selecciona un método de pago de la lista')", 'oninput': "setCustomValidity('')"}),
            'Observation': Textarea(attrs={'required': '', 'cols': 30, 'rows': 3}),
        }        


OrderDetailFormSet = inlineformset_factory(
    Order, OrderDetail,
    form=OrderDetailForm, extra=0, min_num=1, max_num=20,
    fields=('Product', 'Quantity', ),
    can_delete=True, widgets={'Product': Select(attrs={'required': '', 'oninvalid': "setCustomValidity('Selecciona un producto de la lista')", 'oninput': "setCustomValidity('')"}),
            'Quantity': NumberInput(attrs={'required': '', 'min': 1, 'max': 9999, 'onkeypress':"return event.charCode >= 46", 
                'oninvalid': "setCustomValidity('El rango de productos permitidos es de 1 a 9999 kg')", 'oninput': "setCustomValidity('')"})})
