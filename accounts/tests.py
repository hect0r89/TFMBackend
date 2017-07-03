from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from accounts.models import Account
from users.models import User

ACCOUNT_URL = '/api/1.0/accounts/'


class TestsAccounts(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client_2 = APIClient()
        self.username = 'user'
        self.username_2 = 'user_2'
        self.password = '1234'
        self.user = User.objects.create_superuser(username=self.username,
                                                  password=self.password,
                                                  email='user@mail.com')
        self.user_2 = User.objects.create_superuser(username=self.username_2,
                                                    password=self.password,
                                                    email='user2@mail.com')
        self.user.subscribers.add(self.user_2)
        self.token_user, self.created = Token.objects.get_or_create(user=self.user)
        self.token_user_2, self.created = Token.objects.get_or_create(user=self.user_2)
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token_user))
        self.client_2.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token_user_2))
        self.amount = 1500
        self.new_amount = 2000
        self.bookie = 'bet365'
        self.account = Account.objects.create(bank=self.amount, bookie=self.bookie, user=self.user)
        self.account_2 = Account.objects.create(bank=self.amount, bookie=self.bookie, user=self.user)
        self.account_3 = Account.objects.create(bank=self.amount, bookie=self.bookie, user=self.user_2)

    def test_create_account_ok(self):
        response = self.client.post(ACCOUNT_URL, data={'bank': self.amount,
                                                       'bookie': self.bookie,
                                                       })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_accounts_ok(self):
        response = self.client.get(ACCOUNT_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Account.objects.filter(user=self.user).count())

    def test_retrieve_account_ok(self):
        response = self.client.get(ACCOUNT_URL + str(self.account.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_not_owner_account_ok(self):
        response = self.client_2.get(ACCOUNT_URL + str(self.account.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_account_ko(self):
        response = self.client.delete(ACCOUNT_URL + str(self.account.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_not_owner_account_ko(self):
        response = self.client_2.delete(ACCOUNT_URL + str(self.account.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_account_ok(self):
        response = self.client.patch(ACCOUNT_URL + str(self.account.pk) + '/', data={'bank': self.new_amount})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('bank'), self.new_amount)

    def test_update_account_not_owner_ko(self):
        response = self.client_2.patch(ACCOUNT_URL + str(self.account.pk) + '/', data={'bank': self.new_amount})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
