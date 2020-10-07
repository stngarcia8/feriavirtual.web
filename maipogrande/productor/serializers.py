from rest_framework import serializers
from.models import Producto


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ('ProductName', 'Observation',
                  'ProductValue', 'ProductQuantity')


class ProductoSaveSerializer(serializers.ModelSerializer):
    User_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Producto
        depth = 1
        fields = ('ProductName', 'Observation',
                  'ProductValue', 'ProductQuantity', 'User_id')
