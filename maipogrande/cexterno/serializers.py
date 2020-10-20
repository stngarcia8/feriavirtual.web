from rest_framework import serializers
from.models import ExportProduct


class ExportProductSerializer(serializers.ModelSerializer):
    "Serializador de la lista de productos de exportación."

    class Meta:
        model = ExportProduct
        fields = ('ProductName', 'User',)

    def create(self, data):
        "Almacena el serializer con el usuario asociado."
        pro = ExportProduct.objects.create(
            ProductName=data['ProductName'], User=data['User'])
        return pro
