from django.forms import ModelForm, Textarea, TextInput, NumberInput, HiddenInput, Select, RadioSelect
from .models import Vehicle, Auction, BidModel


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
            'VehiclePatent': TextInput(attrs={'size': '15', 'pattern': "[ÑA-Zña-z0-9]+$", 'minlength': 4, 
                'oninvalid':"setCustomValidity('Ingrese una patente válida')", 'oninput':"setCustomValidity('')"}),
            'VehicleModel': TextInput(attrs={'size': '15', 'minlength': 5, 'pattern': "[ña-zÑA-ZáéíóúÁÉÍÓÚ]+$",
                'oninvalid':"setCustomValidity('Ingrese un modelo válido')", 'oninput':"setCustomValidity('')"}),
            'VehicleCapacity': NumberInput(attrs={'min': 1, 'pattern': "^[0-9]+$",
                'oninvalid':"setCustomValidity('Ingrese una capacidad válida')", 'oninput':"setCustomValidity('')",
                'onkeypress':"return event.charCode >=46"}),
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
            'VehiclePatent': TextInput(attrs={'size': '15', 'pattern': "[ÑA-Zña-z0-9]+$", 'minlength': 4, 
                'oninvalid':"setCustomValidity('Ingrese una patente válida')", 'oninput':"setCustomValidity('')"}),
            'VehicleModel': TextInput(attrs={'size': '15', 'minlength': 5, 'pattern': "[ña-zÑA-ZáéíóúÁÉÍÓÚ]+$",
                'oninvalid':"setCustomValidity('Ingrese un modelo válido')", 'oninput':"setCustomValidity('')"}),
            'VehicleCapacity': NumberInput(attrs={'min': 1, 'pattern': "^[0-9]+$",
                'oninvalid':"setCustomValidity('Ingrese una capacidad válida')", 'oninput':"setCustomValidity('')",
                'onkeypress':"return event.charCode >=46"}),
            'VehicleAvailable': RadioSelect(),
            'Observation': Textarea(attrs={'cols': 30, 'rows': 3}),
        }


class AuctionParticipateForm(ModelForm):
    "Formulario para participar en subasta"
    class Meta:
        model = BidModel
        fields = (
            'ValueID', 'AuctionID', 'ClientID', 'Value',
        )
        widgets = {
            'ValueID': HiddenInput(),
            'AuctionID': HiddenInput(),
            'ClientID': HiddenInput(),
            'Hour':HiddenInput(),
            'Value': NumberInput(attrs={'min': 1, 'pattern': "^[1-9]+$",'max': 'subasta.Value',
            'oninvalid':"setCustomValidity('Ingrese una puja válida')", 'oninput':"setCustomValidity('')",
            'onkeypress':"return event.charCode >=46"}),
        }        
