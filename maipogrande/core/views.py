import requests
import json
from django.conf import settings
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.views.defaults import page_not_found
from django.urls import reverse
from django.core.mail import EmailMessage
from .forms import ContactForm


class Home(TemplateView):
    "Muestra la página de inicio de feria virtual."
    template_name = 'core/home.html'


class About(TemplateView):
    "Muestra la página acerca de feria virtual."
    template_name = 'core/about.html'


def Error_404(request, exception):
    "Muestra página de error 404."
    return page_not_found(request, template_name='core/404.html', status=404)


def Contact(request):
    "Muestra página de contacto de feria virtual."
    contact_form = ContactForm()
    if request.method == "POST":
        contact_form = ContactForm(data=request.POST)
        if contact_form.is_valid():
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY, 'response': recaptcha_response}
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            if result['success']:
                name = request.POST.get('name', '')
                email = request.POST.get('email', '')
                content = request.POST.get('content', '')
                email = EmailMessage(
                    "Feria Virtual: Nueva solicitud de registro.",
                    "De {} <{}>\n\nEscribió:\n\n{}".format(name, email, content),
                    "no-contestar@inbox.mailtrap.io",
                    ["maipogrande-fv@gmail.com"],
                    reply_to=[email]
                )
                try:
                    email.send()
                    return redirect(reverse('emailOk'))
                except Exception:
                    return redirect(reverse('emailFail'))
            else:
                messages.error(request, 'Verificación inválida, por favor intentelo nuevamente.')
    return render(request, "core/contact.html", {'form': contact_form})


class EmailOk(TemplateView):
    "Muestra la página de correo enviado correctamente."
    template_name = 'core/emailsent.html'


class EmailFail(TemplateView):
    "Muestra la página de correo fallido."
    template_name = 'core/failedemail.html'


class ServiceNotAvailable(TemplateView):
    "Muestra la página servicio no disponible de feria virtual."
    template_name = 'core/servicenotavailable.html'


@login_required(login_url='login')
def DinamicHome(request):
    "Redirecciona a las páginas de inicio según el perfil del usuario."
    pagina = "core/home.html"
    if request.user.loginsession.ProfileId == 3:
        pagina = "cexterno/home-externo.html"
    if request.user.loginsession.ProfileId == 4:
        pagina = "cinterno/home-interno.html"
    if request.user.loginsession.ProfileId == 5:
        pagina = "productor/home-productor.html"
    if request.user.loginsession.ProfileId == 6:
        pagina = "transportista/home-transportista.html"
    miPlantilla = loader.get_template(pagina)
    return HttpResponse(miPlantilla.render({}, request))


def DinamicHomePage(request):
    "Retorna la ppágina de inicio de los usuarios según su perfil."
    pagina = "core/home.html"
    if request.user.loginsession.ProfileId == 3:
        pagina = "cexterno/home-externo.html"
    if request.user.loginsession.ProfileId == 4:
        pagina = "cinterno/home-interno.html"
    if request.user.loginsession.ProfileId == 5:
        pagina = "productor/home-productor.html"
    if request.user.loginsession.ProfileId == 6:
        pagina = "transportista/home-transportista.html"
    return pagina
