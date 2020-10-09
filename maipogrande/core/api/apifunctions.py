import json
import requests
from django.conf import settings
from core.models import ComercialInfo, City, Country
from core.serializers import ComercialSaveSerializer


# GrabarDatoComercial(user, serializador):
# Crea un dato comercial en la base de datos de feria virtual
# parametros:
#   user: usuario que esta grabando la informacion.
#   serializador: diccionario que contiene los datos ingresados por el usuario
# retorna:
#   resultado: True si el almacenamiento fue correcto, False en caso contrario o por problemas ajenos a el programa.
def GrabarDatoComercial(user, serializador):
    resultado = False
    jsonData = CrearDatoComercial(serializador, user, '')
    print(" AQUI ")
    print(jsonData)
    print(" AQUI ")
    url = settings.COMERCIAL_SERVICE_URL_POST
    headers = {'content-type': 'application/json'}
    response = requests.post(url, headers=headers, data=jsonData)
    if response.status_code == 200:
        resultado = True
    return resultado


# CrearDatoComercial(serializador, user, comercialID):
# Crea el modelo de dato comercial para enviarlo por api a la base de datos.
# parametros:
#   serializador: objeto que contiene los datos ingresados por el usuario.
#   user: objeto que contiene los datos del usuario que inicio sesion en el sistema
#   comercialID: identificador del dato comercial, si es nuevo este va vacio.
# retorna:
#   json: objeto que contiene la informacion a enviar en formato json
def CrearDatoComercial(serializador, user, comercialID):
    data = {}
    data['ComercialID'] = comercialID
    data['ClientID'] = user.loginsession.ClientID
    data['CompanyName'] = serializador.data.get('CompanyName')
    data['FantasyName'] = serializador.data.get('FantasyName')
    data['ComercialBusiness'] = serializador.data.get('ComercialBusiness')
    data['Email'] = serializador.data.get('Email')
    data['ComercialDNI'] = serializador.data.get('ComercialDNI')
    data['Address'] = serializador.data.get('Address')
    data['City'] = {}
    data['Country'] = {}
    data['City'] = ObtenerCiudad(serializador.data.get('City'))
    data['Country'] = ObtenerPais(serializador.data.get('Country'))
    data['PhoneNumber'] = serializador.data.get('PhoneNumber')
    return json.dumps(data)


# ObtenerCiudad(objeto):
# Genera el objeto ciudad para serializarlos en el json de resultados
# parametros:
#   objeto:representa un objeto ciudad que debe ser traspasado a diccionario para su serializacion
# retorna:
#   cityDict: Diccionario con los datos de la ciudad serializada
def ObtenerCiudad(objeto):
    cityDict = {}
    cityDict['CityID'] = objeto.CityID
    cityDict['CityName'] = objeto.CityName
    return cityDict


# ObtenerPais(objeto):
# Genera el objeto pais para serializarlos en el json de resultados
# parametros:
#   objeto:representa un objeto pais que debe ser traspasado a diccionario para su serializacion
# retorna:
#   countryDict: Diccionario con los datos dedel pais serializada
def ObtenerPais(objeto):
    countryDict = {}
    countryDict['CountryID'] = objeto.CountryID
    countryDict['CountryName'] = objeto.CountryName
    countryDict['CountryPrefix'] = objeto.CountryPrefix
    return countryDict


# CargarDatosComerciales(user):
# Carga los datos comerciales del usuario y estos se almacenan temporalmente en la bdd
# parametros:
#   user: objeto que contiene los datos del usuario que inicio la sesion
# retorna:
#   querySet: Retorna el objeto encontrado o cargado desde la api, retorna None
#               si no encuentra informacion.
def CargarDatosComerciales(user):
    url = settings.COMERCIAL_SERVICE_URL_GET
    args = {'clientID': user.loginsession.ClientID}
    response = requests.get(url, params=args)
    if response.status_code != 200:
        return None
    data = response.json()
    if not data.get('ClientID'):
        return None
    serializador = ComercialSaveSerializer(data=data)
    serializador.is_valid()
    serializador.save()
    city = City.objects.get(CityID=data['City']['CityID'])
    country = Country.objects.get(CountryID=data['Country']['CountryID'])
    comercial = ComercialInfo.objects.get(ClientID=user.loginsession.ClientID)
    comercial.City = city
    comercial.Country = country
    comercial.User = user
    comercial.save()
    return comercial


# ActualizarDatoComercial(user, serializador, comercialID):
# Actualiza los datos comerciales de un cliente en la base de feria virtual
# parametros:
#   user: usuario que esta grabando la informacion.
#   serializador: diccionario que contiene los datos ingresados por el usuario
#   comercialID: identificador del item que se esta modificando
# retorna:
#   resultado: True si el almacenamiento fue correcto, False en caso contrario o por problemas ajenos a el programa.
def ActualizarDatoComercial(user, serializador, comercialID):
    resultado = False
    jsonData = CrearDatoComercial(serializador, user, comercialID)
    url = settings.COMERCIAL_SERVICE_URL_PUT
    headers = {'content-type': 'application/json'}
    response = requests.put(url, headers=headers, data=jsonData)
    if response.status_code == 200:
        resultado = True
    return resultado


# EliminarDatosComerciales(user):
# Elimina los datos comerciales por medio de la api
# parametros:
#   comercialID: identificador del dato comercial a eliminar
# retorna:
#   resultado: True si elimino bien y False en cualquier otro caso
def EliminarDatosComerciales(comercialID):
    url = settings.COMERCIAL_SERVICE_URL_DELETE
    args = {'comercialID': comercialID}
    response = requests.delete(url, params=args)
    return True if response.status_code == 200 else False


# Imprimir(algo)
# imprime algo en consola para verificar su estado, esto sale luego
def imprimir(algo):
    print()
    print("Ocurrio algo que se debe mirar!")
    print(algo)
    print()
    return
