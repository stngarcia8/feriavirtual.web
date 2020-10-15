from rest_framework import serializers
from.models import Producto


class ProductoSerializer(serializers.ModelSerializer):
    "Serializador de productos."
    class Meta:
        model = Producto
        fields = '__all__'

    def create(self, data):
        "Permite recibir parámetros en el evento save()"
        prod = Producto.objects.create(**data)
        return prod


class ProductoApiSerializer(serializers.ModelSerializer):
    "Almacena los datos para enviarlos a la api feria virtual"
    class Meta:
        model = Producto
        exclude = ('id', 'User',)
