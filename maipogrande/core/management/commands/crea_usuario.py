import json
from django.contrib.auth.models import User
from login.serializers import LoginSerializer
from django.core.management.base import BaseCommand
from maipogrande.rabbitmq import ConectarRabbitMQ


class Command(BaseCommand):
    help = 'Crea un usuario desde una cola de mensajes rabbitMQ.'

    def handle(self, *args, **kwargs):
        self.conectar_rabbitmq()

    def CrearUsuario(self, json_data):
        "Crea un usuario en la base de datos temporal."
        user = User.objects.create_user(
            username=json_data['Username'], password=json_data['Password'],
            first_name=json_data['FullName'], email=json_data['Email'])
        user.is_staff = True
        user.is_active = True
        user.save()
        return user

    def consumer_callback(self, ch, method, properties, body):
        "Callback de la cola de usuarios"
        json_data = json.loads(body)
        try:
            User.objects.get(username=json_data['Username'])
        except Exception:
            user = self.CrearUsuario(json_data)
            serializador = LoginSerializer(data=json_data, many=False)
            serializador.is_valid()
            serializador.save(User=user)
            print('Usuario {0} creado'.format(user.username))
        return

    def conectar_rabbitmq(self):
        "Conecta a la cola de mensajes de usuarios creados."
        nombre_queue = 'UserWasCreated'
        connection = ConectarRabbitMQ().get_connection()
        channel = connection.channel()
        channel.queue_declare(queue=nombre_queue, durable=True)
        channel.basic_consume(on_message_callback=self.consumer_callback, queue=nombre_queue, auto_ack=True)
        try:
            print('Consumiendo mensajes de cola {0}'.format(nombre_queue))
            channel.start_consuming()
        except KeyboardInterrupt:
            connection.close()
            print('Conexión a RabbitMQ finalizada.')
