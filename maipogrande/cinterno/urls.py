from django.conf.urls import url
from . import views


# Rutas de la aplicacion
urlpatterns = [
    # Ruta para la pagina de inicio del cliente externo
    url(r'^home/$', views.HomeInternalCustomer.as_view(),
        name='homeInterno'),
    url(r'^ordenes/cargar/$', views.CargarProductosInternosExportacion,
        name='cargarProductosInternosExportacion'),    
    url(r'^ofertas/cargar/$', views.CargarOfertas,
        name='cargarOfertas'),    
]
