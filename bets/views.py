from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, \
    DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from django_filters import rest_framework as filters

from bets.models import Bet
from bets.serializers import BetSerializer, BetUserSerializer

class BetViewSet(GenericViewSet, ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin,
                 DestroyModelMixin):
    serializer_class = BetUserSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('status',)

    def get_queryset(self):
        return Bet.objects.filter(user=self.request.user).order_by('-created_at')


class AllBetsViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    serializer_class = BetSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('user',)

    def get_queryset(self):
        return Bet.objects.all().order_by('-created_at')


class SubscribedBetsViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    serializer_class = BetSerializer

    def get_queryset(self):
        return Bet.objects.filter(user__in=self.request.user.subscribers.all()).order_by('-created_at')
