from productor.models import Producto

class ProductEvents(object):
    "Procesa los eventos asociados a los productos."
    evento = ''
    json_data = ''

    def __init__(self, evento, json_data):
        self.evento = evento
        self.json_data = json_data

    def event_executor(self):
        if self.evento == 'UPDATESTOCK':
            self.__actualizar_stock(self.json_data)

    def __actualizar_stock(self, json_data):
        "Actualiza el stock de los productos en la base de datos."
        try:
            producto = Producto.objects.get(ProductId=json_data['ProductId'])
            producto.ProductQuantity= json_data['Stock']
            producto.save()
            print("El stock del producto {0} fue actualizado.".format(json_data['ProductId']))
        except Exception:
            print("El stock del producto {0} no fue posible actualizarlo.".format(json_data['ProductId']))
        return