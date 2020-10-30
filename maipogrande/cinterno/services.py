import json
import requests
from django.conf import settings
from .serializers import ExportInternalProductSerializer


def GetExportInternalProductFromApi(user):
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
    serializador = ExportInternalProductSerializer(data=response.json(), many=True)
    serializador.is_valid()
    serializador.save(User=user)
    return True