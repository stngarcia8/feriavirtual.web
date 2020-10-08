import operator
from django.views.generic.base import TemplateView
from django.db.models import Q
from functools import reduce
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from .forms import ProductoForm
from .models import Producto
from .serializers import ProductoSerializer
from productor.api import apifunctions
from django.views.generic import ListView, DetailView


# ListaDeProductos:
# Lista los productos desde el almacenamiento temporal
class ListaDeProductos(ListView):
    model = Producto
    slug_field = 'User_id'
    slug_url_kwarg = 'User_id'
    template_name = 'productor/producto-listar.html'
    paginate_by = settings.RECORDS_PER_PAGE

    def get_queryset(self):
        result = super(ListaDeProductos, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(reduce(operator.and_,
                                          (Q(ProductName__icontains=q) for q in query_list)) |
                                   reduce(operator.and_, (Q(ProductName__icontains=q)
                                                          for q in query_list)))
        return result


@login_required(login_url='login')
def ActualizarListaDeProductos(request):
    datos = Producto.objects.filter(User_id=request.user.id)
    if datos.count() != 0:
        datos.delete()
    apifunctions.CargarProductos(request.user)
    return redirect('listaDeProductos')


class DetalleProducto(DetailView):
    model = Producto
    template_name = 'productor/producto-detalle.html'


@login_required(login_url='login')
def RegistrarProducto(request):
    form = ProductoForm(request.POST or None)
    template_name = loader.get_template("productor/producto-registrar.html")
    context_data = {'form': form, 'usuario': request.user, }
    if form.is_valid():
        serializador = ProductoSerializer(data=form.cleaned_data)
        serializador.is_valid()
        resultado = apifunctions.GrabarProducto(
            request.user, serializador)
        if resultado:
            return redirect('listaDeProductos')
        else:
            return redirect('serviceNotAvailable')
    return HttpResponse(template_name.render(context_data, request))


def EditarProducto(request, pk):
    producto = get_object_or_404(Producto, id=pk)
    form = ProductoForm(instance=producto)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            serializador = ProductoSerializer(data=form.cleaned_data)
            serializador.is_valid()
            productID = producto.ProductID
            resultado = apifunctions.ActualizarProductos(
                request.user, serializador, productID)
            if resultado:
                form.save()
                return redirect('listaDeProductos')
            else:
                return redirect('serviceNotAvailable')
            return redirect('listaDeProductos')
    return render(request, 'productor/producto-editar.html', {'form': form})

class confirmDeleteProduct(TemplateView):
    template_name = 'productor/producto-confirmareliminar.html'  

    def get_context_data(self, **kwargs):
        context = super(confirmDeleteProduct, self).get_context_data(**kwargs)
        context['producto'] = Producto.objects.get(id=self.kwargs.get('pk'))
        return context
    
    
def EliminarProducto(request, pk):
    producto = Producto.objects.get(id=pk)
    resultado = apifunctions.EliminarProducto(producto.ProductID)
    if resultado:
        producto.delete()
        return redirect('listaDeProductos')
    return redirect('serviceNotAvailable')          
