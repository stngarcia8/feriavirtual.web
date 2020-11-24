import json
import requests
from django.conf import settings
from .models import Order
from .serializers import OrderSerializer, OrderRefuseSerializer


def PostToApi(orderId):
    """ Almacena una nueva orden de compra.

        Permite almacenar los datos de la nueva orden de compra en la base de datos de feria virtual.
        parámetros:
            - orderID: identificador de la orden de compra aque almacenar.
        retorna:
            - True: La orden fue almacenado correctamente
            - False: Ocurrio algun problema y la orden no fue almacenado
    """
    orden = Order.objects.get(OrderId=orderId)
    orden_serializer = OrderSerializer(instance=orden)
    response = requests.post(
        url=settings.ORDER_SERVICE_URL_POST,
        headers=settings.SERVER_HEADERS,
        data=json.dumps(orden_serializer.data))  
    return True if response.status_code == 200 else False


def PutToApi(orderId):
    """ Actualiza una orden de compra.

        Permite actualizar la información de una orden de compra en la base de datos de feria virtual.
        parámetros:
            - orderID: identificador de la orden de compra que será actualizada. a.
        retorna:
            - True: la orden de compra fue actualizada correctamente
            - False: Ocurrio algun problema y la orden no fue almacenada
    """
    orden = Order.objects.get(OrderId=orderId)
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
        params={'orderId': order_id})
    return True if response.status_code == 200 else False


def PostOrderRefuseToApi(serializador):
    """ Rechaza los productos

        Rechaza los productos por parte del cliente,
        permitiendo ingresar una observación a la cancelación.

        parametros:
            - serializador: objeto serializer que contiene los datos de rechazo.
        retorna:
            - True, en caso de realizar el rechazo correctamente.
            - false, en caso de problemas de envío o conectividad.
    """
    response = requests.patch(
        url=settings.ORDER_SERVICE_URL_REFUSE,
        headers=settings.SERVER_HEADERS,
        data=json.dumps(serializador.data))  
    print()
    print(response)
    print(settings.ORDER_SERVICE_URL_REFUSE)
    print(json.dumps(serializador.data))
    print()
    return True if response.status_code == 200 else False    


def PostAcceptToApi(serializador):
    """ Acepta los productos

        Acepta los productos por parte del cliente,
        permitiendo ingresar una observación a la aceptación.

        parametros:
            - serializador: objeto serializer que contiene los datos de rechazo.
        retorna:
            - True, en caso de realizar el rechazo correctamente.
            - false, en caso de problemas de envío o conectividad.
    """
    response = requests.post(
        url=settings.PAYMENT_SERVICE_URL_POST,
        headers=settings.SERVER_HEADERS,
        data=json.dumps(serializador.data))  
    print()
    print(response)
    print(settings.PAYMENT_SERVICE_URL_POST)
    print(json.dumps(serializador.data))
    print()
    return True if response.status_code == 200 else False 