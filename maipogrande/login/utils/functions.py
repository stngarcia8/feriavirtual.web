import requests
import hashlib
from django.contrib.auth import authenticate, logout
from django.conf import settings
from django.contrib.auth.models import User
from login.models import LoginSession

# CargarLogin(username, password)
# Parametros:
#   username: Nombre de usuario a verificar
#   password: Contraseña del usuario a verificar.
# Retorna:
#   resultado: true si la peticion es correcta, false en caso de error o falla fe validacion
#   json: resultado obtenido de la peticion, None en caso de problema.


def CargarLogin(username, password):
    json = None
    url = settings.LOGIN_SERVICE_URL
    url = 'http://maipogrande-fv.duckdns.org:8080/api/v1/login/autenticate'
    payload = {'username': username, 'password': EncriptPassword(password)}
    headers = {"content-type": "application/json; charset=utf-8", }
    response = requests.post(url, json=payload, headers=headers)
    print()
    print(url)
    print(response)
    print()
    if response.status_code == 200:
        json = response.json()
    return (json)


# EncriptarPassword(password):
# Encripta una contraseña ingresada para el inicio de sesion.
# parametros:
#   password: contraseña a encriptar.
# retorna:
#   encriptedPassword: contraseña encriptada con shas1
def EncriptPassword(password):
    return hashlib.sha1(str.encode(password)).hexdigest().strip()


# CrearUsuario(request, loginSerializer, password)
# Crea un usuario en el sistema para su autentificacion.
# parametros:
#   request: objeto request de la sesion en ejecucion.
#   json: json que contiene los datos cargados desde la api
# password: contraseña de usuario que se logea en el sistema, esta clave no esta encriptada ya que sera encriptada al grabar el usuario.
# retorna:
#   user: Objeto de tipo User con el usuario creado.
def CrearUsuario(request, loginSerializer, password):
    logout(request)
    EliminarUsuario(loginSerializer.data.get('Username'))
    user = User.objects.create_user(
        username=loginSerializer.data.get('Username'),
        password=password,
        first_name=loginSerializer.data.get('FullName'),
        email=loginSerializer.data.get('Email'))
    user.is_staff = True
    user.is_active = True
    user.save()
    return authenticate(username=user.username, password=password)


# EliminarUsuario(userName)
# Elimina un usuario de la base de datos del sistema.
# parametros:
#   username: nombre de usuario que sera eliminado.
def EliminarUsuario(userName):
    try:
        u = User.objects.get(username=userName)
        u.delete()
        return
    except Exception:
        return


# CrearSesion(serializador, user)
# Crea la sesion de usuario
# parametros:
#   serializador: serializer que contiene los datos cargados desde la api
#   user: objeto user que contiene los datos del usuario autentificado en el sistema local
def CrearSesion(serializador, user):
    sesion = LoginSession()
    sesion.UserId = serializador.data.get('UserId')
    sesion.ClientID = serializador.data.get('ClientID')
    sesion.Username = serializador.data.get('Username')
    sesion.FullName = serializador.data.get('FullName')
    sesion.Email = serializador.data.get('Email')
    sesion.ProfileID = serializador.data.get('ProfileID')
    sesion.ProfileName = serializador.data.get('ProfileName')
    sesion.User = user
    sesion.save()
    return


# RedireccionarInicio(user):
# Redirecciona a los diferentes inicios de sesion segun el tipo de usuario.
# parametros:
#   user: objeto de usuario que contiene la informacion de inicio de sesion
# retorna:
#   pagina: corresponde a la vista que sera redirigido el usuario segun su perfil.
def RedireccionarInicio(user):
    pagina = 'home'
    if user.loginsession.ProfileID == 3:
        pagina = 'homeExternalCustomer'
    if user.loginsession.ProfileID == 4:
        pagina = 'homeInternalCustomer'
    if user.loginsession.ProfileID == 5:
        pagina = 'homeProducer'
    if user.loginsession.ProfileID == 6:
        pagina = 'homeCarrier'
    return pagina
