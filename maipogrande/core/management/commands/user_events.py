from django.contrib.auth.models import User
from login.models import LoginSession
from login.serializers import LoginSerializer


class UserEvents(object):
    "Procesa los eventos de usuarios en el sistema."
    evento = ''
    json_data = ''

    def __init__(self, evento, json_data):
        self.evento = evento
        self.json_data = json_data

    def event_executor(self):
        if self.evento == 'USERWASCREATE':
            self.__crear_usuario(self.json_data)
        elif self.evento == 'USERWASMODIFY':
            self.__editar_usuario(self.json_data)
        elif self.evento == 'USERWASENABLE':
            self.__habilitar_usuario(self.json_data)
        elif self.evento == 'USERWASDISABLE':
            self.__inhabilitar_usuario(self.json_data)

    def __crear_usuario(self, json_data):
        "Crea un usuario en la base de datos temporal."
        user = User.objects.create_user(
            username=json_data['Username'], password=json_data['Password'],
            first_name=json_data['FullName'], email=json_data['Email'])
        user.is_staff = True
        user.is_active = True
        user.save()
        serializador = LoginSerializer(data=json_data, many=False)
        serializador.is_valid()
        serializador.save(User=user)
        print("El usuario {0} {1} ha sido creado.".format(json_data['ProfileName'], json_data['FullName']))
        return

    def __editar_usuario(self, json_data):
        "Edita la información de un usuario."
        user = User.objects.get(username=json_data['Username'])
        user.first_name = json_data['FullName']
        user.email = json_data['Email']
        user.save()
        session = LoginSession.objects.get(UserId=json_data['UserId'])
        session.Username = json_data['Username']
        session.FullName = json_data['FullName']
        session.Email = json_data['Email']
        session.save()
        print("El usuario {0} {1} ha sido modificado.".format(json_data['ProfileName'], json_data['FullName']))
        return

    def __habilitar_usuario(self, json_data):
        "Habilita un usuario en el sistema."
        try:
            sesion = LoginSession.objects.get(UserId=json_data['Id'])
            user = sesion.User
            user.is_active = True
            user.save()
            print("Usuario {0} fue habilitado en el sistema.".format(user.first_name))
        except Exception:
            print("El usuario seleccionado no posee una cuenta en el sitio web.")
        return

    def __inhabilitar_usuario(self, json_data):
        "Inhabilita un usuario en el sistema."
        try:
            sesion = LoginSession.objects.get(UserId=json_data['Id'])
            user = sesion.User
            user.is_active = False
            user.save()
            print("Usuario {0} fue inhabilitado en el sistema.".format(user.first_name))
        except Exception:
            print("El usuario seleccionado no posee una cuenta en el sitio web.")
        return
