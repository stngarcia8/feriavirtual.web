from transportista.models import Auction
from transportista.serializers import AuctionSerializer


class AuctionEvents(object):
    "Procesa los eventos de las subastas."
    evento = ''
    json_data = ''

    def __init__(self, evento, json_data):
        self.evento = evento
        self.json_data = json_data

    def event_executor(self):
        if self.evento == 'AUCTIONWASCREATE':
            self.__crear_subasta(self.json_data)
        elif self.evento == 'AUCTIONWASPUBLISH':
            self.__notificar_publicacion_subasta(self.json_data['Id'])
        elif self.evento == 'AUCTIONWASCLOSE':
            self.__notificar_cierre_subasta(self.json_data['Id'])

    def __crear_subasta(self, json_data):
        "Crea una subasta"
        try:
            serializador = AuctionSerializer(data=json_data, many=False)
            serializador.is_valid()
            serializador.save()
            print("La subasta {0} fue creada.".format(json_data['AuctionId']))
        except Exception:
            print("No fue posible crear la subasta {0}.".format(json_data['AuctionId']))
        return 


    def __notificar_publicacion_subasta(self, id):
        "Notifica la publicación de una subasta."
        try:
            subasta = Auction.objects.get(AuctionId=id)
            subasta.Status = 1
            subasta.save()
            print("Subasta {0} fue publicada.".format(id))
        except Exception:
            print("No fue posible publicar la Subasta {0}.".format(id))
        return

    def __notificar_cierre_subasta(self, id):
        "Notifica la publicación de una subasta."
        try:
            subasta = Auction.objects.get(AuctionId=id)
            subasta.Status = 3
            subasta.save()
            print("Subasta {0} fue cerrada.".format(id))
        except Exception:
            print("Subasta {0} no fue posible cerrarla, avise al administrador del sitio.".format(id))
        return
