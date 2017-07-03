from rest_framework.decorators import detail_route
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(GenericViewSet, ListModelMixin, UpdateModelMixin, RetrieveModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @detail_route(methods=['post'])
    def subscribe(self, request, pk=None):
        request.user.subscribers.add(self.get_object())
        return Response({'Ok': 'User subscribe correctly'})

    @detail_route(methods=['post'])
    def unsubscribe(self, request, pk=None):
        request.user.subscribers.remove(self.get_object())
        return Response({'Ok': 'User unsubscribe correctly'})

