from django.forms import ModelForm, Textarea, TextInput, NumberInput, HiddenInput, Select, RadioSelect
from .models import Vehicle


class CreateVehiculoForm(ModelForm):
    "Formulario para crear vehiculos."
    class Meta:
        model = Vehicle
        fields = (
            'VehicleID', 'ClientID', 'VehicleType', 'VehiclePatent', 'VehicleModel', 'VehicleCapacity', 'Observation', )
        widgets = {
            'VehicleID': HiddenInput(),
            'ClientID': HiddenInput(),
            'VehicleType': Select(attrs={'autofocus': ''}),
            'VehiclePatent': TextInput(attrs={'size': '15'}),
            'VehicleModel': TextInput(attrs={'size': '15'}),
            'VehicleCapacity': NumberInput(),
            'Observation': Textarea(attrs={'cols': 30, 'rows': 3}),
        }


class UpdateVehiculoForm(ModelForm):
    "Formulario para actualizar los vehiculos"
    class Meta:
        model = Vehicle
        fields = (
            'VehicleID', 'ClientID', 'VehicleType',
            'VehiclePatent', 'VehicleModel', 'VehicleCapacity',
            'VehicleAvailable', 'Observation',
        )
        widgets = {
            'VehicleID': HiddenInput(),
            'ClientID': HiddenInput(),
            'VehicleType': Select(attrs={'autofocus': ''}),
            'VehiclePatent': TextInput(attrs={'size': '15'}),
            'VehicleModel': TextInput(attrs={'size': '15'}),
            'VehicleCapacity': NumberInput(),
            'VehicleAvailable': RadioSelect(),
            'Observation': Textarea(attrs={'cols': 30, 'rows': 3}),
        }
