from django import forms
from django.forms import ModelForm
from .models import Vehicle

# TransportForm()
# Formulario de mantenimiento de los datos comerciales de los usuarios
class TransportForm(ModelForm):
    class Meta:
        model = Vehicle
        fields = ('VehicleType', 'VehiclePatent', 'VehicleModel', 'VehicleCapacity',
                  'VehicleAvailable')
