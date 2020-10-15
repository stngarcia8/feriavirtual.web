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
from .serializers import ProductoSerializer, ProductoApiSerializer


class HomeProducer(TemplateView):
    "Carga la vista de productor"
    template_name = 'productor/home-productor.html'


class ProductoListView(ListView):
    "Muestra la lista de productos"
    model = Producto
    slug_field = 'User_id'
    slug_url_kwarg = 'User_id'
    template_name = 'productor/producto-listar.html'
    paginate_by = settings.RECORDS_PER_PAGE

    def get_queryset(self):
        "Ejecuta el filtro de la lista desplegada."
        result = super(ProductoListView, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(reduce(operator.and_,
                                          (Q(ProductName__icontains=q) for q in query_list)) |
                                   reduce(operator.and_, (Q(ProductName__icontains=q)
                                                          for q in query_list)))
        return result


class ProductoDetailView(DetailView):
    "Muestra el detalle del producto."
    model = Producto
    template_name = 'productor/producto-detalle.html'


class ProductoCreateView(CreateView):
    "Crea un nuevo producto."
    model = Producto
    template_name = 'productor/producto-registrar.html'
    form_class = ProductoForm
    success_url = reverse_lazy('listarProductos')

    def form_valid(self, form):
        "Valida el formulario de ingreso."
        self.object = form.save(commit=False)
        self.object.ClientID = self.request.user.loginsession.ClientID
        self.object.User = self.request.user
        if PostToApi(ProductoSerializer(instance=self.object)):
            self.object.save()
        return super(ProductoCreateView, self).form_valid(form)


class ProductoUpdateView(UpdateView):
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


class ProductoDeleteView(DeleteView):
    "Permite eliminar un producto de la lista de productos disponibles de un productor."
    model = Producto
    template_name = 'productor/producto-eliminar.html'
    success_url = reverse_lazy('listarProductos')

    def delete(self, request, *args, **kwargs):
        "Valida la eliminación del producto."
        self.object = self.get_object()
        if DeleteToApi(self.object.ProductID):
            self.object.delete()
        return redirect('listarProductos')


def ProductosLoadView(request):
    data = Producto.objects.filter(User_id=request.user.id)
    if data.count() != 0:
        data.delete()
        GetFromApi(request.user)
    return redirect('listarProductos')