import json
import requests
from django.conf import settings
from .models import Order
from .serializers import ExportProductSerializer, OrderSerializer


def GetExportProductFromApi(user):
    """ Carga la lista de productos.

        Carga los productos de exportación desde la base de datos de feria virtual.
        parámetros:
            - user: objeto que contiene la información del usuario actual.
        retorna:
            - True: Si cargo los datos
            - False: En caso de problemas de conectividad.
    """
    response = requests.get(
        url=settings.PRODUCTOR_SERVICE_URL_GET_EXPORTPRODUCT_ALL)
    if response.status_code != 200:
        return False
    serializador = ExportProductSerializer(data=response.json(), many=True)
    serializador.is_valid()
    serializador.save(User=user)
    return True


def PostToApi(orderID):
    """ Almacena una nueva orden de compra.

        Permite almacenar los datos de la nueva orden de compra en la base de datos de feria virtual.
        parámetros:
            - orderID: identificador de la orden de compra aque almacenar.
        retorna:
            - True: La orden fue almacenado correctamente
            - False: Ocurrio algun problema y la orden no fue almacenado
    """
    orden = Order.objects.get(OrderID=orderID)
    orden_serializer = OrderSerializer(instance=orden)
    response = requests.post(
        url=settings.ORDER_SERVICE_URL_POST,
        headers=settings.SERVER_HEADERS,
        data=json.dumps(orden_serializer.data))
    return True if response.status_code == 200 else False


def PutToApi(orderID):
    """ Actualiza una orden de compra.

        Permite actualizar la información de una orden de compra en la base de datos de feria virtual.
        parámetros:
            - orderID: identificador de la orden de compra que será actualizada. a.
        retorna:
            - True: la orden de compra fue actualizada correctamente
            - False: Ocurrio algun problema y la orden no fue almacenada
    """
    orden = Order.objects.get(OrderID=orderID)
    orden_serializer = OrderSerializer(instance=orden)
    response = requests.put(
        url=settings.ORDER_SERVICE_URL_PUT,
        headers=settings.SERVER_HEADERS,
        data=json.dumps(orden_serializer.data))
    return True if response.status_code == 200 else False


def DeleteToApi(order_id):
    """Elimina una orden de compra.

        Elimina una orden de compra de la base de datos de feria virtual.
        parámetros:
            - order_id: corresponde al identificador de la orden de compra que se quiere eliminar.
        retorna:
            - True: Si la orden se eliminó correctamente.
            - False: En caso de problemas o errores.
    """
    response = requests.delete(
        url=settings.ORDER_SERVICE_URL_DELETE,
        params={'orderID': order_id})
    return True if response.status_code == 200 else False

