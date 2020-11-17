from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.views.generic.base import TemplateView
from .forms import LoginForm
from .services import EncriptPassword, RedireccionarInicio


def iniciarSesion(request):
    form = LoginForm(request.POST or None)
    template = loader.get_template("login/login.html")
    context = {'form': form, 'usuario': request.user, }
    if form.is_valid():
        data = form.cleaned_data
        user = authenticate(
            username=data.get("username"), password=EncriptPassword(data.get("password")))
        if user is not None:
            login(request, user)
            return redirect(RedireccionarInicio(user))
        else:
            return redirect('accessdenied')
    return HttpResponse(template.render(context, request))


@login_required(login_url='login')
def cerrarSesion(request):
    "Cerrar la sesion del usuario."
    logout(request)
    return redirect('/')


class Denied(TemplateView):
    "Vista que indica el acceso no permitido."
    template_name = 'login/accessdenied.html'


class Restricted(TemplateView):
    "Vista que muestra página de acceso restringido."
    template_name = 'login/restrictedaccess.html'


class ErrorLoginService(TemplateView):
    "Vista que muestra página en caso que el servicio de login no este disponible."
    template_name = 'login/loginservicenotavailable'
