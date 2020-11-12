from rest_framework import serializers
from .models import Vehicle, VehicleType, AuctionProduct, Auction, BidModel


class VehicleTypeSerializer(serializers.ModelSerializer):
    "Serializador para los tipos de transportes"

    class Meta:
        model = VehicleType
        fields = ('VehicleTypeId', 'VehicleTypeDescription')


class VehiculoSerializer(serializers.ModelSerializer):
    "Serializador de los vehiculos."
    VehicleType = VehicleTypeSerializer()

    class Meta:
        model = Vehicle
        fields = ('VehicleId', 'ClientId', 'VehicleType',
                  'VehiclePatent', 'VehicleModel', 'VehicleCapacity',
                  'VehicleAvailable', 'Observation', 'User',)
        depth = 1

    def create(self, data):
        "Permite recibir parámetros en el evento save()"
        id = data['VehicleType']['VehicleTypeId']
        vehicle_type = VehicleType.objects.get(VehicleTypeId=id)
        veh = Vehicle.objects.create(
            VehicleId=data['VehicleId'], ClientId=data['ClientId'],
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
        fields = ('VehicleId', 'ClientId', 'VehicleType',
                  'VehiclePatent', 'VehicleModel', 'VehicleCapacity',
                  'VehicleAvailable', 'Observation',)
        depth = 1


class AuctionProductSerializer(serializers.ModelSerializer):
    "Serializador para los productos de las subastas"

    class Meta:
        model = AuctionProduct
        fields = ('Product', 'UnitValue', 'Quantity', 'TotalValue',)


class AuctionSerializer(serializers.ModelSerializer):
    "Serializador para las subastas."
    Products = AuctionProductSerializer(many=True)

    class Meta:
        model = Auction
        fields = ('AuctionId', 'AuctionDate', 'Percent', 'Value',
                  'Weight', 'LimitDate', 'Observation', 'CompanyName', 'Destination',
                  'PhoneNumber', 'Status', 'Products',)
        depth = 1

    def create(self, data):
        auc = Auction.objects.create(
            AuctionId=data['AuctionId'], AuctionDate=data['AuctionDate'],
            Percent=data['Percent'], Value=data['Value'], Weight=data['Weight'],
            LimitDate=data['LimitDate'], Observation=data['Observation'],
            CompanyName=data['CompanyName'], Destination=data['Destination'],
            PhoneNumber=data['PhoneNumber'], Status=data['Status']
        )
        Products = AuctionProductSerializer(data=data['Products'], many=True)
        Products.is_valid()
        Products.save(Auction=auc)
        return auc


class BidValueSerializer(serializers.ModelSerializer):
    "Serializador para participar en subastas"

    class Meta:
        model = BidModel
        fields = ('ValueId', 'AuctionId', 'ClientId', 'Value',)
