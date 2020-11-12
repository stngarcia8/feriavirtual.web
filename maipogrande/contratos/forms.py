from django.forms import ModelForm, Textarea, HiddenInput
from .models import Contract


class ContractForm(ModelForm):
    "Formulario para la aceptación o rechazo de los contratos."

    class Meta:
        model = Contract
        fields = (
            'ProfileId', 'ContractId', 'ClientId',
            'CustomerObservation',
            'Status', 'StatusDescription', )
        widgets = {
            'ProfileId': HiddenInput(),
            'ContractId': HiddenInput(),
            'ClientId': HiddenInput(),
            'CustomerObservation': Textarea(attrs={'cols': 30, 'rows': 3}),
            'Status': HiddenInput(),
            'StatusDescription': HiddenInput(),
        }
