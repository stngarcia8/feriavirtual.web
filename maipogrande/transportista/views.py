import operator
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.db.models import Q
from functools import reduce
from django.conf import settings
from .forms import CreateVehiculoForm, UpdateVehiculoForm
from .models import Vehicle
from dcomercial.models import Comercial
from django.views.generic.base import TemplateView
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from .services import PostToApi, PutToApi, DeleteToApi, GetFromApi
from .serializers import VehiculoApiSerializer, VehiculoSerializer
from dcomercial.views import CargarDatoComercial


class HomeCarrier(TemplateView):
    "Carga la vista de transportista"
    template_name = 'transportista/home-transportista.html'

    def get_context_data(self, **kwargs):
        data = super(HomeCarrier, self).get_context_data(**kwargs)
        CargarDatoComercial(self.request)
        try:
            comercial = Comercial.objects.get(User_id=self.request.user.id)
        except Exception:
            comercial = None
        data['comercial'] = comercial
        return data       


class VehiculoListView(ListView):
    "Muestra la lista de vehiculos"
    model = Vehicle
    slug_field = 'User_id'
    slug_url_kwarg = 'User_id'
    template_name = 'transportista/vehiculo-listar.html'
    paginate_by = settings.RECORDS_PER_PAGE

    def get_queryset(self):
        "Ejecuta el filtro de la lista desplegada."
        result = super(VehiculoListView, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(reduce(operator.and_,
                                          (Q(VehiclePatent__icontains=q) for q in query_list)) |
                                   reduce(operator.and_, (Q(VehiclePatent__icontains=q)
                                                          for q in query_list)))
        return result


class VehiculoDetailView(DetailView):
    "Muestra el detalle del vehiculo."
    model = Vehicle
    template_name = 'transportista/vehiculo-detalle.html'


class VehiculoCreateView(CreateView):
    "Crea un nuevo vehiculo."
    model = Vehicle
    template_name = 'transportista/vehiculo-registrar.html'
    form_class = CreateVehiculoForm
    success_url = reverse_lazy('listarVehiculos')

    def form_valid(self, form):
        "Valida el formulario de ingreso."
        self.object = form.save(commit=False)
        self.object.ClientID = self.request.user.loginsession.ClientID
        self.object.User = self.request.user
        if PostToApi(VehiculoSerializer(instance=self.object, many=False)):
            self.object.save()
        return super(VehiculoCreateView, self).form_valid(form)


class VehiculoUpdateView(UpdateView):
    "Actualiza la información de un vehiculo."
    model = Vehicle
    form_class = UpdateVehiculoForm
    template_name = 'transportista/vehiculo-editar.html'
    success_url = reverse_lazy('listarVehiculos')

    def form_valid(self, form):
        "Valida el formulario de actualización"
        self.object = form.save(commit=False)
        if PutToApi(VehiculoSerializer(instance=self.object)):
            self.object.save()
        return super(VehiculoUpdateView, self).form_valid(form)


class VehiculoDeleteView(DeleteView):
    "Permite eliminar un vehiculo de la lista de productos disponibles de un productor."
    model = Vehicle
    template_name = 'transportista/vehiculo-eliminar.html'
    success_url = reverse_lazy('listarVehiculos')

    def delete(self, request, *args, **kwargs):
        "Valida la eliminación del vehiculo."
        self.object = self.get_object()
        if DeleteToApi(self.object.VehicleID):
            self.object.delete()
        return redirect('listarVehiculos')


def VehiculosLoadView(request):
    "Carga la lista de vehiculos desde la base de datos de feria virtual."
    data = Vehicle.objects.filter(User_id=request.user.id)
    if data.count() != 0:
        data.delete()
    GetFromApi(request.user)
    return redirect('listarVehiculos')

