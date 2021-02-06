
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .user_manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model to be used in the app.
    """

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)

    is_active = models.BooleanField(default=True)
    is_merchant = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

