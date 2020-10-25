from django.urls import reverse_lazy
from django.db import transaction
from django.shortcuts import render
from django.conf import settings
from django.views.generic.base import TemplateView
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from .forms import OrderForm, OrderDetailFormSet
from .models import Order, ExportProduct
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

    def get_queryset(self):
        result = super(OrderListView, self).get_queryset()
        query1 = self.request.GET.get('q1')
        query2 = self.request.GET.get('q2')
        if not query2:
            query2 = query1
        if query1:
            result = result.filter(OrderDate__range=(query1, query2))
        return result


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
        data['comercial'] = Comercial.objects.get(User_id=self.request.user.id)
        if self.request.POST:
            data['order_detail'] = OrderDetailFormSet(self.request.POST)
        else:
            data['order_detail'] = OrderDetailFormSet()
        try:
            data['comercial'] = Comercial.objects.get(User_id=self.request.user.id)
        except Exception:
            data['comercial'] = None
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


class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'cexterno/orden-editar.html'

    def get_context_data(self, **kwargs):
        data = super(OrderUpdateView, self).get_context_data(**kwargs)
        data['comercial'] = Comercial.objects.get(User_id=self.request.user.id)
        if self.request.POST:
            data['order_detail'] = OrderDetailFormSet(self.request.POST, instance=self.object)
        else:
            data['order_detail'] = OrderDetailFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        details = context['order_detail']
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            if details.is_valid():
                details.instance = self.object
                details.save()
        return super(OrderUpdateView, self).form_valid(form)


class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'cexterno/orden-eliminar.html'
    success_url = reverse_lazy('listarOrdenes')
