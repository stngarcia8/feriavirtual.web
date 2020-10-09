from django.shortcuts import render
import operator
from django.db.models import Q
from functools import reduce
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import TransporteForm
from .models import Vehicle, VehicleType
from .serializers import TransportSerializer
from transportista.api import apifunctions
from django.views.generic import ListView, DetailView, TemplateView

# Create your views here.

# ListaDeTransportes:
# Lista los transportes desde el almacenamiento temporal
class ListaDeTransporte(ListView):
    model = Vehicle
    slug_field = 'User_id'
    slug_url_kwarg = 'User_id'
    template_name = 'transportista/transporte-listar.html'
    paginate_by = settings.RECORDS_PER_PAGE

    def get_queryset(self):
        result = super(ListaDeTransporte, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(reduce(operator.and_,
                                          (Q(VehiclePatent__icontains=q) for q in query_list)) |
                                   reduce(operator.and_, (Q(VehiclePatent__icontains=q)
                                                          for q in query_list)))
        return result


@login_required(login_url='login')
def ActualizarListaDeTransporte(request):
    datos = Vehicle.objects.filter(User_id=request.user.id)
    if datos.count() != 0:
        datos.delete()
    apifunctions.CargarTransporte(request.user)
    return redirect('listaDeTransporte')

class DetalleTransporte(DetailView):
    model = Vehicle
    template_name = 'transportista/transporte-detalle.html'

@login_required(login_url='login')
def RegistrarTransporte(request):
    form = TransporteForm(request.POST or None)
    template_name = loader.get_template("transportista/transporte-registrar.html")
    context_data = {'form': form, 'usuario': request.user, }
    if form.is_valid():
        serializador = TransportSerializer(data=form.cleaned_data)
        serializador.is_valid()
        resultado = apifunctions.GrabarTransporte(
            request.user, serializador)
        if resultado:
            return redirect('actualizarListaDeTransporte')
        else:
            return redirect('serviceNotAvailable')
    return HttpResponse(template_name.render(context_data, request))

def EditarTransporte(request, pk):
    vehicle = get_object_or_404(Vehicle, id=pk)
    form = TransporteForm(instance=vehicle)
    if request.method == 'POST':
        form = TransporteForm(request.POST, instance=vehicle)
        if form.is_valid():
            serializador = TransportSerializer(data=form.cleaned_data)
            serializador.is_valid()
            vehicleID = vehicle.VehicleID
            resultado = apifunctions.ActualizarTransporte(
                request.user, serializador, vehicleID)
            if resultado:
                form.save()
                return redirect('listaDeTransporte')
            else:
                return redirect('serviceNotAvailable')
            return redirect('listaDeTransporte')
    return render(request, 'transportista/transporte-editar.html', {'form': form})

class confirmDeleteTransport(TemplateView):
    template_name = 'transportista/transporte-confirmareliminar.html'  

    def get_context_data(self, **kwargs):
        context = super(confirmDeleteTransport, self).get_context_data(**kwargs)
        context['vehicle'] = Vehicle.objects.get(id=self.kwargs.get('pk'))
        return context

def EliminarTransporte(request, pk):
    vehicle = Vehicle.objects.get(id=pk)
    resultado = apifunctions.EliminarTransporte(vehicle.VehicleID)
    if resultado:
        vehicle.delete()
        return redirect('listaDeTransporte')
    return redirect('serviceNotAvailable')            
