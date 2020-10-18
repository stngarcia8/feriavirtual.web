from rest_framework import serializers
from .models import Vehicle, VehicleType


class VehicleTypeSerializer(serializers.ModelSerializer):
    "Serializador para los tipos de transportes"
    class Meta:
        model = VehicleType
        fields = ('VehicleTypeID', 'VehicleTypeDescription')


class VehiculoSerializer(serializers.ModelSerializer):
    "Serializador de los vehiculos."
    VehicleType = VehicleTypeSerializer()

    class Meta:
        model = Vehicle
        fields = ('VehicleID', 'ClientID', 'VehicleType',
                  'VehiclePatent', 'VehicleModel', 'VehicleCapacity',
                  'VehicleAvailable', 'Observation', 'User', )
        depth = 1

    def create(self, data):
        "Permite recibir parámetros en el evento save()"
        id = data['VehicleType']['VehicleTypeID']
        vehicle_type = VehicleType.objects.get(VehicleTypeID=id)
        veh = Vehicle.objects.create(
            VehicleID=data['VehicleID'], ClientID=data['ClientID'],
            VehicleType=vehicle_type, VehiclePatent=data['VehiclePatent'],
            VehicleModel=data['VehicleModel'], VehicleCapacity=data['VehicleCapacity'],
            VehicleAvailable=data['VehicleAvailable'],
            Observation=data['Observation'], User=data['User'])
        return veh


class VehiculoApiSerializer(serializers.ModelSerializer):
    "Almacena los datos para enviarlos a la api feria virtual"
    VehicleType = VehicleTypeSerializer()

    class Meta:
        model = Vehicle
        #exclude = ('id', 'User',)
        fields = ('VehicleID', 'ClientID', 'VehicleType',
                  'VehiclePatent', 'VehicleModel', 'VehicleCapacity',
                  'VehicleAvailable', 'Observation', )
        depth = 1
