from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import ExportProduct
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