import pika
import json
from django.contrib.auth.models import User
from login.serializers import LoginSerializer


def consumer_callback(ch, method, properties, body):
    "Callback de la cola de usuarios"
    json_data = json.loads(body)
    try:
        User.objects.get(username=json_data['Username'])
    except Exception:
        user = CrearUsuario(json_data)
        serializador = LoginSerializer(data=json_data, many=False)
        serializador.is_valid()
        serializador.save(User=user)
    return


def LoadUserFromRabbitMQ():
    "Carga los usuarios y crea su objeto user desde la cola de rabbitMQ"
    host = 'maipogrande-fv.duckdns.org'
    port = 5672
    user = 'fv_user'
    password = 'fv_pwd'
    credentials = pika.PlainCredentials(user, password)
    parameters = pika.ConnectionParameters(host, port, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    my_queue = 'UserWasCreated'
    channel.queue_declare(queue=my_queue, durable=True)
    channel.basic_consume(on_message_callback=consumer_callback, queue=my_queue, auto_ack=True)
    channel.start_consuming()
    connection.close()


def CrearUsuario(json_data):
    "Crea un usuario en la base de datos temporal."
    user = User.objects.create_user(
        username=json_data['Username'], password=json_data['Password'],
        first_name=json_data['FullName'], email=json_data['Email'])
    user.is_staff = True
    user.is_active = True
    user.save()
    return user
