from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from accounts.models import Account
from bets.models import Bet
from users.models import User

BET_URL = '/api/1.0/bets/'


class TestsBets(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.username = 'user'
        self.password = '1234'
        self.user = User.objects.create_superuser(username=self.username,
                                                  password=self.password,
                                                  email='user@mail.com')
        self.token, self.created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token))
        self.account = Account.objects.create(bank=1000, bookie='bet365')
        self.sport = "football"
        self.type = "HA"
        self.pick = 'Athletic HA +0.5'
        self.stake = 0.1
        self.amount = 25
        self.odds = 1.85
        self.status = 'P'
        self.new_status = 'W'
        self.bet = Bet.objects.create(account=self.account, user=self.user)

    def test_create_bet_ok(self):
        response = self.client.post(BET_URL, data={'sport': self.sport,
                                                   'type': self.type,
                                                   'pick': self.pick,
                                                   'account': self.account.pk,
                                                   'stake': self.stake,
                                                   'amount': self.amount,
                                                   'odds': self.odds,
                                                   'status': self.status,
                                                   })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_without_mandatory_fields_bet_ko(self):
        response = self.client.post(BET_URL, data={'sport': self.sport,
                                                   'type': self.type,
                                                   'pick': self.pick,
                                                   'stake': self.stake,
                                                   'amount': self.amount,
                                                   'odds': self.odds,
                                                   'status': self.status,
                                                   })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_status_incorrect_bet_ko(self):
        response = self.client.post(BET_URL, data={'sport': self.sport,
                                                   'type': self.type,
                                                   'pick': self.pick,
                                                   'account': self.account.pk,
                                                   'stake': self.stake,
                                                   'amount': self.amount,
                                                   'odds': self.odds,
                                                   'status': 'INCORRECT',
                                                   })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_not_authenticated_bet_ko(self):
        self.client.logout()
        response = self.client.post(BET_URL, data={'sport': self.sport,
                                                   'type': self.type,
                                                   'pick': self.pick,
                                                   'account': self.account.pk,
                                                   'stake': self.stake,
                                                   'amount': self.amount,
                                                   'odds': self.odds,
                                                   'status': self.status,
                                                   })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_bet_ok(self):
        response = self.client.patch(BET_URL+ str(self.bet.pk) + '/', data={
            'status': self.new_status,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data.get('status'), self.new_status)

    def test_update_user_not_authenticated_bet_ko(self):
        self.client.logout()
        response = self.client.patch(BET_URL+ str(self.bet.pk) + '/', data={
            'status': self.new_status,
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_bet_incorrect_status_ko(self):
        response = self.client.patch(BET_URL+ str(self.bet.pk) + '/', data={
            'status': 'incorrect',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_bet_ok(self):
        response = self.client.delete(BET_URL + str(self.bet.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(0, Bet.objects.filter(pk=self.bet.pk).count())
