from rest_framework import serializers
from .models import Vehicle


# TransportSerializer:
# Serializador de los datos comerciales de los clientes.
class TransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ('VehicleType', 'VehiclePatent', 'VehicleModel', 'VehicleCapacity',
                  'VehicleAvailable')


class ProductoSaveSerializer(serializers.ModelSerializer):
    User_id = serializers.IntegerField(write_only=True)

# TransportistaSaveSerializer:
# Serializador que permite evaluar los datos provenientes de la api
# # para poder almacenarlosde forma correcta en el almacenamiento temporal.
class TransportistaSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ('VehicleType', 'VehiclePatent', 'VehicleModel', 'VehicleCapacity',
                  'VehicleAvailable', 'User_id')
        depth = 1
