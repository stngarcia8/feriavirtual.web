from django.conf.urls import url
from . import views


# Rutas de la aplicacion
urlpatterns = [
    url(r'^producto/$', views.ActualizarListaDeProductos, name='actualizarListaDeProductos'),
    url(r'^producto/all/$', views.ListaDeProductos.as_view(), name='listaDeProductos'),
    url(r'^proeducto/detalle/(?P<pk>\d+)$',
        views.DetalleProducto.as_view(), name='detalleProducto'),
    url(r'^producto/registrar$', views.RegistrarProducto, name='registrarProductos'),
    url(r'^producto/editar/(?P<pk>\d+)$', views.EditarProducto, name='editarProducto'),
    url(r'^producto/confirmar/(?P<pk>\d+)$', views.confirmDeleteProduct.as_view(),
        name='confirmDeleteProduct'),
    url(r'^producto/eliminar/(?P<pk>\d+)$',
        views.EliminarProducto, name='eliminarProducto'),
]
