import json
import requests
from django.conf import settings
from .serializers import VehiculoApiSerializer, VehiculoSerializer, AuctionSerializer, DispatchSerializer


def PostToApi(serializador):
    """ Almacena un nuevo vehiculo.

        Permite almacenar los datos del nuevo vehiculo en la base de datos de feria virtual.
        parámetros:
            - serializador: objeto serializer que contiene la información del vehiculo.
        retorna:
            - True: El vehiculo fue almacenado correctamente
            - False: Ocurrio algun problema y el vehiculo no fue almacenado
    """
    data = VehiculoApiSerializer(data=serializador.data)
    data.is_valid()
    data.is_valid()
    response = requests.post(
        url=settings.TRANSPORTISTA_SERVICE_URL_POST,
        headers=settings.SERVER_HEADERS,
        data=json.dumps(data.data))
    return True if response.status_code == 200 else False


def PutToApi(serializador):
    """ Actualiza un vehiculo.

        Permite actualizar los datos del vehiculo en la base de datos de feria virtual.
        parámetros:
            - serializador: objeto serializer que contiene la información del vehiculo.
        retorna:
            - True: El vehiculo fue almacenado correctamente
            - False: Ocurrio algun problema y el vehiculo no fue almacenado
    """
    data = VehiculoApiSerializer(data=serializador.data)
    data.is_valid()
    response = requests.put(
        url=settings.TRANSPORTISTA_SERVICE_URL_PUT,
        headers=settings.SERVER_HEADERS,
        data=json.dumps(data.data))
    return True if response.status_code == 200 else False


def DeleteToApi(vehicle_id):
    """Elimina un vehiculo

        Elimina un vehiculo de la base de datos de feria virtual.
        parámetros:
            - vehicle_id: corresponde al identificador del vehiculo a eliminar.
        retorna:
            - True: Si el vehiculo se elimino correctamente.
            - False: En caso de problemas o errores.
    """
    response = requests.delete(
        url=settings.TRANSPORTISTA_SERVICE_URL_DELETE,
        params={'vehicleId': vehicle_id})
    return True if response.status_code == 200 else False


def GetFromApi(user):
    """ Carga la lista de vehiculos

        Carga los vehiculos almacenados en la base de datos de feria virtual
        parámetros:
            - user: objeto que contiene la información del usuario actual.
        retorna:
            - True: Si cargo los datos
            - False: En caso de problemas de conectividad. 
    """
    response = requests.get(
        url=settings.TRANSPORTISTA_SERVICE_URL_GET_ALL,
        params={'clientId': user.loginsession.ClientId})
    if response.status_code != 200:
        return False
    serializador = VehiculoSerializer(data=response.json(), many=True)
    serializador.is_valid()
    serializador.save(User=user)
    return True

def GetAuctionsFromApi(user):
    """ Carga la lista de subastas

        Carga los subastas almacenados en la base de datos de feria virtual
        parámetros:
            - user: objeto que contiene la información del usuario actual.
        retorna:
            - True: Si cargo los datos
            - False: En caso de problemas de conectividad. 
    """
    response = requests.get(
        url=settings.AUCTION_SERVICE_URL_GET_ALL,
        params={'clientId': user.loginsession.ClientId})
    print()
    print(response.json())
    print()    
    if response.status_code != 200:
        return False     
    serializador = AuctionSerializer(data=response.json(), many=True)
    serializador.is_valid()
    print("Error serializador")
    print(serializador.errors)
    serializador.save(User=user)
    return True


def PostBidValueToApi(serializador):
    """ Almacena una nueva puja.

        Permite almacenar el valor de la puja en la base de datos de feria virtual.
        parámetros:
            - serializador: objeto serializer que contiene el valor de la puja.
        retorna:
            - True: El valor de puja fue almacenado correctamente
            - False: Ocurrio algun problema y la puja no fue almacenada
    """
    response = requests.post(
        url=settings.AUCTION_SERVICE_URL_BIDVALUE_POST,
        headers=settings.SERVER_HEADERS,
        data=json.dumps(serializador.data))
    return True if response.status_code == 200 else False 


def GetDispatchesFromApi(user):
    """ Carga la lista de despachos

        Carga los despachos almacenados en la base de datos de feria virtual
        parámetros:
            - user: objeto que contiene la información del usuario actual.
        retorna:
            - True: Si cargo los datos
            - False: En caso de problemas de conectividad. 
    """
    response = requests.get(
        url=settings.DISPATCH_SERVICE_URL_GET,
        params={'clientId': user.loginsession.ClientId})
    print("RESPONSE")
    print(response.json())
    print()         
    if response.status_code != 200:
        return False     
    serializador = DispatchSerializer(data=response.json(), many=True)
    serializador.is_valid()
    serializador.save(User=user)
    return True


def DispatchDeliverToApi(serializador):
    """ Finaliza el despacho

        Finaliza un despacho por parte del transportista,
        permitiendo ingresar una observación al despacho.

        parametros:
            - serializador: objeto serializer que contiene los datos de aceptación.
        retorna:
            - True, en caso de realizar la aceptación correctamente.
            - false, en caso de problemas de envío o conectividad.
    """
    response = requests.patch(
        url=settings.DISPATCH_SERVICE_URL_PATCCH_DELIVER,
        headers=settings.SERVER_HEADERS,
        data=json.dumps(serializador.data))
    return True if response.status_code == 200 else False


def DispatchCancelToApi(serializador):
    """ Cancela el despacho

        Rechaza un despacho por parte del transportista,
        permitiendo ingresar una observación al despacho.

        parametros:
            - serializador: objeto serializer que contiene los datos de cancelación.
        retorna:
            - True, en caso de realizar el rechazo correctamente.
            - false, en caso de problemas de envío o conectividad.
    """
    response = requests.patch(
        url=settings.DISPATCH_SERVICE_URL_PATCCH_CANCEL,
        headers=settings.SERVER_HEADERS,
        data=json.dumps(serializador.data))
    return True if response.status_code == 200 else False
