import json
import requests
from django.conf import settings
from .models import TransportInfo


def GrabarTransporte(user, serializador):
    resultado = False
    jsonData = CrearTransporte(serializador, user, '')
    url = settings.TRANSPORTISTA_SERVICE_URL_POST
    headers = {'content-type': 'application/json'}
    response = requests.post(url, headers=headers, data=jsonData)
    if response.status_code == 200:
        GrabarTransporteEnTemporal(serializador, user, '')
        resultado = True
    return resultado


def CrearTransporte(serializador, user, VehicleID):
    data = {}
    data['VehicleID'] = vehicleID
    data['ClientID'] = user.loginsession.ClientID
    # data['VehicleType'] = serializador.data.get('VehicleType')
    data['VehiclePatent'] = serializador.data.get('VehiclePatent')
    data['VehicleModel'] = serializador.data.get('VehicleModel')
    data['VehicleCapacity'] = serializador.data.get('VehicleCapacity')
    data['VehicleAvailable'] = serializador.data.get('VehicleAvailable')
    return json.dumps(data)


def GrabarTransporteEnTemporal(serializador, user, productID):
    data = TransportInfo.objects.create(
        VehicleID=vehicleID, ClientID=user.loginsession.ClientID,
        VehicleType=serializador.data.get('VehicleType'),
        VehiclePatent=serializador.data.get('VehiclePatent'),
        VehicleModel=serializador.data.get('VehicleModel'),
        VehicleCapacity=serializador.data.get('VehicleCapacity'),
        VehicleAvailable=serializador.data.get('VehicleAvailable'),
        User_id=user.id)
    data.save()
    return


def CargarTransporte(user):
    url = settings.TRANSPORTISTA_SERVICE_URL_GET
    args = {'clientID': user.loginsession.ClientID}
    response = requests.get(url, params=args)
    if response.status_code != 200:
        return
    for data in response.json():
        transporte = TransportInfo.objects.create(
            VehicleID=data.get('VehicleID'), ClientID=data.get('ClientID'),
            VehicleType=data.get('VehicleType'), VehiclePatent=data.get('VehiclePatent'),
            VehicleModel=data.get('VehicleModel'),
            VehicleCapacity=data.get('VehicleCapacity'),
            VehicleAvailable=data.get('VehicleAvailable'), User=user)
        transporte.save()
    return
