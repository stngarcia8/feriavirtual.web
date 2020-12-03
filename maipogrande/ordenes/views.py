import uuid
from django.urls import reverse_lazy
from django.db.models import Q
from django.shortcuts import redirect
from django.db import transaction
from django.shortcuts import render
from django.conf import settings
from django.template import loader
from django.http import HttpResponse

import pandas as pd
from plotly.offline import plot
import plotly.graph_objs as go
from plotly.graph_objs import Scatter
import plotly.express as px
import numpy as np

from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from .forms import OrderForm, OrderDetailFormSet, OrderRefuseForm, OrderAcceptForm
from .models import Order, OrderDetail, OrderRefuse, Payment
from dcomercial.models import Comercial
from productor.models import Producto, Category
from .services import PostToApi, DeleteToApi, PutToApi, PostOrderRefuseToApi, PostAcceptToApi
from .serializers import OrderRefuseSerializer, OrderAcceptSerializer
from dcomercial.views import CargarDatoComercial
from core.permission import LoginRequired

class ClientRequired(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.loginsession.ProfileId == 3 or request.user.loginsession.ProfileId == 4:
            return super().dispatch(request, *args, **kwargs)
        return redirect('restrictedaccess')
        

class OrderListView(LoginRequired, ClientRequired, ListView):
    "Muestra la lista de ordenes de compra"
    model = Order
    template_name = 'ordenes/orden-listar.html'
    paginate_by = settings.RECORDS_PER_PAGE

    def get_queryset(self):
        result = super(OrderListView, self).get_queryset()
        result = result.filter(Q(ClientId=self.request.user.loginsession.ClientId) & Q(Status__range=(1, 5)))
        query1 = self.request.GET.get('q1')
        query2 = self.request.GET.get('q2')
        query2 = query1 if not query2 else query2
        if query1:
            result = result.filter(OrderDate__range=(query1, query2))
        return result


class OrderDetailView(LoginRequired, ClientRequired, DetailView):
    model = Order
    template_name = 'ordenes/orden-ver.html'
    
    def get_context_data(self, **kwargs):
        data = super(OrderDetailView, self).get_context_data(**kwargs)
        detalles = OrderDetail.objects.filter(Order_id=self.object.id)
        data['order_detail'] = detalles
        return data


class OrderCreateView(LoginRequired, ClientRequired, CreateView):
    "Crea una nueva orden de compra."
    model = Order
    template_name = 'ordenes/orden-registrar.html'
    form_class = OrderForm
    success_url = None

    def get_context_data(self, **kwargs):
        data = super(OrderCreateView, self).get_context_data(**kwargs)
        categoria = 1 if self.request.user.loginsession.ProfileId == 3 else 2
        filtro_categoria = Category.objects.get(CategoryId=categoria)
        productos = Producto.objects.filter(Q(Category=filtro_categoria) & Q(ProductQuantity__gt=0)).order_by('ProductName').distinct('ProductName')
        if self.request.POST:
            form_set_detail = OrderDetailFormSet(self.request.POST)
        else:
             form_set_detail = OrderDetailFormSet()
        for form in form_set_detail:
            form.fields['Product'].queryset = productos
        data['order_detail'] = form_set_detail
        return data


    def form_valid(self, form):
        context = self.get_context_data()
        detalles = context['order_detail']
        with transaction.atomic():
            form.instance.ClientId = self.request.user.loginsession.ClientId
            form.instance.User = self.request.user
            self.object = form.save()
            if detalles.is_valid():
                detalles.instance = self.object
                detalles.save()
                PostToApi(self.object.OrderId)
        return super(OrderCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('listarOrdenes')


class OrderUpdateView(LoginRequired, ClientRequired, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'ordenes/orden-editar.html'

    def get_context_data(self, **kwargs):
        data = super(OrderUpdateView, self).get_context_data(**kwargs)
        categoria = 1 if self.request.user.loginsession.ProfileId == 3 else 2
        productos = Producto.objects.filter(Q(Category_id=categoria) & Q(ProductQuantity__gt=1))
        if self.request.POST:
            form_set_detail = OrderDetailFormSet(
                self.request.POST, instance=self.object)
        else:
            form_set_detail = OrderDetailFormSet(instance=self.object)
        for form in form_set_detail:
            form.fields['Product'].queryset = productos
        data['order_detail'] = form_set_detail    
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        details = context['order_detail']
        with transaction.atomic():
            self.object = form.save()
            if details.is_valid():
                details.instance = self.object
                details.save()
                PutToApi(self.object.OrderId)
        return super(OrderUpdateView, self).form_valid(form)


class OrderDeleteView(LoginRequired, ClientRequired, DeleteView):
    model = Order
    template_name = 'ordenes/orden-eliminar.html'
    success_url = reverse_lazy('listarOrdenes')

    def delete(self, request, *args, **kwargs):
        "Valida la eliminación de la orden de compra."
        self.object = self.get_object()
        if DeleteToApi(self.object.OrderId):
            self.object.delete()
        return redirect('listarOrdenes')


def CargarOrdenesSinProcesar(request):
    "Carga las ordenes de compras no procesadas desde la base de feria virtual."
    if request.user.loginsession.ProfileId == 3 or request.user.loginsession.ProfileId == 4:
        criterio_user = Q(User_id=request.user.id)
        criterio_status = Q(Status=1)
        ordenes = Order.objects.filter(criterio_user & criterio_status)
        if ordenes.count() > 0:
            ordenes.delete()
        return render(request, 'cexterno/home-externo.html')
    return redirect('restrictedaccess')    

def OrdenesLoadView(request):
    return redirect('listarOrdenes')


class ConfirmarOrdenListView(LoginRequired, ClientRequired, ListView):
    "Muestra la lista de ordenes de compra con estado entregado"
    model = Order
    template_name = 'confirmar/confirmar-orden-listar.html'
    paginate_by = settings.RECORDS_PER_PAGE

    def get_queryset(self):
        result = super(ConfirmarOrdenListView, self).get_queryset()
        result = result.filter(Q(ClientId=self.request.user.loginsession.ClientId) & Q(Status=6))
        query1 = self.request.GET.get('q1')
        query2 = self.request.GET.get('q2')
        query2 = query1 if not query2 else query2
        if query1:
            result = result.filter(OrderDate__range=(query1, query2))
        return result


class ConfirmarOrdenDetailView(LoginRequired, ClientRequired, DetailView):
    model = Order
    template_name = 'confirmar/confirmar-orden-ver.html'
    
    def get_context_data(self, **kwargs):
        data = super(ConfirmarOrdenDetailView, self).get_context_data(**kwargs)
        detalles = OrderDetail.objects.filter(Order_id=self.object.id)
        data['order_detail'] = detalles
        return data


class OrderRefuseUpdateView(LoginRequired, ClientRequired, UpdateView):
    "Rechazar productos"
    model = Order
    form_class = OrderRefuseForm
    template_name = 'confirmar/confirmar-orden-rechazar.html'
    success_url = reverse_lazy('listarOrdenesEntregadas')

    def form_valid(self, form):
        "Valida el formulario de rechazo de productos."
        self.object = form.save(commit=False)
        self.object.ClientId = self.request.user.loginsession.ClientId
        self.object.Status = 8
        order_refuse = OrderRefuse(
            RefuseId=uuid.uuid4,
            OrderId=self.object.OrderId,
            RefuseType=8,
            Observation=self.object.CustomerObservation
        )
        if PostOrderRefuseToApi(OrderRefuseSerializer(instance=order_refuse)):
            self.object.save()
        return super(OrderRefuseUpdateView, self).form_valid(form) 


class OrderAcceptCreateView(LoginRequired, ClientRequired, CreateView):
    "Aceptar productos"
    model = Payment
    form_class = OrderAcceptForm
    template_name = 'confirmar/confirmar-orden-aceptar.html'
    success_url = reverse_lazy('listarOrdenesEntregadas')

    def get_context_data(self, **kwargs):
        data = super(OrderAcceptCreateView, self).get_context_data(**kwargs)
        orden_compra = Order.objects.get(pk=self.kwargs.get('pk'))
        detalle_orden = OrderDetail.objects.filter(Order=orden_compra)
        data['details'] = detalle_orden
        data['orden'] = orden_compra
        return data

    def form_valid(self, form, **kwargs):
        "Valida el formulario de aceptación de productos."
        data = self.get_context_data(**kwargs)
        orden_compra = data['orden']
        self.object = form.save(commit=False)
        self.object.ClientId = self.request.user.loginsession.ClientId
        self.object.Order = orden_compra
        self.object.OrderId = orden_compra.OrderId
        self.object.User = self.request.user
        self.object.Amount = orden_compra.Amount
        if PostAcceptToApi(OrderAcceptSerializer(instance=self.object)):
            self.object.save()
            orden_compra.Status = 7
            orden_compra.save()
        return super(OrderAcceptCreateView, self).form_valid(form)


def ConfirmarOrdenesLoadView(request):
    return redirect('listarOrdenesEntregadas')


class OrdenRechazadaListView(LoginRequired, ClientRequired, ListView):
    "Muestra la lista de ordenes de compra con estado rechazada"
    model = Order
    template_name = 'rechazadas/orden-rechazada-listar.html'
    paginate_by = settings.RECORDS_PER_PAGE

    def get_queryset(self):
        result = super(OrdenRechazadaListView, self).get_queryset()
        result = result.filter(Q(ClientId=self.request.user.loginsession.ClientId) & Q(Status=8))
        query1 = self.request.GET.get('q1')
        query2 = self.request.GET.get('q2')
        query2 = query1 if not query2 else query2
        if query1:
            result = result.filter(OrderDate__range=(query1, query2))
        return result


class OrdenRechazadaDetailView(LoginRequired, ClientRequired, DetailView):
    model = Order
    template_name = 'rechazadas/orden-rechazada-ver.html'
    
    def get_context_data(self, **kwargs):
        data = super(OrdenRechazadaDetailView, self).get_context_data(**kwargs)
        detalles = OrderDetail.objects.filter(Order_id=self.object.id)
        data['order_detail'] = detalles
        return data


def OrdenesRechazadasLoadView(request):
    return redirect('listarOrdenesRechazadas')


class OrdenAceptadaListView(LoginRequired, ClientRequired, ListView):
    "Muestra la lista de ordenes de compra con estado aceptado"
    model = Order
    template_name = 'aceptadas/orden-aceptada-listar.html'
    paginate_by = settings.RECORDS_PER_PAGE

    def get_queryset(self):
        result = super(OrdenAceptadaListView, self).get_queryset()
        result = result.filter(Q(ClientId=self.request.user.loginsession.ClientId) & Q(Status=7))
        query1 = self.request.GET.get('q1')
        query2 = self.request.GET.get('q2')
        query2 = query1 if not query2 else query2
        if query1:
            result = result.filter(OrderDate__range=(query1, query2))
        return result


class OrdenAceptadaDetailView(LoginRequired, ClientRequired, DetailView):
    model = Order
    template_name = 'aceptadas/orden-aceptada-ver.html'
    
    def get_context_data(self, **kwargs):
        data = super(OrdenAceptadaDetailView, self).get_context_data(**kwargs)
        detalles = OrderDetail.objects.filter(Order_id=self.object.id)
        data['order_detail'] = detalles
        pago = Payment.objects.get(OrderId=self.object.OrderId)
        data['payment'] = pago
        return data


def OrdenesAceptadasLoadView(request):
    return redirect('listarOrdenesAceptadas')


@login_required(login_url='login')
def HistorialComprasDetailView(request):
    if request.user.loginsession.ProfileId == 3 or request.user.loginsession.ProfileId ==4:
        pagos = Payment.objects.filter(ClientId=request.user.loginsession.ClientId).all().values()
        template = loader.get_template('compras/historial-compras-ver.html')
        context = {'pagos': pagos}
        return HttpResponse(template.render(context, request))
    return redirect('restrictedaccess')


@login_required(login_url='login')
def EstadisticasDetailView(request):
    if request.user.loginsession.ProfileId == 3 or request.user.loginsession.ProfileId ==4:
        pagos = Payment.objects.filter(ClientId=request.user.loginsession.ClientId).all().values()
        template = loader.get_template('estadisticas/estadistica-ordenes-ver.html')
        data = pd.DataFrame(pagos)
        if not pagos:
            context = {'pagos': pagos, 'data': data.to_html}
            return HttpResponse(template.render(context, request))
        data = data.rename(columns={"PaymentDate": "Fecha de pago", "Amount": "Total pagado", "id": "N° de Orden"})
        data = data.round(decimals=0)
        valor_total = data["Total pagado"].sum()
        valor_promedio = data["Total pagado"].mean()
        valor_maximo = data["Total pagado"].max()
        valor_minimo = data["Total pagado"].min()
        # Grafico total ordenes de compra
        fig = px.bar(data, x="N° de Orden", y="Total pagado", color="Total pagado")
        plot_div = plot(fig, output_type='div')
        # Grafico ordenes de compra por día
        fig = px.bar(data, x="Total pagado", y="Fecha de pago")
        plots_div = plot(fig, output_type='div')
        context = {'pagos': pagos, 'data': data.to_html(), 'plot_div': plot_div, 'valor_total': valor_total,
                'valor_promedio': valor_promedio, 'valor_maximo': valor_maximo, 'valor_minimo': valor_minimo,
                'plots_div': plots_div}
        return HttpResponse(template.render(context, request))
    return redirect('restrictedaccess')         



 
    
   
