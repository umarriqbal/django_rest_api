from django.contrib.auth import get_user_model


from common.validators import password_validator
from user.serializers.v1.user import UserSerializer


class UserSerializerV2(UserSerializer):
    """
    Serializer V2 for the User object.

    Changes:
        - Added additional field to get. ('is_staff')
    """
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name', 'is_staff')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 8,
                'required': True,
                'allow_blank': False,
                'validators': [password_validator]
            }
        }
