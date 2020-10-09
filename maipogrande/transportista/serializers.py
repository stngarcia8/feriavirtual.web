from rest_framework import serializers
from .models import Vehicle, VehicleType

# TransportSerializer:
# Serializador de los datos de vehiculos.
class TransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ('VehicleType', 'VehiclePatent', 'VehicleModel', 'VehicleCapacity',
                  'VehicleAvailable')

# VehicleTypeSerializer:
# Serializador de los tipos de transporte.
class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = ('VehicleTypeID', 'VehicleType')
        


# TransportistaSaveSerializer:
# Serializador que permite evaluar los datos provenientes de la api
# # para poder almacenarlosde forma correcta en el almacenamiento temporal.
class TransportSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ('VehicleType', 'VehiclePatent', 'VehicleModel', 'VehicleCapacity',
                  'VehicleAvailable')
        depth = 1
