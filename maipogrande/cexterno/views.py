import operator
from django.urls import reverse_lazy
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.db.models import Q
from functools import reduce
from django.conf import settings
from django.views.generic.base import TemplateView
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from .forms import OrderForm, OrderDetailForm, OrderDetailFormSet
from .models import Order, OrderDetail
from dcomercial.models import Comercial


class HomeExternalCustomer(TemplateView):
    "Muestra la página de inicio del cliente externo."
    template_name = 'cexterno/home-externo.html'


class OrderListView(ListView):
    "Muestra la lista de ordenes de compra"
    model = Order
    slug_field = 'User_id'
    slug_url_kwarg = 'User_id'
    template_name = 'cexterno/orden-listar.html'
    paginate_by = settings.RECORDS_PER_PAGE


class OrderCreateView(CreateView):
    "Crea una nueva orden de compra."
    model = Order
    template_name = 'cexterno/orden-registrar.html'
    form_class = OrderForm
    success_url = reverse_lazy('listarOrdenes')

    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        comercial = None
        try:
            comercial = Comercial.objects.get(User_id=self.request.user.id)
        except Exception:
            comercial = None
        context['comercial'] = comercial
        return context

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        details = OrderDetail.objects.filter(Order=self.object).order_by('id')
        details_data = []
        for detail in details:
            d = {'Product': detail.Product, 'Quantity': detail.Quantity}
            details_data.append(d)
        orderDetailFormSet = OrderDetailFormSet(initial=details_data)
        return self.render_to_response(self.get_context_data(form=form, OrderDetailFormSet=orderDetailFormSet))

