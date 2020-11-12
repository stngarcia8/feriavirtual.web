from rest_framework import serializers
from login.models import LoginSession


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginSession
        fields = ('id', 'UserId', 'ClientId', 'Username',
                  'FullName', 'Email', 'ProfileId', 'ProfileName', 'User')
