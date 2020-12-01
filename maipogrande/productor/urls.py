from django.conf.urls import url
from . import views


# Rutas de la aplicacion
urlpatterns = [
    # Ruta para la pagina de inicio del productor
    url(r'^home/$', views.HomeProducer.as_view(),
        name='homeProducer'),
    url(r'^productos/cargar$', views.ProductosLoadView,
        name='actualizarListaProductos'),
    url(r'^productos/listar/$', views.ProductoListView.as_view(),
        name='listarProductos'),
    url(r'^productos/detalle/(?P<pk>\d+)$',
        views.ProductoDetailView.as_view(), name='detalleProducto'),
    url(r'^productos/crear/$', views.ProductoCreateView.as_view(),
        name='registrarProducto'),
    url(r'^productos/actualizar/(?P<pk>\d+)$',
        views.ProductoUpdateView.as_view(), name='editarProducto'),
    url(r'^productos/eliminar/(?P<pk>\d+)$',
        views.ProductoDeleteView.as_view(), name='eliminarProducto'),
    url(r'^historial/ventas/listar$',
        views.HistorialVentasListView.as_view(), name='listarVentas'),
    url(r'^historial/ventas/cargar$', views.VentasLoadView,
        name='actualizarListaVentas'),
    url(r'^ventas/estadisticas/ver/$',
        views.EstadisticasVentasDetailView, name='verEstadisticasVentas'),                 
]
