from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, TemplateView

from core.views import DinamicHomePage
from .forms import CreateComercialForm
from .models import Comercial, City
from .serializers import ComercialSerializer
from .services import PostToApi, PutToApi, DeleteToApi, GetFromApi


def CargarDatoComercial(request):
    "Redirecciona a los usuarios a su página de inicio al cargar los datos comerciales cuando se carga por ajax."
    datos = Comercial.objects.filter(User_id=request.user.id)
    if datos.count() == 0:
        resultado = GetFromApi(request.user)
    return render(request, DinamicHomePage(request))


def IniciarDatoComercial(request):
    "Carga los datos comerciales desde el enlace de datos comerciales."
    datos = Comercial.objects.filter(User_id=request.user.id)
    if datos.count() == 0:
        resultado = GetFromApi(request.user)
        if resultado == False:
            return redirect('sinDatoComercial')
    comercial = Comercial.objects.get(User_id=request.user.id)
    return redirect('verComercial', comercial.id)


class ComercialTemplateView(TemplateView):
    "Carga la vista de datos comerciales inexistentes"
    template_name = 'dcomercial/comercial-sindato.html'


class ComercialDetailView(DetailView):
    "Muestra los datos comerciales"
    model = Comercial
    template_name = 'dcomercial/comercial-ver.html'


class ComercialCreateView(CreateView):
    "Crea un nuevo dato comercial"
    model = Comercial
    template_name = 'dcomercial/comercial-registrar.html'
    form_class = CreateComercialForm
    success_url = reverse_lazy('iniciarComercial')

    def form_valid(self, form):
        "Valida el formulario de ingreso"
        self.object = form.save(commit=False)
        self.object.ClientId = self.request.user.loginsession.ClientId
        self.object.User = self.request.user
        if PostToApi(ComercialSerializer(instance=self.object, many=False)):
            self.object.save()
        return super(ComercialCreateView, self).form_valid(form)


class ComercialUpdateView(UpdateView):
    "Actualiza la información de un dato comercial."
    model = Comercial
    form_class = CreateComercialForm
    template_name = 'dcomercial/comercial-editar.html'
    success_url = reverse_lazy('iniciarComercial')

    def form_valid(self, form):
        "Valida el formulario de actualización"
        self.object = form.save(commit=False)
        if PutToApi(ComercialSerializer(instance=self.object)):
            self.object.save()
        return super(ComercialUpdateView, self).form_valid(form)


class ComercialDeleteView(DeleteView):
    "Permite eliminar un dato comercial."
    model = Comercial
    template_name = 'dcomercial/comercial-eliminar.html'
    success_url = reverse_lazy('iniciarComercial')

    def delete(self, request, *args, **kwargs):
        "Valida la eliminación del dato comercial."
        self.object = self.get_object()
        if DeleteToApi(self.object.ComercialId):
            self.object.delete()
        return redirect('iniciarComercial')


def CargarCiudades(request):
    "Refresca el campo de ciudades dependiendo del país"
    country_id = request.GET.get('country_id')
    cities = City.objects.filter(Country_id=country_id).all()
    return render(request, 'dcomercial/ciudades.html', {'cities': cities})
