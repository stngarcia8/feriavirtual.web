import operator
from functools import reduce

from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.views.generic.base import TemplateView

from core.permission import LoginRequired
from dcomercial.models import Comercial
from dcomercial.views import CargarDatoComercial
from .forms import CreateVehiculoForm, UpdateVehiculoForm, AuctionParticipateForm, DispatchForm
from ordenes.models import Order
from .models import Vehicle, Auction, BidModel, AuctionProduct, OrderDispatch, DispatchProducts
from .serializers import VehiculoSerializer, BidValueSerializer, DispatchApiserializer
from .services import PostToApi, PutToApi, DeleteToApi, GetFromApi, GetAuctionsFromApi, PostBidValueToApi, \
    GetDispatchesFromApi, DispatchDeliverToApi, DispatchCancelToApi


class CarrierRequired(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.loginsession.ProfileId == 6:
            return super().dispatch(request, *args, **kwargs)
        return redirect('restrictedaccess')  

class HomeCarrier(LoginRequired, CarrierRequired, TemplateView):
    "Carga la vista de transportista"
    template_name = 'transportista/home-transportista.html'


class VehiculoListView(LoginRequired, CarrierRequired, ListView):
    "Muestra la lista de vehiculos"
    model = Vehicle
    template_name = 'transportista/vehiculo-listar.html'
    paginate_by = settings.RECORDS_PER_PAGE

    def get_queryset(self):
        "Ejecuta el filtro de la lista desplegada."
        result = super(VehiculoListView, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
            result = result.filter(Q(ClientId=self.request.user.loginsession.ClientId) & Q(VehiclePatent__icontains=query))
        else:
            result = result.filter(ClientId=self.request.user.loginsession.ClientId)    
        return result


class VehiculoDetailView(LoginRequired, CarrierRequired, DetailView):
    "Muestra el detalle del vehiculo."
    model = Vehicle
    template_name = 'transportista/vehiculo-detalle.html'


class VehiculoCreateView(LoginRequired, CarrierRequired, CreateView):
    "Crea un nuevo vehiculo."
    model = Vehicle
    template_name = 'transportista/vehiculo-registrar.html'
    form_class = CreateVehiculoForm
    success_url = reverse_lazy('listarVehiculos')

    def form_valid(self, form):
        "Valida el formulario de ingreso."
        self.object = form.save(commit=False)
        self.object.ClientId = self.request.user.loginsession.ClientId
        self.object.User = self.request.user
        if PostToApi(VehiculoSerializer(instance=self.object, many=False)):
            self.object.save()
        return super(VehiculoCreateView, self).form_valid(form)


class VehiculoUpdateView(LoginRequired, CarrierRequired, UpdateView):
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


class VehiculoDeleteView(LoginRequired, CarrierRequired, DeleteView):
    "Permite eliminar un vehiculo de la lista de productos disponibles de un productor."
    model = Vehicle
    template_name = 'transportista/vehiculo-eliminar.html'
    success_url = reverse_lazy('listarVehiculos')

    def delete(self, request, *args, **kwargs):
        "Valida la eliminación del vehiculo."
        self.object = self.get_object()
        if DeleteToApi(self.object.VehicleId):
            self.object.delete()
        return redirect('listarVehiculos')


def VehiculosLoadView(request):
    "Carga la lista de vehiculos desde la base de datos de feria virtual."
    # GetFromApi(request.user)
    return redirect('listarVehiculos')


class AuctionListView(LoginRequired, CarrierRequired, ListView):
    "Muestra la lista de subastas disponibles"
    model = Auction
    template_name = 'transportista/subasta/subasta-listar.html'
    paginate_by = settings.RECORDS_PER_PAGE

    def get_queryset(self):
        result = super(AuctionListView, self).get_queryset()
        return result    

def AuctionsLoadView(request):
    "Carga la lista de subastas desde la base de datos de feria virtual."
    # auction = Auction.objects.all().delete()
    # GetAuctionsFromApi(request.user)
    return redirect('listarSubastas')

@login_required(login_url='login') 
def AuctionParticipateView(request, pk):
    if request.user.loginsession.ProfileId != 6:
        return redirect('restrictedaccess')
    form = AuctionParticipateForm(request.POST or None)
    template = loader.get_template("transportista/subasta/subasta-pujar.html")
    auction = Auction.objects.get(id=pk)
    auction_product = AuctionProduct.objects.filter(Auction=auction)
    bid_value = BidModel.objects.filter(AuctionId=auction.AuctionId)
    context = {'form': form, 'subasta': auction, 'productos': auction_product, 'puja': bid_value}
    return HttpResponse(template.render(context, request))

@login_required(login_url='login')
def ActualizarPujasView(request, pk):
    "Actualiza la vista de las pujas automaticamente."
    auction = Auction.objects.get(id=pk)
    bid_value = BidModel.objects.filter(AuctionId=auction.AuctionId)[:10]
    return render(request, 'transportista/subasta/pujas.html', {'pujas': bid_value})

@login_required(login_url='login')
def MostrarPujasView(request, pk):
    "Muestra los valores de las pujas realizadas."
    if request.user.loginsession.ProfileId != 6:
        return redirect('restrictedaccess')
    valor = request.GET.get('value')
    auction = Auction.objects.get(id=pk)
    bid = BidModel(AuctionId=auction.AuctionId, ClientId=request.user.loginsession.ClientId,
                   Value=valor, Bidder= request.user.loginsession.FullName)
    bid.save()
    PostBidValueToApi(BidValueSerializer(instance=bid))
    bid_value = BidModel.objects.filter(AuctionId=auction.AuctionId)[:10]
    return render(request, 'transportista/subasta/pujas.html', {'pujas': bid_value})
    
@login_required(login_url='login')
def AuctionShowView(request, pk):
    if request.user.loginsession.ProfileId != 6:
        return redirect('restrictedaccess')
    template = loader.get_template("transportista/subasta/subasta-detalle.html")
    auction = Auction.objects.get(id=pk)
    auction_product = AuctionProduct.objects.filter(Auction=auction)
    bid_value = BidModel.objects.filter(AuctionId=auction.AuctionId)
    context = {'subasta': auction, 'productos': auction_product, 'pujas': bid_value}
    return HttpResponse(template.render(context, request))


class DispatchListView(LoginRequired, CarrierRequired, ListView):
    "Muestra la lista de despachos"
    model = OrderDispatch
    slug_field = 'User_id'
    slug_url_kwarg = 'User_id'
    template_name = 'transportista/despacho/despacho-listar.html'
    paginate_by = settings.RECORDS_PER_PAGE

    def get_queryset(self):
        result = super(DispatchListView, self).get_queryset()
        query1 = self.request.GET.get('q1')
        query2 = self.request.GET.get('q2')
        if not query2:
            query2 = query1
        if query1:
            result = result.filter(StartDate__range=(query1, query2))
        return result


class DispatchDetailView(LoginRequired, CarrierRequired, DetailView):
    "Muestra el detalle del despacho."
    model = OrderDispatch
    template_name = 'transportista/despacho/despacho-detalle.html'

    def get_context_data(self, **kwargs):
        data = super(DispatchDetailView, self).get_context_data(**kwargs)
        detalles = DispatchProducts.objects.filter(OrderDispatch_id=self.object.id)
        data['dispatch_products'] = detalles
        return data


@login_required(login_url='login')
def DispatchLoadView(request):
    "Carga la lista de ordenes de despacho desde la base de datos de feria virtual."
    if request.user.loginsession.ProfileId != 6:
        return redirect('restrictedaccess')
    data = OrderDispatch.objects.filter(ClientId=request.user.loginsession.ClientId)
    if data.count() != 0:
        data.delete()
    GetDispatchesFromApi(request.user)
    return redirect('listarDespachos')


class DispatchDeliverUpdateView(LoginRequired, CarrierRequired, UpdateView):
    "Finalizar un despacho"
    model = OrderDispatch
    form_class = DispatchForm
    template_name = 'transportista/despacho/despacho-finalizar.html'
    success_url = reverse_lazy('listarDespachos')

    def form_valid(self, form):
        "Valida el formulario de finalización de un despacho."
        self.object = form.save(commit=False)
        self.object.ProfileId = self.request.user.loginsession.ProfileId
        self.object.Status = 6
        self.object.StatusDescription = 'ENTREGADO'
        if DispatchDeliverToApi(DispatchApiserializer(instance=self.object)):
            self.object.save()
            CambiarEstadoOrdenCompra(self.object.OrderId, 6)
        return super(DispatchDeliverUpdateView, self).form_valid(form)


class DispatchCancelUpdateView(LoginRequired, CarrierRequired, UpdateView):
    "Cancela un despacho"
    model = OrderDispatch
    form_class = DispatchForm
    template_name = 'transportista/despacho/despacho-cancelar.html'
    success_url = reverse_lazy('listarDespachos')

    def form_valid(self, form):
        "Valida el formulario de cancelación de un despacho."
        self.object = form.save(commit=False)
        self.object.ProfileId = self.request.user.loginsession.ProfileId
        self.object.Status = 9
        self.object.StatusDescription = 'CANCELADO'
        if DispatchCancelToApi(DispatchApiserializer(instance=self.object)):
            self.object.save()
            CambiarEstadoOrdenCompra(self.object.OrderId, 9)
        return super(DispatchCancelUpdateView, self).form_valid(form)        


def CambiarEstadoOrdenCompra(orderId, estado):
    orden_compra = Order.objects.get(OrderId=orderId)
    orden_compra.Status = estado
    orden_compra.save()
    return


class DespachosEntregadosListView(LoginRequired, CarrierRequired, ListView):
    "Muestra el historial de los despachos entregados"
    model = OrderDispatch
    template_name = 'historial/despachos-entregados-listar.html'
    paginate_by = settings.RECORDS_PER_PAGE

    def get_queryset(self):
        result = super(DespachosEntregadosListView, self).get_queryset()
        result = result.filter(Q(ClientId=self.request.user.loginsession.ClientId) & Q(Status=6))
        query1 = self.request.GET.get('q1')
        query2 = self.request.GET.get('q2')
        if not query2:
            query2 = query1
        if query1:
            result = result.filter(StartDate__range=(query1, query2))
        return result


class DespachosCanceladosListView(LoginRequired, CarrierRequired, ListView):
    "Muestra el historial de los despachos Cancelados"
    model = OrderDispatch
    template_name = 'historial/despachos-cancelados-listar.html'
    paginate_by = settings.RECORDS_PER_PAGE

    def get_queryset(self):
        result = super(DespachosCanceladosListView, self).get_queryset()
        result = result.filter(Q(ClientId=self.request.user.loginsession.ClientId) & Q(Status=9))
        query1 = self.request.GET.get('q1')
        query2 = self.request.GET.get('q2')
        if not query2:
            query2 = query1
        if query1:
            result = result.filter(StartDate__range=(query1, query2))
        return result

        


