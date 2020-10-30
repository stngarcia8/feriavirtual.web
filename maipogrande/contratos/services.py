import requests
import json
from django.conf import settings
from .serializers import ContratoSerializer


def GetFromApi(user):
    """ Carga la lista de contratos

        Carga los contratos almacenados en la base de datos de feria virtual
        parámetros:
            - user: objeto que contiene la información del usuario actual.
        retorna:
            - True: Si cargo los datos
            - False: En caso de problemas de conectividad.
    """
    response = requests.get(
        url=settings.CONTRATO_SERVICE_URL_GET,
        params={'profileID': user.loginsession.ProfileID, 'clientID': user.loginsession.ClientID})
    if response.status_code != 200:
        return False    
    serializador = ContratoSerializer(data=response.json(), many=True)
    serializador.is_valid()
    serializador.save(User=user, ProfileID=user.loginsession.ProfileID)
    print()
    print(serializador.data)
    print()
    return True


def PatchAcceptToApi(serializador):
    """ Acepta el contrato

        Acepta un contrato por parte del productor/transportista,
        permitiendo ingresar una observación a el contrato.

        parametros:
            - serializador: objeto serializer que contiene los datos de aceptación.
        retorna:
            - True, en caso de realizar la aceptación correctamente.
            - false, en caso de problemas de envío o conectividad.
    """
    response = requests.patch(
        url=settings.CONTRATO_SERVICE_URL_PATCCH_ACCEPT,
        headers=settings.SERVER_HEADERS,
        data=json.dumps(serializador.data))
    return True if response.status_code == 200 else False


def PatchRefuseToApi(serializador):
    """ Rechaza el contrato

        Rechaza un contrato por parte del productor/transportista,
        permitiendo ingresar una observación al contrato.

        parametros:
            - serializador: objeto serializer que contiene los datos de rechazo.
        retorna:
            - True, en caso de realizar el rechazo correctamente.
            - false, en caso de problemas de envío o conectividad.
    """
    response = requests.patch(
        url=settings.CONTRATO_SERVICE_URL_PATCCH_REFUSE,
        headers=settings.SERVER_HEADERS,
        data=json.dumps(serializador.data))
    return True if response.status_code == 200 else False
