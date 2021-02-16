from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework_simplejwt.exceptions import TokenError

from rest_framework.test import APIClient
from rest_framework import status

from unittest.mock import patch
from .helpers import create_user

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
REFRESH_TOKEN_URL = reverse('user:refresh_token')
ME_URL = reverse('user:me')


class PublicUserAPITests(TestCase):

    def setUp(self):

        self.client = APIClient()

    def test_create_valid_user_success(self):
        """
        Test that the user with valid payload is created successfully.
        """
        payload = {
            'email': 'umar@djangotest.com',
            'password': 'testpassword123',
            'name': 'umar test'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_duplicate_user_fail(self):
        """
        Test that a user creation fails if it's already present.
        """
        payload = {
            'email': 'umar@djangotest.com',
            'password': 'testpassword123',
            'name': 'umar test'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """
        Test that a user creation fails if the password provided does not meet the requirement: too short.
        """
        payload = {
            'email': 'umar@djangotest.com',
            'password': 'tp',
            'name': 'umar test'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload['email']).exists()
        self.assertEqual(user_exists, False)

    def test_password_should_have_numbers(self):
        """
        Test that a user creation fails if the password provided does not meet the requirement: numbers.
        """
        payload = {
            'email': 'umar@djangotest.com',
            'password': 'testpass',
            'name': 'umar test'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload['email']).exists()
        self.assertEqual(user_exists, False)

    def test_password_should_have_alphabets(self):
        """
        Test that a user creation fails if the password provided does not meet the requirement: alphabets.
        """
        payload = {
            'email': 'umar@djangotest.com',
            'password': '12345',
            'name': 'umar_test'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload['email']).exists()
        self.assertEqual(user_exists, False)

    def test_create_token(self):
        """
        Test that a valid access token is created for the user.
        """
        payload = {
            'email': 'umar@djangotest.com',
            'password': 'testpass123',
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('access', res.data)

    def test_create_token_with_invalid_credentials(self):
        """
        Test that token is not created when invalid credentials are given.
        """
        payload = {
            'email': 'umar@djangotest.com',
            'password': 'testpass123',
            'name': 'test user'
        }
        invalid_payload = {
            'email': 'umar@djangotest.com',
            'password': 'wrongpassword',
            'name': 'test user'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, invalid_payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_against_non_existent_user(self):
        """
        Test that a token is not created against non existent user.
        """
        payload = {
            'email': 'umar@djangotest.com',
            'password': 'testpass123',
            'name': 'test user'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    @patch('rest_framework_simplejwt.serializers.TokenRefreshSerializer.validate')
    def test_valid_refresh_token(self, validate_mock):
        """
        Test that the refresh token can be used to return an access token.
        """
        payload = {
            'refresh': 'some_refresh_token',
        }
        validate_mock.side_effect = {"access": "some_access_token", "refresh": "some_refresh_token"}
        res = self.client.post(REFRESH_TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('access', res.data)

    @patch('rest_framework_simplejwt.serializers.TokenRefreshSerializer.validate')
    def test_invalid_refresh_token(self, validate_mock):
        """
        Test that an invalid refresh token will not return an access token.
        """
        payload = {
            'refresh': 'some_refresh_token',
        }
        validate_mock.side_effect = TokenError('Token is invalid or expired.')
        res = self.client.post(REFRESH_TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('access', res.data)

    def test_access_token_expires(self):
        pass

    def test_retrieve_user_unauthorized(self):
        """
        Test that unauthorized request is unsuccessful.
        """
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITests(TestCase):
    """
    Test user APIs that require authentication.
    """

    def setUp(self):
        self.user = create_user(
            email="django_test@djangotester.com",
            password="password123",
            name="Django PrivateTester"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_user_success(self):
        """
        Test that an authenticated user can get their profile.
        """
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_retrieve_user_with_post_not_allowed(self):
        """
        Test that an authenticated user can not update their profile with POST.
        """
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user(self):
        """
        Test updating an authenticated user with PATCH/PUT.
        """
        payload = {
            "email": "newdjango_test@djangotester.com",
            "password": "Newpassword123",
            "name": "NewDjango PrivateTester"
        }
        res = self.client.patch(ME_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertEqual(self.user.email, payload['email'])
        self.assertTrue(self.user.check_password(payload['password']))

