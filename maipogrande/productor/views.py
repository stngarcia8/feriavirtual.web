from django.urls import reverse_lazy
from django.shortcuts import redirect
import operator
from django.db.models import Q
from functools import reduce
from django.template import loader
from django.http import HttpResponse
from django.conf import settings

import pandas as pd
from plotly.offline import plot
import plotly.graph_objs as go
from plotly.graph_objs import Scatter
import plotly.express as px
import numpy as np

from .forms import ProductoForm
from .models import Producto, Category, Venta
from django.views.generic.base import TemplateView
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from .services import PostToApi, PutToApi, DeleteToApi, GetFromApi
from .serializers import ProductoSerializer
from core.permission import LoginRequired
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class ProducerRequired(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.loginsession.ProfileId == 5:
            return super().dispatch(request, *args, **kwargs)
        return redirect('restrictedaccess')


class HomeProducer(LoginRequired, ProducerRequired, TemplateView):
    "Carga la vista de productor"
    template_name = 'productor/home-productor.html'


class ProductoListView(LoginRequired, ProducerRequired, ListView):
    "Muestra la lista de productos"
    model = Producto
    template_name = 'productor/producto-listar.html'
    paginate_by = settings.RECORDS_PER_PAGE

    def get_queryset(self):
        "Ejecuta el filtro de la lista desplegada."
        result = super(ProductoListView, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
            result = result.filter(Q(ClientId=self.request.user.loginsession.ClientId) & Q(ProductName__icontains=query))
        else:
            result = result.filter(ClientId=self.request.user.loginsession.ClientId)
        return result


class ProductoDetailView(LoginRequired, ProducerRequired, DetailView):
    "Muestra el detalle del producto."
    model = Producto
    template_name = 'productor/producto-detalle.html'


class ProductoCreateView(LoginRequired, ProducerRequired, CreateView):
    "Crea un nuevo producto."
    model = Producto
    template_name = 'productor/producto-registrar.html'
    form_class = ProductoForm
    success_url = reverse_lazy('listarProductos')

    def form_valid(self, form):
        "Valida el formulario de ingreso."
        self.object = form.save(commit=False)
        self.object.ClientId = self.request.user.loginsession.ClientId
        self.object.User = self.request.user
        if PostToApi(ProductoSerializer(instance=self.object)):
            self.object.save()
        return super(ProductoCreateView, self).form_valid(form)


class ProductoUpdateView(LoginRequired, ProducerRequired, UpdateView):
    "Actualiza la información de un producto."
    model = Producto
    form_class = ProductoForm
    template_name = 'productor/producto-editar.html'
    success_url = reverse_lazy('listarProductos')

    def form_valid(self, form):
        "Valida el formulario de actualización"
        self.object = form.save(commit=False)
        if PutToApi(ProductoSerializer(instance=self.object)):
            self.object.save()
        return super(ProductoUpdateView, self).form_valid(form)


class ProductoDeleteView(LoginRequired, ProducerRequired, DeleteView):
    "Permite eliminar un producto de la lista de productos disponibles de un productor."
    model = Producto
    template_name = 'productor/producto-eliminar.html'
    success_url = reverse_lazy('listarProductos')

    def delete(self, request, *args, **kwargs):
        "Valida la eliminación del producto."
        self.object = self.get_object()
        if DeleteToApi(self.object.ProductId):
            self.object.delete()
        return redirect('listarProductos')


def ProductosLoadView(request):
    return redirect('listarProductos')


class HistorialVentasListView(LoginRequired, ProducerRequired, ListView):
    "Permite visualizar las compras efectuadas por el productor."
    model = Venta
    template_name = 'ventas/historial-ventas-listar.html'
    paginate_by = settings.RECORDS_PER_PAGE

    def get_queryset(self):
        "Ejecuta el filtro de la lista desplegada."
        result = super(HistorialVentasListView, self).get_queryset()
        result = result.filter(Q(ClientId=self.request.user.loginsession.ClientId))
        query = self.request.GET.get('q')
        if query:
            result = result.filter(Q(ClientId=self.request.user.loginsession.ClientId) & Q(ProductName__icontains=query))
        else:
            result = result.filter(ClientId=self.request.user.loginsession.ClientId)
        return result

def VentasLoadView(request):
    return redirect('listarVentas')


@login_required(login_url='login')
def EstadisticasVentasDetailView(request):
    if request.user.loginsession.ProfileId == 5:
        template = loader.get_template('estadisticas/estadisticas-ventas-ver.html')
        ventas = Venta.objects.filter(ClientId=request.user.loginsession.ClientId).all().values()
        data = pd.DataFrame(ventas)
        if not ventas:
            context = {'ventas': ventas, 'data': data.to_html}
            return HttpResponse(template.render(context, request))    
        data = data.rename(columns={"SalesDate": "Fecha de venta", "Quantity": "Cantidad", "id": "N° de Venta",
                                "Quantity": "Cantidad", "ProductName": "Nombre Producto",
                                "ProductPrice": "Valor Total Producto"})
        data = data.round(decimals=0)
        valor_total = data["Valor Total Producto"].sum()
        valor_promedio = data["Valor Total Producto"].mean()
        valor_maximo = data["Valor Total Producto"].max()
        valor_minimo = data["Valor Total Producto"].min()
        # Grafico total ordenes de compra
        fig = px.bar(data, x="Nombre Producto", y="Valor Total Producto", color="Valor Total Producto")
        plot_div = plot(fig, output_type='div')
        # Grafico ordenes de compra por día
        fig = px.bar(data, x="Valor Total Producto", y="Fecha de venta")
        plots_div = plot(fig, output_type='div')
        context = {'ventas': ventas, 'data': data.to_html(), 'valor_total': valor_total,
                'valor_promedio': valor_promedio, 'valor_maximo': valor_maximo, 
                'valor_minimo': valor_minimo, "plot_div": plot_div, "plots_div": plots_div}
        return HttpResponse(template.render(context, request))
    return redirect('restrictedaccess')           
