from django import forms
from django.forms import ModelForm
from .models import Vehicle, VehicleType

# TransportForm()
# Formulario de mantenimiento de los datos comerciales de los usuarios
class TransporteForm(ModelForm):
    class Meta:
        model = Vehicle
        fields = ('VehicleType', 'VehiclePatent', 'VehicleModel', 'VehicleCapacity',
                  'VehicleAvailable')
