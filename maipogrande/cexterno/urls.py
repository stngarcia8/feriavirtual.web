from django.conf.urls import url
from . import views


# Rutas de la aplicacion
urlpatterns = [
    # Ruta para la pagina de inicio del cliente externo
    url(r'^home/$', views.HomeExternalCustomer.as_view(),
        name='homeExterno'),
    url(r'^ordenes/cargar/$', views.CargarProductosExportacion,
        name='cargarProductosExportacion'),
    url(r'^ordenes/listar/$', views.OrderListView.as_view(),
        name='listarOrdenes'),
    url(r'^ordenes/ver/(?P<pk>\d+)$',
        views.OrderDetailView.as_view(), name='verOrden'),
    url(r'^ordenes/crear/$', views.OrderCreateView.as_view(),
        name='registrarOrden'),
]
