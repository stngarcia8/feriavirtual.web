import hashlib
import requests
from django.conf import settings
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from login.models import LoginSession


def CargarLogin(username, password):
    json = None
    url = settings.LOGIN_SERVICE_URL
    url = 'http://maipogrande-fv.duckdns.org:8080/api/v1/login/autenticate'
    payload = {'username': username, 'password': EncriptPassword(password)}
    headers = {"content-type": "application/json; charset=utf-8", }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        json = response.json()
    return (json)


def EncriptPassword(password):
    "Encripta una constraseña con shas1."
    return hashlib.sha1(str.encode(password)).hexdigest().strip()


def CrearUsuario(request, loginSerializer, password):
    "Crea un usuario en la base de datos temporal."
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


def EliminarUsuario(userName):
    "elimina un usuario de la base de datos temporal."
    try:
        u = User.objects.get(username=userName)
        u.delete()
        return
    except Exception:
        return


def CrearSesion(serializador, user):
    "Crea una sesion de usuario en el sistema."
    sesion = LoginSession()
    sesion.UserId = serializador.data.get('UserId')
    sesion.ClientId = serializador.data.get('ClientId')
    sesion.Username = serializador.data.get('Username')
    sesion.FullName = serializador.data.get('FullName')
    sesion.Email = serializador.data.get('Email')
    sesion.ProfileId = serializador.data.get('ProfileId')
    sesion.ProfileName = serializador.data.get('ProfileName')
    sesion.User = user
    sesion.save()
    return


def RedireccionarInicio(user):
    "redirecciona a los usuarios a sus páginas de inicio según su perfil."
    pagina = 'home'
    if user.loginsession.ProfileId == 3:
        pagina = 'homeExterno'
    if user.loginsession.ProfileId == 4:
        pagina = 'homeInterno'
    if user.loginsession.ProfileId == 5:
        pagina = 'homeProducer'
    if user.loginsession.ProfileId == 6:
        pagina = 'homeCarrier'
    return pagina
