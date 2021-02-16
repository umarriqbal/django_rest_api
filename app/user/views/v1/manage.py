from user.serializers.v1.user import UserSerializer
from rest_framework import generics, permissions


class ManageUserView(generics.RetrieveUpdateAPIView):
    """
    Retrieve and Update user via API.
    """
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """
        Retrieve and return requested authenticated user.
        """
        return self.request.user
