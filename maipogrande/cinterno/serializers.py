from rest_framework import serializers
from .models import ExportInternalProduct


class ExportInternalProductSerializer(serializers.ModelSerializer):
    "Serializador de la lista de productos de exportación."

    class Meta:
        model = ExportInternalProduct
        fields = ('ProductName', 'User',)

    def create(self, data):
        "Almacena el serializer con el usuario asociado."
        pro = ExportInternalProduct.objects.create(
            ProductName=data['ProductName'], User=data['User'])
        return pro