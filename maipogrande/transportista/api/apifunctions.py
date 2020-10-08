import json
import requests
from django.conf import settings
from transportista.models import Vehicle, VehicleType
from transportista.serializers import TransportSaveSerializer


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

# def CrearTransporte(serializador, user, VehicleID):
#     data = {}
#     data['ComercialID'] = comercialID
#     data['ClientID'] = user.loginsession.ClientID
#     data['CompanyName'] = serializador.data.get('CompanyName')
#     data['FantasyName'] = serializador.data.get('FantasyName')
#     data['ComercialBusiness'] = serializador.data.get('ComercialBusiness')
#     data['Email'] = serializador.data.get('Email')
#     data['ComercialDNI'] = serializador.data.get('ComercialDNI')
#     data['Address'] = serializador.data.get('Address')
#     data['City'] = {}
#     data['Country'] = {}
#     data['City'] = ObtenerCiudad(serializador.data.get('City'))
#     data['Country'] = ObtenerPais(serializador.data.get('Country'))
#     data['PhoneNumber'] = serializador.data.get('PhoneNumber')
#     return json.dumps(data)

def ObtenerTipo(objeto):
    vehicleType = {}
    vehicleType['VehicleTypeID'] = objeto.VehicleTypeID
    vehicleType['VehicleTypeDescription'] = objeto.VehicleTypeDescription
    return vehicleType

# def CargarTransporte(user):
#     url = settings.TRANSPORTISTA_SERVICE_URL_GET
#     args = {'clientID': user.loginsession.ClientID}
#     response = requests.get(url, params=args)
#     if response.status_code != 200:
#         return
#     for data in response.json():
#         transporte = Vehicle.objects.create(
#             VehicleID=data.get('VehicleID'), ClientID=data.get('ClientID'),
#             VehicleType=data.get('VehicleType'), VehiclePatent=data.get('VehiclePatent'),
#             VehicleModel=data.get('VehicleModel'),
#             VehicleCapacity=data.get('VehicleCapacity'),
#             VehicleAvailable=data.get('VehicleAvailable'), User=user)
#         transporte.save()
#     return

def CargarTransporte(user):
    url = settings.TRANSPORTISTA_SERVICE_URL_GET
    args = {'clientID': user.loginsession.ClientID}
    response = requests.get(url, params=args)
    if response.status_code != 200:
        return None
    data = response.json()
    if not data.get('ClientID'):
        return None
    serializador = TransportSaveSerializer(data=data)
    serializador.is_valid()
    serializador.save()
    vehicleType = VehicleType.objects.get(VehicleTypeID=data['VehicleType']['VehicleTypeID'])
    transporte = Vehicle.objects.get(ClientID=user.loginsession.ClientID)
    transporte.VehicleType = vehicleType
    transporte.User = user
    transporte.save()
    return transporte    


def GrabarTransporteEnTemporal(serializador, user, productID):
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