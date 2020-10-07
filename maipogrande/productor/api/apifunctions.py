import json
import requests
from django.conf import settings
from productor.models import Producto


def GrabarProducto(user, serializador):
    resultado = False
    jsonData = CrearProducto(serializador, user, '')
    url = settings.PRODUCTOR_SERVICE_URL_POST
    headers = {'content-type': 'application/json'}
    response = requests.post(url, headers=headers, data=jsonData)
    if response.status_code == 200:
        GrabarProductoEnTemporal(serializador, user, '')
        resultado = True
    return resultado


def CrearProducto(serializador, user, productID):
    data = {}
    data['ProductID'] = productID
    data['ClientID'] = user.loginsession.ClientID
    data['ProductName'] = serializador.data.get('ProductName')
    data['Observation'] = serializador.data.get('Observation')
    data['ProductValue'] = serializador.data.get('ProductValue')
    data['ProductQuantity'] = serializador.data.get('ProductQuantity')
    return json.dumps(data)


def GrabarProductoEnTemporal(serializador, user, productID):
    data = Producto.objects.create(
        ProductID=productID, ClientID=user.loginsession.ClientID,
        ProductName=serializador.data.get('ProductName'),
        Observation=serializador.data.get('Observation'),
        ProductValue=serializador.data.get('ProductValue'),
        ProductQuantity=serializador.data.get('ProductQuantity'),
        User_id=user.id)
    data.save()
    return


def CargarProductos(user):
    url = settings.PRODUCTOR_SERVICE_URL_GET
    args = {'clientID': user.loginsession.ClientID}
    response = requests.get(url, params=args)
    if response.status_code != 200:
        return
    for data in response.json():
        producto = Producto.objects.create(
            ProductID=data.get('ProductID'), ClientID=data.get('ClientID'),
            ProductName=data.get('ProductName'), Observation=data.get('Observation'),
            ProductValue=data.get('ProductValue'),
            ProductQuantity=data.get('ProductQuantity'), User=user)
        producto.save()
    return
