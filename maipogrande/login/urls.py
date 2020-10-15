from django.conf.urls import url
from . import views


# Rutas de la aplicacion
urlpatterns = [
    # Rutas para los eventos asociados a los inicios de sesion
    url(r'^$', views.iniciarSesion, name='login'),
    url(r'^accessdenied/$', views.Denied.as_view(), name='accessdenied'),
    url(r'^restrictedaccess/$', views.Restricted.as_view(), name='restrictedaccess'),
    url(r'^errorloginservice/$', views.ErrorLoginService.as_view(),
        name='errorloginservice'),
    url(r'^logout/$', views.cerrarSesion, name='logout'),
]
