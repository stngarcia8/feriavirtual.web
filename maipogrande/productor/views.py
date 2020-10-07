from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from .models import Producto


# ListarProductos(request):
# Visualiza la lista de productos de un productor
@login_required(login_url='login')
def ListarProductos(request):
    datos = Producto.objects.filter(User_id=request.user.id)
    if datos.count() == 0:
        pass
    template_name = loader.get_template('productor/producto-listar.html')
    context_data = {'productos': datos}
    return HttpResponse(template_name.render(context_data, request))
