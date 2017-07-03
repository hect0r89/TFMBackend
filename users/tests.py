from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from users.models import User

URL_USERS = '/api/1.0/users/'
URL_SUBSCRIBE = '/subscribe/'
URL_UNSUBSCRIBE = '/unsubscribe/'


class TestsUsers(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client_2 = APIClient()
        self.username = 'user'
        self.username_2 = 'user_2'
        self.new_username = 'new_username'
        self.password = '1234'
        self.user = User.objects.create_superuser(username=self.username,
                                                  password=self.password,
                                                  email='user@mail.com')
        self.user_2 = User.objects.create_superuser(username=self.username_2,
                                                    password=self.password,
                                                    email='user2@mail.com')
        self.token_user, self.created = Token.objects.get_or_create(user=self.user)
        self.token_user_2, self.created = Token.objects.get_or_create(user=self.user_2)
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token_user))
        self.client_2.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token_user_2))

    def test_list_users_ok(self):
        response = self.client.get(URL_USERS)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), User.objects.all().count())

    def test_retrieve_user_ok(self):
        response = self.client.get(URL_USERS + str(self.user_2.pk)+'/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_subscribe_user_ok(self):
        response = self.client.post(URL_USERS + str(self.user_2.pk) + URL_SUBSCRIBE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unsubscribe_user_ok(self):
        response = self.client.post(URL_USERS + str(self.user_2.pk) + URL_UNSUBSCRIBE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_ok(self):
        response = self.client.patch(URL_USERS + str(self.user.pk) + '/', data={'username': self.new_username})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('username'), self.new_username)

    def test_update_user_different_ko(self):
        response = self.client.patch(URL_USERS + str(self.user_2.pk) + '/', data={'username': self.new_username})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
