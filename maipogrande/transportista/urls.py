from django.conf.urls import url
from . import views

# Rutas de la aplicacion
urlpatterns = [
    url(r'^transporte/$', views.ActualizarListaDeTransporte,
        name='actualizarListaDeTransporte'),
    url(r'^transporte/all/$', views.ListaDeTransporte.as_view(), name='listaDeTransporte'),
    url(r'^transporte/registrar$', views.RegistrarTransporte, name='registrarTransporte'),
]

# url(r'^transporte/detalle/(?P<pk>\d+)$',
#     views.DetalleTransporte.as_view(), name='detalleTransporte'),
# url(r'^transporte/registrar$', views.RegistrarTransporte, name='registrarTransporte'),
