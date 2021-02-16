import datetime
import math

from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth.models import update_last_login


class AuthTokenSerializer(TokenObtainPairSerializer):
    """
    Serializer for the user authentication token.
    """
    pass

    def validate(self, attrs):
        """
        Validate and authenticate the user.
        """

        data = super(TokenObtainPairSerializer, self).validate(attrs)
        refresh = self.get_token(self.user)

        current_time = datetime.datetime.now().timestamp()
        expire_time = refresh.access_token.payload['exp']
        expires_in = math.ceil(expire_time - current_time)
        data.update({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'expires_in': expires_in,
        })

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
