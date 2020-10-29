from rest_framework import serializers
from.models import ExportInternalProduct, InternalOrder, OrderDetail, OrderModel


class ExportProductSerializer(serializers.ModelSerializer):
    "Serializador de la lista de productos de exportación."

    class Meta:
        model = ExportInternalProduct
        fields = ('ProductName', 'User',)

    def create(self, data):
        "Almacena el serializer con el usuario asociado."
        pro = ExportInternalProduct.objects.create(
            ProductName=data['ProductName'], User=data['User'])
        return pro


class OrderDetailSerializer(serializers.ModelSerializer):
    "Serializador para el detalle de la orden de compra."

    class Meta:
        model = OrderDetail
        fields = ('OrderDetailID', 'OrderID', 'ProductName', 'Quantity', )


class OrderSerializer(serializers.ModelSerializer):
    "Serializador para las ordenes de compra."
    OrderDetail = serializers.SerializerMethodField('get_order_detail')

    def get_order_detail(self, obj):
        data = OrderDetail.objects.filter(Order=obj)
        serializador = OrderDetailSerializer(instance=data, many=True)
        return serializador.data

    class Meta:
        model = InternalOrder
        fields = ('OrderID', 'ClientID', 'ConditionID',
                  'ConditionDescription', 'OrderDiscount',
                  'Observation', 'OrderDetail', )
        depth = 1


class OrderApiSerializer(serializers.ModelSerializer):
    Order = OrderSerializer()
    OrderDetail = OrderDetailSerializer(many=True)

    class Meta:
        model = OrderModel
        fields = ('Order', 'OrderDetail', )
        depth = 1