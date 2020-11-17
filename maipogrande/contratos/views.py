from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView
from core.permission import LoginRequired
from .forms import ContractForm
from .models import Contract
from .serializers import ContractApiserializer
from .services import GetFromApi, PatchAcceptToApi, PatchRefuseToApi


class UserRequired(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.loginsession.ProfileId == 5 or request.user.loginsession.ProfileId == 6:
            return super().dispatch(request, *args, **kwargs)
        return redirect('restrictedaccess')


class ContratoListView(LoginRequired, UserRequired, ListView):
    "Muestra la lista de contratos"
    model = Contract
    slug_field = 'User_id'
    slug_url_kwarg = 'User_id'
    template_name = 'contratos/contrato-listar.html'
    paginate_by = settings.RECORDS_PER_PAGE

    def get_queryset(self):
        result = super(ContratoListView, self).get_queryset()
        query1 = self.request.GET.get('q1')
        query2 = self.request.GET.get('q2')
        if not query2:
            query2 = query1
        if query1:
            result = result.filter(StartDate__range=(query1, query2))
        return result


class ContratoDetailView(LoginRequired, UserRequired, DetailView):
    "Muestra el detalle del contrato."
    model = Contract
    template_name = 'contratos/contrato-detalle.html'


def ContratosLoadView(request):
    "Carga la lista de contratos desde la base de datos de feria virtual."
    GetFromApi(request.user)
    return redirect('listarContratos')


class ContratoAcceptUpdateView(LoginRequired, UserRequired, UpdateView):
    "Acepta un contrato"
    model = Contract
    form_class = ContractForm
    template_name = 'contratos/contrato-aceptar.html'
    success_url = reverse_lazy('listarContratos')

    def form_valid(self, form):
        "Valida el formulario de aceptación de un contrato."
        self.object = form.save(commit=False)
        self.object.ProfileId = self.request.user.loginsession.ProfileId
        self.object.Status = 1
        self.object.StatusDescription = 'Aceptado'
        if PatchAcceptToApi(ContractApiserializer(instance=self.object)):
            self.object.save()
        return super(ContratoAcceptUpdateView, self).form_valid(form)


class ContratoRefuseUpdateView(LoginRequired, UserRequired, UpdateView):
    "Rechaza un contrato"
    model = Contract
    form_class = ContractForm
    template_name = 'contratos/contrato-rechazar.html'
    success_url = reverse_lazy('listarContratos')

    def form_valid(self, form):
        "Valida el formulario de aceptación de un contrato."
        self.object = form.save(commit=False)
        self.object.ProfileId = self.request.user.loginsession.ProfileId
        self.object.Status = 2
        self.object.StatusDescription = 'Rechazado'
        if PatchRefuseToApi(ContractApiserializer(instance=self.object)):
            self.object.save()
        return super(ContratoRefuseUpdateView, self).form_valid(form)
