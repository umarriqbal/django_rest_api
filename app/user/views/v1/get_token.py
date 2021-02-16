
from user.serializers.v1.token import AuthTokenSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class GetToken(TokenObtainPairView):
    """
    Returns a pair of auth token and refresh token in response.

    This is an override class in case we want to update the response of the RestAPI which only returns the
    auth token and refresh token e.g. we can add the expiry time, update keys, etc.
    """
    serializer_class = AuthTokenSerializer
