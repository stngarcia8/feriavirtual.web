from django.urls import reverse_lazy
from django.shortcuts import redirect
import operator
from django.db.models import Q
from functools import reduce
from django.conf import settings
from .forms import ProductoForm
from .models import Producto
from django.views.generic.base import TemplateView
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from .services import PostToApi, PutToApi, DeleteToApi, GetFromApi
from .serializers import ProductoSerializer
from core.permission import LoginRequired

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
    # GetFromApi(request.user)
    return redirect('listarProductos')
