import json
import requests
from django.conf import settings
from .serializers import ProductoApiSerializer, ProductoSerializer


def PostToApi(serializador):
    """ Almacena un nuevo producto.

        Permite almacenar los datos del nuevo producto en la base de datos de feria virtual.
        parámetros:
            - serializador: objeto serializer que contiene la información del producto.
        retorna:
            - True: El producto fue almacenado correctamente
            - False: Ocurrio algun problema y el producto no fue almacenado
    """
    data = ProductoApiSerializer(data=serializador.data)
    data.is_valid()
    response = requests.post(
        url=settings.PRODUCTOR_SERVICE_URL_POST,
        headers=settings.SERVER_HEADERS,
        data=json.dumps(data.data))
    return True if response.status_code == 200 else False


def PutToApi(serializador):
    """ Actualiza un producto.

        Permite actualizar los datos del producto en la base de datos de feria virtual.
        parámetros:
            - serializador: objeto serializer que contiene la información del producto.
        retorna:
            - True: El producto fue almacenado correctamente
            - False: Ocurrio algun problema y el producto no fue almacenado
    """
    data = ProductoApiSerializer(data=serializador.data)
    data.is_valid()
    response = requests.put(
        url=settings.PRODUCTOR_SERVICE_URL_PUT,
        headers=settings.SERVER_HEADERS,
        data=json.dumps(data.data))
    return True if response.status_code == 200 else False


def DeleteToApi(product_id):
    """Elimina un producto

        Elimina un producto de la base de datos de feria virtual.
        parámetros:
            - product_id: corresponde al identificador del producto a eliminar.
        retorna:
            - True: Si el producto se elimino correctamente.
            - False: En caso de problemas o errores.
    """
    response = requests.delete(
        url=settings.PRODUCTOR_SERVICE_URL_DELETE,
        params={'productId': product_id})
    return True if response.status_code == 200 else False


def GetFromApi(user):
    """ Carga la lista de productos

        Carga los productos almacenados en la base de datos de feria virtual
        parámetros:
            - user: objeto que contien la información del usuario actual.
        retorna:
            - True: Si cargo los datos
            - False: En caso de problemas de conectividad.
    """
    response = requests.get(
        url=settings.PRODUCTOR_SERVICE_URL_GET_ALL,
        params={'clientId': user.loginsession.ClientId})
    if response.status_code != 200:
        return False
    serializador = ProductoSerializer(data=response.json(), many=True)
    serializador.is_valid()
    serializador.save(User=user)
    return True
