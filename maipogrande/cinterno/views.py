from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import ExportInternalProduct
from .services import GetExportInternalProductFromApi


class HomeInternalCustomer(TemplateView):
    "Muestra la página de inicio del cliente interno."
    template_name = 'cinterno/home-interno.html'


def CargarProductosInternosExportacion(request):
    "Carga los productos de exportacion de la base de datos de feria virtual."
    productos = ExportInternalProduct.objects.filter(User_id=request.user.id)
    if productos.count() == 0:
        GetExportInternalProductFromApi(request.user)
        productos = ExportInternalProduct.objects.filter(User_id=request.user.id)
    return render(request, 'cinterno/home-interno.html', {'product_list': productos})
