from django.urls import reverse_lazy
from django.db.models import Q
from django.shortcuts import redirect
from django.db import transaction
from django.shortcuts import render
from django.conf import settings
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from .forms import OrderForm, OrderDetailFormSet
from .models import Order
from dcomercial.models import Comercial
from .services import PostToApi, DeleteToApi, PutToApi
from dcomercial.views import CargarDatoComercial

class OrderListView(ListView):
    "Muestra la lista de ordenes de compra"
    model = Order
    slug_field = 'User_id'
    slug_url_kwarg = 'User_id'
    template_name = 'ordenes/orden-listar.html'
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
    template_name = 'ordenes/orden-ver.html'


class OrderCreateView(CreateView):
    "Crea una nueva orden de compra."
    model = Order
    slug_field = 'User_id'
    slug_url_kwarg = 'User_id'
    template_name = 'ordenes/orden-registrar.html'
    form_class = OrderForm
    success_url = None

    def get_context_data(self, **kwargs):
        data = super(OrderCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['order_detail'] = OrderDetailFormSet(self.request.POST)
        else:
            data['order_detail'] = OrderDetailFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        detalles = context['order_detail']
        with transaction.atomic():
            form.instance.ClientID = self.request.user.loginsession.ClientID
            form.instance.User = self.request.user
            self.object = form.save()
            if detalles.is_valid():
                detalles.instance = self.object
                detalles.save()
                PostToApi(self.object.OrderID)
        return super(OrderCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('listarOrdenes')


class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'ordenes/orden-editar.html'

    def get_context_data(self, **kwargs):
        data = super(OrderUpdateView, self).get_context_data(**kwargs)
        data['comercial'] = Comercial.objects.get(User_id=self.request.user.id)
        if self.request.POST:
            data['order_detail'] = OrderDetailFormSet(
                self.request.POST, instance=self.object)
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
                PutToApi(self.object.OrderID)
        return super(OrderUpdateView, self).form_valid(form)


class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'ordenes/orden-eliminar.html'
    success_url = reverse_lazy('listarOrdenes')

    def delete(self, request, *args, **kwargs):
        "Valida la eliminación de la orden de compra."
        self.object = self.get_object()
        if DeleteToApi(self.object.OrderID):
            self.object.delete()
        return redirect('listarOrdenes')


def CargarOrdenesSinProcesar(request):
    "Carga las ordenes de compras no procesadas desde la base de feria virtual."
    criterio_user = Q(User_id=request.user.id)
    criterio_status = Q(Status=1)
    ordenes = Order.objects.filter(criterio_user & criterio_status)
    if ordenes.count() > 0:
        ordenes.delete()
    # aqui voy, cargando las ordenes desde la bdd.
    return render(request, 'cexterno/home-externo.html')
