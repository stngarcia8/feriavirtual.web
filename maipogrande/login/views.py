from django.views.generic.base import TemplateView
import json
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from .utils import functions
from .serializers import LoginSerializer


# Login:
# Vista para el inicio de sesion
def iniciarSesion(request):
    form = LoginForm(request.POST or None)
    template = loader.get_template("login/login.html")
    context = {'form': form, 'usuario': request.user, }
    if form.is_valid():
        data = form.cleaned_data
        json = functions.CargarLogin(
            data.get("username"), data.get("password"))
        if json is not None:
            serializador = LoginSerializer(data=json)
            serializador.is_valid()
            if serializador.data.get('ProfileID') < 3:
                return redirect('restrictedaccess')
            user = functions.CrearUsuario(
                request, serializador, data.get("password"))
            if user is not None:
                login(request, user)
                functions.CrearSesion(serializador, user)
                return redirect(functions.RedireccionarInicio(user))
        else:
            return redirect('accessdenied')
    return HttpResponse(template.render(context, request))


# Logout:
# Vista para finalizar la sesion del usuario.
@login_required(login_url='iniciarSesion')
def cerrarSesion(request):
    username = request.user.username
    logout(request)
    functions.EliminarUsuario(username)
    return redirect('/')


# Denegar:
# Muestra la vista para denegar el acceso a los usuarios sin permisos de login
class Denied(TemplateView):
    template_name = 'login/accessdenied.html'


# Restringir:
# Muestra la vista para los usuarios que intentan acceder por url a los servicios.
class Restricted(TemplateView):
    template_name = 'login/restrictedaccess.html'


# ErrorLoginService:
# Muestra la vista cuando la api de login no este disponible.
class ErrorLoginService(TemplateView):
    template_name = 'login/loginservicenotavailable'
