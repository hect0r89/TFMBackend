from rest_framework.decorators import list_route
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, \
    DestroyModelMixin
from rest_framework.viewsets import GenericViewSet

from bets.models import Bet
from bets.serializers import BetSerializer


class BetViewSet(GenericViewSet, ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin):
    serializer_class = BetSerializer

    def get_queryset(self):
        return Bet.objects.filter(user=self.request.user)

    @list_route(methods=['GET'])
    def subscribed_bets(self):
        #TODO Actualizar cuando se implemente Users
        pass