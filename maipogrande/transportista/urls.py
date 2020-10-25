from django.conf.urls import url
from . import views


urlpatterns = [
    # Ruta para la pagina de inicio del transportista
    url(r'^home/$', views.HomeCarrier.as_view(),
        name='homeCarrier'),
    url(r'^vehiculos/cargar$', views.VehiculosLoadView,
        name='actualizarListaVehiculos'),
    url(r'^vehiculos/listar/$', views.VehiculoListView.as_view(),
        name='listarVehiculos'),
    url(r'^vehiculos/detalle/(?P<pk>\d+)$',
        views.VehiculoDetailView.as_view(), name='detalleVehiculo'),
    url(r'^vehiculos/crear/$', views.VehiculoCreateView.as_view(),
        name='registrarVehiculo'),
    url(r'^vehiculo/actualizar/(?P<pk>\d+)$',
        views.VehiculoUpdateView.as_view(), name='editarVehiculo'),
    url(r'^vehiculo/eliminar/(?P<pk>\d+)$',
        views.VehiculoDeleteView.as_view(), name='eliminarVehiculo'),

]
