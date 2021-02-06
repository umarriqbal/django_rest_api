from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """
        Test whether creating a new user with email is successful.
        """
        email = 'test@django_rest_project.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """
        Test the email for a new user if its email is normalized.
        """
        email = 'test@DJANGO_REST_PROJECT.com'
        password = 'random_string'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email.lower())

    def test_creating_user_with_invalid_email(self):
        """
        Tests if the user being created has a valid email and throws rejection on invalid emails.
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email=None, password='test123')

    def test_create_new_super_user(self):
        """
        Tests creating new super user.
        """
        super_user = get_user_model().objects.create_superuser(
            email='superuser@django_rest_project.com',
            password='test123'
        )
        self.assertTrue(super_user.is_superuser)
