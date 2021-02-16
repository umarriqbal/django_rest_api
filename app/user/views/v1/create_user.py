from user.serializers.v1.user import UserSerializer
from rest_framework import generics


class CreateUserView(generics.CreateAPIView):
    """
    Create new user view.
    """
    serializer_class = UserSerializer
