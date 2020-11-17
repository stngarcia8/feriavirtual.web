from rest_framework import serializers
from.models import Comercial, City, Country

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('CountryId', 'CountryName', 'CountryPrefix')


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('CityId', 'CityName')


class ComercialSerializer(serializers.ModelSerializer):
    Country = CountrySerializer()
    City = CitySerializer()

    class Meta:
        model = Comercial
        fields = ('ComercialId', 'ClientId', 'CompanyName', 'FantasyName', 'ComercialBusiness',
                  'Email', 'ComercialDni', 'Address',
                  'City', 'Country', 'PhoneNumber', 'User')
        depth = 1

    def create(self, data):
        id = data['Country']['CountryId']
        country = Country.objects.get(CountryId=id)
        id = data['City']['CityId']
        city = City.objects.get(CityId=id)
        com = Comercial.objects.create(
            ComercialId=data['ComercialId'], ClientId=data['ClientId'],
            CompanyName=data['CompanyName'], FantasyName=data['FantasyName'],
            ComercialBusiness=data['ComercialBusiness'], Email=data['Email'],
            ComercialDni=data['ComercialDni'], Address=data['Address'],
            City=city, Country=country, PhoneNumber=data['PhoneNumber'],
            User=data['User']
        )
        return com
    
class ComercialApiSerializer(serializers.ModelSerializer):
    "Almacena los datos para enviarlos a la api feria virtual"
    Country = CountrySerializer()
    City = CitySerializer()

    class Meta:
        model = Comercial
        fields = ('ComercialId', 'ClientId',
                  'CompanyName', 'FantasyName', 'ComercialBusiness',
                  'Email', 'ComercialDni', 'Address', 'City', 'Country', 'PhoneNumber')
        depth = 1
