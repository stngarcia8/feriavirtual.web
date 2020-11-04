from rest_framework import serializers
from .models import Vehicle, VehicleType, AuctionProduct, Auction, BidModel


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


class AuctionProductSerializer(serializers.ModelSerializer):
    "Serializador para los productos de las subastas"
    class Meta:
        model = AuctionProduct
        fields = ('Product', 'UnitValue', 'Quantity', 'TotalValue', )


class AuctionSerializer(serializers.ModelSerializer):
    "Serializador para las subastas."
    Products = AuctionProductSerializer(many=True)

    class Meta:
        model = Auction
        fields = ('AuctionID', 'AuctionDate', 'Percent', 'Value',
                  'Weight', 'LimitDate', 'Observation', 'Status', 'Products', )
        depth = 1

    def create(self, data):
        auc = Auction.objects.create(
            AuctionID=data['AuctionID'], AuctionDate=data['AuctionDate'],
            Percent=data['Percent'], Value=data['Value'], Weight= data['Weight'],
            LimitDate=data['LimitDate'], Observation=data['Observation'],
            Status=data['Status']
        )
        Products = AuctionProductSerializer(data=data['Products'], many=True)
        Products.is_valid()
        Products.save(Auction=auc)
        return auc


class AuctionParticipateSerializer(serializers.ModelSerializer):
    "Serializador para participar en subastas"
    class Meta:
        model = BidModel
        fields = ('ValueID', 'AuctionID', 'ClientID', 'Value', )
        depth = 1

    def create(self, data):
        bid = BidModel.objects.create(*data)
        return bid    
