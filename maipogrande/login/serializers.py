from rest_framework import serializers
from login.models import LoginSession


# LoginSerializer:
# Serializador de las sesiones de usuario
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginSession
        fields = ('id', 'UserId', 'ClientId', 'Username',
                  'FullName', 'Email', 'ProfileId', 'ProfileName', 'User')
