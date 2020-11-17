import pika


class ConectarRabbitMQ(object):
    "Clase que permite obtener la conexión con RabbitMq."
    __host = ''
    __port = 0
    __user = ''
    __password = ''

    def __init__(self):
        self.__host = 'maipogrande-fv.duckdns.org'
        self.__port = 5672
        self.__user = 'fv_user'
        self.__password = 'fv_pwd'

    def get_connection(self):
        credentials = pika.PlainCredentials(self.__user, self.__password)
        parameters = pika.ConnectionParameters(self.__host, self.__port, '/', credentials)
        connection = pika.BlockingConnection(parameters)
        return connection
