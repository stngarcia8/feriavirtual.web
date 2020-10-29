from rest_framework import serializers
from .models import Order, OrderDetail


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
        model = Order
        fields = ('OrderID', 'ClientID', 'ConditionID',
                  'ConditionDescription', 'OrderDiscount',
                  'Observation', 'OrderDetail', )
        depth = 1
