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
    url(r'^subastas/listar/$', views.AuctionListView.as_view(),
        name='listarSubastas'),
    url(r'^subastas/cargar$', views.AuctionsLoadView,
        name='actualizarListaSubastas'),
    url(r'^subasta/participar/(?P<pk>\d+)$',
        views.AuctionParticipateView, name='participarSubasta'),            
    url(r'^subasta/pujar/(?P<pk>\d+)$',
        views.MostrarPujasView, name='mostrarPujaSubasta'),
    url(r'^subasta/puja/actualizar/(?P<pk>\d+)$',
        views.ActualizarPujasView, name='actualizarPujaSubasta'),
        
    url(r'^despachos/listar$', views.DispatchListView.as_view(),
        name='listarDespachos'),
    url(r'^despachos/cargar$', views.DispatchLoadView,
        name='actualizarListaDespachos'),
    url(r'^despachos/detalle(?P<pk>\d+)$',
        views.DispatchDetailView.as_view(), name='detalleDespacho'),
    url(r'^despachos/finalizar/(?P<pk>\d+)$',
        views.DispatchDeliverUpdateView.as_view(), name='finalizarDespacho'),
    url(r'^despachos/cancelar(?P<pk>\d+)$',
        views.DispatchCancelUpdateView.as_view(), name='cancelarDespacho'),                                
                    

]
