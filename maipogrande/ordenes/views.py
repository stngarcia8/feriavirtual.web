from django.urls import reverse_lazy
from django.db.models import Q
from django.shortcuts import redirect
from django.db import transaction
from django.shortcuts import render
from django.conf import settings
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from .forms import OrderForm, OrderDetailFormSet
from .models import Order, OrderDetail
from dcomercial.models import Comercial
from .services import PostToApi, DeleteToApi, PutToApi
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
        result = result.filter(ClientId=self.request.user.loginsession.ClientId)
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
        if self.request.POST:
            data['order_detail'] = OrderDetailFormSet(
                self.request.POST, instance=self.object)
        else:
            data['order_detail'] = OrderDetailFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        details = context['order_detail']
        print()
        print("forrmset")
        print(details.errors)
        print()
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
    criterio_user = Q(User_id=request.user.id)
    criterio_status = Q(Status=1)
    ordenes = Order.objects.filter(criterio_user & criterio_status)
    if ordenes.count() > 0:
        ordenes.delete()
    # aqui voy, cargando las ordenes desde la bdd.
    return render(request, 'cexterno/home-externo.html')

def OrdenesLoadView(request):
    return redirect('listarOrdenes')
