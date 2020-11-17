from .tasks.user_task import LoadUserFromRabbitMQ


def CargarNuevoUsuario(request):
    LoadUserFromRabbitMQ()
    return
