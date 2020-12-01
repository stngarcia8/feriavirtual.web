from contratos.serializers import ContratoSerializer
from login.models import LoginSession


class ContractEvents(object):
    "Procesa los eventos de los contratos."
    evento = ''
    json_data = ''

    def __init__(self, evento, json_data):
        self.evento = evento
        self.json_data = json_data

    def event_executor(self):
        if self.evento == 'CONTRACTWASCREATE':
            self.__crear_contrato(self.json_data)

    def __crear_contrato(self, json_data):
        "Notifica la creación de un contrato."
        try:
            session = LoginSession.objects.get(ClientId=json_data['ClientId'])
            serializador = ContratoSerializer(data=json_data)
            serializador.is_valid()
            serializador.save()
            print("El Contrato {0}  para {1} fue creado.".format(json_data['ContractId'], json_data['Customername']))
        except Exception:
            print("No fue posible crear contrato para {0}, el cliente no posee el perfil creado en sitio de feria virtual.".format(json_data['Customername']))
        return

