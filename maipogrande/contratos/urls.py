from django.conf.urls import url
from . import views


urlpatterns = [
    # Rutas para los contratos
    url(r'^contratos/listar/$', views.ContratoListView.as_view(),
        name='listarContratos'),
    url(r'^contratos/cargar$', views.ContratosLoadView,
        name='cargarContratos'),
    url(r'^contratos/detalle/(?P<pk>\d+)$',
        views.ContratoDetailView.as_view(), name='detalleContrato'),
    url(r'^contratos/aceptar/(?P<pk>\d+)$',
        views.ContratoAcceptUpdateView.as_view(), name='aceptarContrato'),
    url(r'^contratos/rechazar/(?P<pk>\d+)$',
        views.ContratoRefuseUpdateView.as_view(), name='rechazarContrato'),

]
