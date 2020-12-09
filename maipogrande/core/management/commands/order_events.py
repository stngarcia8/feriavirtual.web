from ordenes.models import Order


class OrderEvents(object):
    "Procesa los eventos de las ordenes de compra.."
    evento = ''
    json_data = ''

    def __init__(self, evento, json_data):
        self.evento = evento
        self.json_data = json_data

    def event_executor(self):
        if self.evento == 'PRODUCTSPROPOSED':
            self.__notificar_productos_orden(self.json_data)
        elif self.evento == 'CHANGESTATUS':
            self.__notificar_estado_orden(self.json_data)

    def __notificar_productos_orden(self, json_data):
        "Notifica el cambio de estado de la orden de compra y agrega los precios."
        try:
            orden_compra = Order.objects.get(OrderId=json_data['OrderId'])
            orden_compra.NetValue = json_data['NetValue']
            orden_compra.Iva = json_data['Iva']
            orden_compra.TotalValue = json_data['TotalValue']
            orden_compra.DiscountValue = json_data['DiscountValue']
            orden_compra.Amount = json_data['Amount']
            orden_compra.Status = 2
            orden_compra.save()
            print("La orden de compra {0} tiene sus valores asignados.".format(json_data['OrderId']))
        except Exception:
            print("No fue posible asignar los valores a la orden de compra {0}.".format(json_data['OrderId']))
        return

    def __notificar_estado_orden(self, json_data):
        "Notifica el cambio de estado de una orden de compra."
        try:
            orden_compra = Order.objects.get(OrderId=json_data['Id'])
            orden_compra.Status = json_data['Status']
            orden_compra.save()
            print("La orden de compra {0} cambio su status a {1}.".format(json_data['Id'], json_data['Status']))
        except Exception:
            print("No fue posible cambiar el estado de la orden de compra {0} a {1}.".format(json_data['Id'], json_data['Status']))
        return

