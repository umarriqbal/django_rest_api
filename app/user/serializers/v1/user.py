from django.contrib.auth import get_user_model
from rest_framework import serializers

from common.validators import password_validator


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User object.
    """
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 8,
                'required': True,
                'allow_blank': False,
                'validators': [password_validator]
            }
        }

    def create(self, validated_data):
        """
        Create a new user with encrypted password and return it.
        """
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """
        Update the user with validated data.
        """
        user_password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if user_password:
            user.set_password(user_password)
            user.save()
        return user

