from user.serializers.v2.user import UserSerializerV2
from rest_framework import generics, permissions


class ManageUserViewV2(generics.RetrieveUpdateAPIView):
    """
    Retrieve and Update user via API.
    """
    serializer_class = UserSerializerV2
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """
        Retrieve and return requested authenticated user.
        """
        return self.request.user
