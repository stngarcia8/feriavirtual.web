import json
import requests
from django.conf import settings
from transportista.models import Vehicle, VehicleType
from transportista.serializers import TransportSaveSerializer


def GrabarTransporte(user, serializador):
    resultado = False
    jsonData = CrearTransporte(serializador, user, '')
    print(" AQUI ")
    print(jsonData)
    print(" AQUI ")
    url = settings.TRANSPORTISTA_SERVICE_URL_POST
    headers = {'content-type': 'application/json'}
    response = requests.post(url, headers=headers, data=jsonData)
    print()
    print(url)
    print()
    if response.status_code == 200:
        GrabarTransporteEnTemporal(serializador, user, '')
        resultado = True
    return resultado

def CrearTransporte(serializador, user, vehicleID):
    data = {}
    data['VehicleID'] = vehicleID
    data['ClientID'] = user.loginsession.ClientID
    data['VehicleType'] = {}
    data['VehicleType'] = ObtenerTipo(serializador.data.get('VehicleType'))
    data['VehiclePatent'] = serializador.data.get('VehiclePatent')
    data['VehicleModel'] = serializador.data.get('VehicleModel')
    data['VehicleCapacity'] = serializador.data.get('VehicleCapacity')
    data['VehicleAvailable'] = 1 if serializador.data.get('VehicleAvailable') else 0
    return json.dumps(data)

def ObtenerTipo(objeto):
    tipoDict = {}
    tipoDict['VehicleTypeID'] = objeto.VehicleTypeID
    tipoDict['VehicleTypeDescription'] = objeto.VehicleTypeDescription
    return tipoDict

def CargarTransporte(user):
    url = settings.TRANSPORTISTA_SERVICE_URL_GET
    args = {'clientID': user.loginsession.ClientID}
    response = requests.get(url, params=args)
    if response.status_code != 200:
        return
    for data in response.json():
        transporte = Vehicle.objects.create(
            VehicleID=data.get('VehicleID'), ClientID=data.get('ClientID'),
            VehiclePatent=data.get('VehiclePatent'),
            VehicleModel=data.get('VehicleModel'),
            VehicleCapacity=data.get('VehicleCapacity'),
            VehicleAvailable=data.get('VehicleAvailable'))
        transporte.save()
        vehicletype = VehicleType.objects.get(VehicleTypeID=data['VehicleType']['VehicleTypeID'])
        transporte.VehicleType = vehicletype
        transporte.User = user
        transporte.save()
    return
    
 
def GrabarTransporteEnTemporal(serializador, user, vehicleID):
    data = Vehicle.objects.create(
        VehicleID=vehicleID, ClientID=user.loginsession.ClientID,
        VehicleType=serializador.data.get('VehicleType'),
        VehiclePatent=serializador.data.get('VehiclePatent'),
        VehicleModel=serializador.data.get('VehicleModel'),
        VehicleCapacity=serializador.data.get('VehicleCapacity'),
        VehicleAvailable=serializador.data.get('VehicleAvailable'),
        User_id=user.id)
    data.save()
    return

def ActualizarTransporte(user, serializador, vehicleID):
    resultado = False
    jsonData = CrearTransporte(serializador, user, vehicleID)
    url = settings.TRANSPORTISTA_SERVICE_URL_PUT
    headers = {'content-type': 'application/json'}
    response = requests.put(url, headers=headers, data=jsonData)
    if response.status_code == 200:
        resultado = True
    return resultado


def EliminarTransporte(vehicleID):
    url = settings.TRANSPORTISTA_SERVICE_URL_DELETE
    args = {'vehicleID': vehicleID}
    response = requests.delete(url, params=args)
    print("   ")
    print(response)
    print("   ")
    return True if response.status_code == 200 else False    
