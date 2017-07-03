from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from accounts.models import Account
from bets.models import Bet
from users.models import User

BET_URL = '/api/1.0/bets/'
ALL_BET_URL = '/api/1.0/all_bets/'
SUBSCRIBED_BET_URL = '/api/1.0/subscribed_bets/'


class TestsBets(TestCase):
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
        self.account = Account.objects.create(bank=1000, bookie='bet365')
        self.sport = "football"
        self.type = "HA"
        self.pick = 'Athletic HA +0.5'
        self.stake = 0.1
        self.amount = 25
        self.odds = 1.85
        self.status = 'P'
        self.new_status = 'W'
        self.bet_user = Bet.objects.create(account=self.account, user=self.user)
        self.bet_user_w = Bet.objects.create(account=self.account, user=self.user, status=self.new_status)
        self.bet_user_2 = Bet.objects.create(account=self.account, user=self.user_2)


    """
    Creations tests
    """
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


    """
    Update tests
    """
    def test_update_bet_ok(self):
        response = self.client.patch(BET_URL + str(self.bet_user.pk) + '/', data={
            'status': self.new_status,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data.get('status'), self.new_status)

    def test_update_bet_not_owner_ko(self):
        response = self.client.patch(BET_URL + str(self.bet_user_2.pk) + '/', data={
            'status': self.new_status,
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_user_not_authenticated_bet_ko(self):
        self.client.logout()
        response = self.client.patch(BET_URL + str(self.bet_user.pk) + '/', data={
            'status': self.new_status,
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_bet_incorrect_status_ko(self):
        response = self.client.patch(BET_URL + str(self.bet_user.pk) + '/', data={
            'status': 'incorrect',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    """
    Delete tests
    """
    def test_delete_bet_ok(self):
        response = self.client.delete(BET_URL + str(self.bet_user.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(0, Bet.objects.filter(pk=self.bet_user.pk).count())

    def test_delete_bet_not_owner_ko(self):
        response = self.client_2.delete(BET_URL + str(self.bet_user.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEquals(1, Bet.objects.filter(pk=self.bet_user.pk).count())


    """
    List and Retrieve tests
    """
    def test_list_bets_ok(self):
        response = self.client.get(BET_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), Bet.objects.filter(user=self.user.pk).count())

    def test_list_user_bets_ok(self):
        response = self.client.get(ALL_BET_URL + '?user='+str(self.user_2.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), Bet.objects.filter(user=self.user_2.pk).count())

    def test_list_subscribed_user_bets_ok(self):
        response = self.client.get(SUBSCRIBED_BET_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), Bet.objects.filter(user=self.user_2.pk).count())

    def test_retrieve_bet_ok(self):
        response = self.client.get(BET_URL + str(self.bet_user.pk)+'/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_user_bet_ok(self):
        response = self.client.get(ALL_BET_URL + str(self.bet_user_2.pk)+'/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_subscribed_user_bet_ok(self):
        response = self.client.get(SUBSCRIBED_BET_URL + str(self.bet_user_2.pk)+'/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_bet_not_owner_ko(self):
        response = self.client_2.get(BET_URL + str(self.bet_user.pk)+'/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_filter_wins_bets_ok(self):
        response = self.client.get(BET_URL + '?status='+self.new_status)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), Bet.objects.filter(status=self.new_status).count())
