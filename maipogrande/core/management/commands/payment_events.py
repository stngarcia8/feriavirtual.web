from productor.serializers import VentaSerializer


class PaymentEvents(object):
    "Procesa los eventos de los pagos realizados por la venta de productos."
    evento = ''
    json_data = ''

    def __init__(self, evento, json_data):
        self.evento = evento
        self.json_data = json_data

    def event_executor(self):
        if self.evento == 'PRODUCTSPAYMENT':
            self.__crear_pago(self.json_data)

    def __crear_pago(self, json_data):
        "Registra un pago en la base de datos."
        try:
            serializador = VentaSerializer(data=json_data, many=False)
            serializador.is_valid()
            serializador.save()
            print("La venta del producto {0} fue registrado.".format(json_data['ProductName']))
        except Exception:
            print("La venta del producto {0} no fue posible registrarla.".format(json_data['ProductName']))
        return
