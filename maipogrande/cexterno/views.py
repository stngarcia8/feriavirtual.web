import operator
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render
from django.db.models import Q
from functools import reduce
from django.conf import settings
from django.views.generic.base import TemplateView
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from .forms import OrderForm, OrderDetailForm, OrderDetailFormSet
from .models import Order, OrderDetail, ExportProduct
from dcomercial.models import Comercial
from .services import GetExportProductFromApi

class HomeExternalCustomer(TemplateView):
    "Muestra la página de inicio del cliente externo."
    template_name = 'cexterno/home-externo.html'

def CargarProductosExportacion(request):
    "Carga los productos de exportacion de la base de datos de feria virtual."
    productos = ExportProduct.objects.filter(User_id=request.user.id)
    if productos.count() == 0:
        GetExportProductFromApi(request.user)
        productos = ExportProduct.objects.filter(User_id=request.user.id)
    return render(request, 'cexterno/home-externo.html', {'product_list': productos})


class OrderListView(ListView):
    "Muestra la lista de ordenes de compra"
    model = Order
    slug_field = 'User_id'
    slug_url_kwarg = 'User_id'
    template_name = 'cexterno/orden-listar.html'
    paginate_by = settings.RECORDS_PER_PAGE


class OrderDetailView(DetailView):
    model = Order
    template_name = 'cexterno/orden-ver.html'

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        return context



class OrderCreateView(CreateView):
    "Crea una nueva orden de compra."
    model = Order
    template_name = 'cexterno/orden-registrar.html'
    form_class = OrderForm
    success_url = reverse_lazy('listarOrdenes')

    def get_context_data(self, **kwargs):
        data = super(OrderCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['order_detail'] = OrderDetailFormSet(self.request.POST)
        else:
            data['order_detail'] = OrderDetailFormSet()
        try:
            data['comercial'] = Comercial.objects.get(User_id=self.request.user.id)
        except Exception:
            data['comercial'] =None
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        detalles = context['order_detail']
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            if detalles.is_valid():
                detalles.instance = self.object
                detalles.save()
        return super(OrderCreateView, self).form_valid(form)
