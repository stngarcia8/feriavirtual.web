from django.conf.urls import url
from . import views


# Rutas de la aplicacion
urlpatterns = [
    url(r'^producto/$', views.ActualizarListaDeProductos, name='actualizarListaDeProductos'),
    url(r'^producto/all/$', views.ListaDeProductos.as_view(), name='listaDeProductos'),
    url(r'^proeducto/detalle/(?P<pk>\d+)$',
        views.DetalleProducto.as_view(), name='detalleProducto'),
    url(r'^producto/registrar$', views.RegistrarProducto, name='registrarProductos'),
]
