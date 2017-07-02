from django.test import TestCase
from rest_framework import status

from users.models import User

DEFAULT_PASSWORD = '1234'
URL_LOGIN = '/api/1.0/authentication/login/'
URL_REGISTER = '/api/1.0/authentication/register/'


class LoginTestsAuthentication(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='user',
                                                  password=DEFAULT_PASSWORD,
                                                  email='user@mail.com')

    def test_login_user_ok(self):
        """
        User tries to login
        """
        response = self.client.post(URL_LOGIN, data={'username': 'user', 'password': DEFAULT_PASSWORD})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_user_not_registered_ko(self):
        """
        User not existent tries to login
        """
        response = self.client.post(URL_LOGIN, data={'username': 'user_not', 'password': DEFAULT_PASSWORD})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user_incorrect_pass_ko(self):
        """
        User with incorrect password tries to login 
        """
        response = self.client.post(URL_LOGIN, data={'username': 'user', 'password': 'incorrectpass'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user_not_registered_incorrect_pass_ko(self):
        """
        User not existent and incorrect password tries to login
        """
        response = self.client.post(URL_LOGIN, data={'username': 'user_not', 'password': 'incorrectpass'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RegisterTestsAuthentication(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='user',
                                                  password=DEFAULT_PASSWORD,
                                                  email='user@mail.com')

    def test_register_user_ok(self):
        """
        User tries to register
        """
        response = self.client.post(URL_REGISTER, data={'username': 'user2', 'password': DEFAULT_PASSWORD, 'email': 'user2@email.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_username_existent_ko(self):
        """
        User existent tries to register
        """
        response = self.client.post(URL_REGISTER, data={'username': 'user', 'password': DEFAULT_PASSWORD})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

