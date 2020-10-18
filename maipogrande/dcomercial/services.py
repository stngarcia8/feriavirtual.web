import json
import requests
from django.conf import settings
from .serializers import ComercialApiSerializer, ComercialSerializer

def PostToApi(serializador):
    """ Almacena un nuevo dato comercial.

        Permite almacenar los datos comerciales en la base de datos de feria virtual.
        parámetros:
            - serializador: objeto serializer que contiene la información del dato comercial.
        retorna:
            - True: El dato comercial fue almacenado correctamente
            - False: Ocurrio algun problema y el dato comercial no fue almacenado
    """
    data = ComercialApiSerializer(data=serializador.data)
    data.is_valid()
    data.is_valid()
    response = requests.post(
        url=settings.COMERCIAL_SERVICE_URL_POST,
        headers=settings.SERVER_HEADERS,
        data=json.dumps(data.data))
    print()
    print(response)
    print(json.dumps(data.data))
    print()
    return True if response.status_code == 200 else False


def PutToApi(serializador):
    """ Actualiza un dato comercial.

        Permite actualizar los datos comerciales en la base de datos de feria virtual.
        parámetros:
            - serializador: objeto serializer que contiene la información del dato comercial.
        retorna:
            - True: El dato comercial fue almacenado correctamente
            - False: Ocurrio algun problema y el dato comercial no fue almacenado
    """
    data = ComercialApiSerializer(data=serializador.data)
    data.is_valid()
    response = requests.put(
        url=settings.COMERCIAL_SERVICE_URL_PUT,
        headers=settings.SERVER_HEADERS,
        data=json.dumps(data.data))
    return True if response.status_code == 200 else False

def DeleteToApi(comercial_id):
    """Elimina un dato comercial

        Elimina un dato comercial de la base de datos de feria virtual.
        parámetros:
            - client_id: corresponde al identificador del cliente.
        retorna:
            - True: Si el dato comercial se elimino correctamente.
            - False: En caso de problemas o errores.
    """
    response = requests.delete(
        url=settings.COMERCIAL_SERVICE_URL_DELETE,
        params={'comercialID': comercial_id})
    return True if response.status_code == 200 else False


def GetFromApi(user):
    """ Carga los datos comerciales

        Carga los datos comerciales almacenados en la base de datos de feria virtual
        parámetros:
            - user: objeto que contiene la información del usuario actual.
        retorna:
            - True: Si cargo los datos
            - False: En caso de problemas de conectividad. 
    """
    response = requests.get(
        url=settings.COMERCIAL_SERVICE_URL_GET,
        params={'clientID': user.loginsession.ClientID})
    if response.status_code != 200:
        return False  
    serializador = ComercialSerializer(data=response.json(), many=False)
    serializador.is_valid()
    serializador.save(User=user)
    return True        