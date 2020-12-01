from rest_framework import serializers
from.models import Offer, OfferDetail



class OfferDetailSerializer(serializers.ModelSerializer):
    "Serializador del detalle de ofertas"
    class Meta:
        model = OfferDetail
        fields = ('OfferDetailId', 'OfferId', 'Offer', 'ProductId', 'ProductName',
                'ActualValue', 'Percent', 'OfferValue')


class OfferSerializer(serializers.ModelSerializer):
    "Serializador de las ofertas de productos."
    Details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ('OfferId', 'Description', 'Discount', 'OfferType', 'TypeDescription',
                'PublishDate', 'Status', 'StatusDescription', 'Details')
        depth = 1

    def create(self, data):
        ofr = Offer.objects.create(
            OfferId=data['OfferId'], Description=data['Description'],
            Discount=data['Discount'], OfferType=data['OfferType'],
            TypeDescription=data['TypeDescription'], PublishDate=data['PublishDate'],
            Status=data['Status'], StatusDescription=data['StatusDescription'],   
        )
        detalle = OfferDetailSerializer(data=data['Details'], many=True)
        detalle.is_valid()
        detalle.save(Offer=ofr)
        return ofr
