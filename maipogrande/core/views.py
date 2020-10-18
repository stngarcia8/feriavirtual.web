from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.views.defaults import page_not_found
from django.urls import reverse
from django.core.mail import EmailMessage


# Home:
# Vista que redirecciona a pagina de inicio.
class Home(TemplateView):
    template_name = 'core/home.html'


# HomeExternalCustomer:
# Vista que redirecciona a pagina de inicio de los clientes externos
class HomeExternalCustomer(TemplateView):
    template_name = 'core/home-externo.html'


# HomeInternalCustomer:
# Vista que redirecciona a pagina de inicio de los clientes internos
class HomeInternalCustomer(TemplateView):
    template_name = 'core/home-interno.html'


# About:
# Vista que redirecciona a pagina acerca de feria virtual
class About(TemplateView):
    template_name = 'core/about.html'


# Error_404:
# Vista que muestra pagina de error 404 cuando un usuario ingresa por url y el recurso no esta disponible.
def Error_404(request, exception):
    return page_not_found(request, template_name='core/404.html', status=404)


# Contact:
# Vista para realizar el contacto y solicitar una cuenta de usuario en la plataforma
def Contact(request):
    contact_form = ContactForm()
    if request.method == "POST":
        contact_form = ContactForm(data=request.POST)
        if contact_form.is_valid():
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
    return render(request, "core/contact.html", {'form': contact_form})


# MailOk:
# Vista que indica al usuario que su correo fue enviado correctamente.
class EmailOk(TemplateView):
    template_name = 'core/emailsent.html'


# MailFail:
# Vista que indica al usuario que su correo fallo.
class EmailFail(TemplateView):
    template_name = 'core/failedemail.html'


# ServiceNotAvailable:
# Vista que indica que los servicios no se encuentran disponibles.
class ServiceNotAvailable(TemplateView):
    template_name = 'core/servicenotavailable.html'


# DinamicHome()
# Vista que permite cargar la pagina de inicio segun el perfil del cliente
@login_required(login_url='login')
def DinamicHome(request):
    pagina = "core/home.html"
    if request.user.loginsession.ProfileID == 3:
        pagina = "core/home-externo.html"
    if request.user.loginsession.ProfileID == 4:
        pagina = "core/home-interno.html"
    if request.user.loginsession.ProfileID == 5:
        pagina = "productor/home-productor.html"
    if request.user.loginsession.ProfileID == 6:
        pagina = "transportista/home-transportista.html"
    miPlantilla = loader.get_template(pagina)
    return HttpResponse(miPlantilla.render({}, request))
