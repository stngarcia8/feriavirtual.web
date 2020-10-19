from django.contrib import admin
from django.urls import path, include
from django.conf import settings


# Definicion de las rutas a las urls de las aplicaciones.
urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('login/', include('login.urls')),
    path('productor/', include('productor.urls')),
    path('transportista/', include('transportista.urls')),
    path('dcomercial/', include('dcomercial.urls')),
    path('externo/', include('cexterno.urls')),

]


if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
