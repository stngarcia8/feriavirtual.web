from rest_framework import serializers
from.models import ComercialInfo, City, Country


# ComercialSerializer:
# Serializador de los datos comerciales de los clientes.
class ComercialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComercialInfo
        fields = ('CompanyName', 'FantasyName', 'ComercialBusiness',
                  'Email', 'ComercialDNI', 'Address', 'City', 'Country', 'PhoneNumber')


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('CountryID', 'CountryName', 'CountryPrefix')


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('CityID', 'CityName')


# ComercialSaveSerializer:
# Serializador que permite evaluar los datos provenientes de la api
# # para poder almacenarlosde forma correcta en el almacenamiento temporal.
class ComercialSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComercialInfo
        fields = ('id', 'ClientID', 'ComercialID',
                  'CompanyName', 'FantasyName', 'ComercialBusiness',
                  'Email', 'ComercialDNI', 'Address', 'City', 'Country', 'PhoneNumber', 'User')
        depth = 1
