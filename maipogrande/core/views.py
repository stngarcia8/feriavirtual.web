from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.views.defaults import page_not_found
from django.urls import reverse
from django.core.mail import EmailMessage
from .forms import ContactForm, ComercialForm
from .models import ComercialInfo, City
from .serializers import ComercialSerializer
from .api import apifunctions


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


# HomeProducer:
# Vista que redirecciona a pagina de inicio de los productores
class HomeProducer(TemplateView):
    template_name = 'core/home-productor.html'


# HomeCarrier:
# Vista que redirecciona a pagina de inicio de los productores
class HomeCarrier(TemplateView):
    template_name = 'core/home-transportista.html'


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
        pagina = "core/home-productor.html"
    if request.user.loginsession.ProfileID == 6:
        pagina = "core/home-transportista.html"
    miPlantilla = loader.get_template(pagina)
    return HttpResponse(miPlantilla.render({}, request))


# VerComercial(request):
# Visualiza los datos comerciales de el usuario logeado.
@login_required(login_url='login')
def VerComercial(request):
    datos = ComercialInfo.objects.filter(User_id=request.user.id)
    if datos.count() == 0:
        datos = apifunctions.CargarDatosComerciales(request.user)
    else:
        datos = ComercialInfo.objects.get(User_id=request.user.id)
    template_name = loader.get_template('core/comercial-ver.html')
    context_data = {'comercial': datos}
    return HttpResponse(template_name.render(context_data, request))


# RegistrarComercial(request)
# Vista que permite el ingreso de datos comerciales del cliente.
def RegistrarComercial(request):
    form = ComercialForm(request.POST or None)
    template_name = loader.get_template("core/comercial-registrar.html")
    context_data = {'form': form, 'usuario': request.user, }
    if form.is_valid():
        serializador = ComercialSerializer(data=form.cleaned_data)
        serializador.is_valid()
        resultado = apifunctions.GrabarDatoComercial(
            request.user, serializador)
        if resultado:
            return redirect('dinamicHome')
        else:
            return redirect('serviceNotAvailable')
    return HttpResponse(template_name.render(context_data, request))


# EditarComercial(request)
# Vista que permite la modificacion de datos comerciales por parte del usuario.
def EditarComercial(request):
    comercial = get_object_or_404(ComercialInfo, User_id=request.user.id)
    form = ComercialForm(instance=comercial)
    if request.method == 'POST':
        form = ComercialForm(request.POST, instance=comercial)
        if form.is_valid():
            serializador = ComercialSerializer(data=form.cleaned_data)
            serializador.is_valid()
            comercialID = comercial.ComercialID
            resultado = apifunctions.ActualizarDatoComercial(
                request.user, serializador, comercialID)
            if resultado:
                form.save()
                return redirect('verComercial')
            else:
                return redirect('serviceNotAvailable')
            return redirect('verComercial')
    return render(request, 'core/comercial-editar.html', {'form': form})


# confirmDeleteComercial:
# Vista que consulta al usuario si desea realmente eliminar los datos comerciales
class confirmDeleteComercial(TemplateView):
    template_name = 'core/comercial-confirmareliminar.html'


# EliminarComercial(request)
# Elimina los datos comerciales de la base de datos permanentemente
def EliminarComercial(request):
    comercial = ComercialInfo.objects.get(User_id=request.user.id)
    resultado = apifunctions.EliminarDatosComerciales(comercial.ComercialID)
    if resultado:
        comercial.delete()
        return redirect('comercialWasDelete')
    return redirect('serviceNotAvailable')


# ComercialHasBeenDeleted:
# Vista que informa al usuario que sus datos comerciales fueron eliminados
class ComercialWasDelete(TemplateView):
    template_name = 'core/comercial-eliminado.html'


# CargarCiudades(request():
# Vista que permite refrescar el campo de ciudades dependiendo del pais seleccionado.
# retorna:
#   Vista renderizada de las ciudades.
def CargarCiudades(request):
    country_id = request.GET.get('country_id')
    cities = City.objects.filter(Country_id=country_id).all()
    return render(request, 'core/ciudades.html', {'cities': cities})
