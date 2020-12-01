from rest_framework import serializers
from.models import Producto, Category, Venta


class CategorySerializer(serializers.ModelSerializer):
    "Serializador de las categorías de productos."
    class Meta:
        model = Category
        fields = ('CategoryId', 'CategoryName')


class ProductoSerializer(serializers.ModelSerializer):
    "Serializador de productos."
    Category = CategorySerializer()

    class Meta:
        model = Producto
        fields = ('ProductId', 'ClientId', 'ProductName', 'Category', 'ProductValue', 'ProductQuantity', 'Observation', 'User')
        depth = 1

    def create(self, data):
        "Permite recibir parámetros en el evento save()"
        id = data['Category']['CategoryId']
        category = Category.objects.get(id=id)
        prod = Producto.objects.create(
            ProductId=data['ProductId'], ClientId=data['ClientId'],
            ProductName=data['ProductName'], Category=category,
            ProductValue=data['ProductValue'], ProductQuantity=data['ProductQuantity'],
            Observation=data['Observation']
        )
        return prod


class ProductoApiSerializer(serializers.ModelSerializer):
    "Almacena los datos para enviarlos a la api feria virtual"
    Category = CategorySerializer()

    class Meta:
        model = Producto
        fields = ('ProductId', 'ClientId', 'ProductName', 'Category', 'ProductValue', 'ProductQuantity', 'Observation')
        depth = 1


class VentaSerializer(serializers.ModelSerializer):
    "Serializador de ventas."
    class Meta:
        model = Venta
        fields = ('PaymentId', 'ClientId', 'SalesDate', 'Quantity', 'ProductName', 'UnitPrice', 'ProductPrice')

