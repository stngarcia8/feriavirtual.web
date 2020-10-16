from django.forms import ModelForm, Textarea, TextInput, NumberInput, HiddenInput, Select, RadioSelect
from .models import Vehicle, VehicleType


class CreateVehiculoForm(ModelForm):
    "Formulario para crear vehiculos."
    class Meta:
        model = Vehicle
        fields = (
            'VehicleID', 'ClientID','VehicleType', 
            'VehiclePatent', 'VehicleModel', 'VehicleCapacity',
        )
        widgets = {
            'VehicleID': HiddenInput(),
            'ClientID': HiddenInput(),
            'VehicleType': Select(attrs={'autofocus': ''}),
            'VehiclePatent': TextInput(attrs={'size': '15'}),
            'VehicleModel': TextInput(attrs={'size': '15'}),
            'VehicleCapacity': NumberInput(),
        }    


class UpdateVehiculoForm(ModelForm):
    "Formulario para actualizar los vehiculos"
    class Meta:
        model = Vehicle
        fields = (
            'VehicleID', 'ClientID','VehicleType', 
            'VehiclePatent', 'VehicleModel', 'VehicleCapacity',
            'VehicleAvailable',
        )
        widgets = {
            'VehicleID': HiddenInput(),
            'ClientID': HiddenInput(),
            'VehicleType': Select(attrs={'autofocus': ''}),
            'VehiclePatent': TextInput(attrs={'size': '15'}),
            'VehicleModel': TextInput(attrs={'size': '15'}),
            'VehicleCapacity': NumberInput(),
            'VehicleAvailable': RadioSelect(), 
        }    
