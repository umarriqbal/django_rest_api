
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """
    Overrides the base user manager that Django provides for a manager customised to the app's needs.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Creates a new user.

        :param str email: Email of the new user.
        :param str password: Password of the new user.
        :param extra_fields: All the extra fields that can be added to the user.
        """
        if not email:
            raise ValueError("User must have an email address.")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """
        Creates a new super user of the app.

        :param str email: Email of the new superuser.
        """
        user = self.create_user(email, password)
        user.is_superuser = True
        user.save(using=self._db)

        return user
