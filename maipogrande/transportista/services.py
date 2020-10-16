import json
import requests
from django.conf import settings
from .serializers import VehiculoApiSerializer, VehiculoSerializer


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
        params={'vehicleID': vehicle_id})
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
        params={'clientID': user.loginsession.ClientID})
    if response.status_code != 200:
        return False
    serializador = VehiculoSerializer(data=response.json(), many=True)
    serializador.is_valid()
    serializador.save(User=user)
    return True
