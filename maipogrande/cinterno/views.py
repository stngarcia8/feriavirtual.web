from django.shortcuts import render
from django.db.models import Q
from django.views.generic.base import TemplateView
from ordenes.models import ExportProduct
from .services import GetExportInternalProductFromApi
from .models import Offer, OfferDetail
from django.template import loader
from django.http import HttpResponse



class HomeInternalCustomer(TemplateView):
    "Muestra la página de inicio del cliente interno."
    template_name = 'cinterno/home-interno.html'


def CargarProductosInternosExportacion(request):
    "Carga los productos de exportacion de la base de datos de feria virtual."
    productos = ExportProduct.objects.filter(User_id=request.user.id)
    if productos.count() == 0:
        GetExportInternalProductFromApi(request.user)
        productos = ExportProduct.objects.filter(User_id=request.user.id)
    return render(request, 'cinterno/home-interno.html', {'product_list': productos})

def CargarOfertas(request):
    "Carga las ofertas de productos de la base de datos feria virtual."    
    template = loader.get_template("cinterno/ofertas.html")
    ofertas = Offer.objects.filter(Status=1)
    lista_ofertas = []
    for oferta in ofertas:
        detalles = OfferDetail.objects.filter(OfferId=oferta.OfferId)
        lista_ofertas.append([oferta, detalles])
        print(lista_ofertas[0])
    context = {'lista_ofertas': lista_ofertas}
    return HttpResponse(template.render(context, request))
